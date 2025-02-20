from flask import Flask, render_template, request, make_response, redirect
import ssl
import secrets
from shared_session import session_manager

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)

@app.route('/')
def index():
    session_id = request.cookies.get('session_id')
    if session_id:
        session = session_manager.get_session(session_id)
        if session:
            if session['status'] == 'approved':
                return redirect('https://localhost:5000/content')
            return render_template('waiting.html')
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')
    
    if username == "demo" and password == "password":
        session_id = secrets.token_hex(16)
        session_manager.add_session(session_id, username)
        
        response = make_response(render_template('waiting.html'))
        response.set_cookie('session_id', session_id, secure=True, httponly=True, samesite='Strict')
        return response
    
    return "Invalid credentials", 401

@app.route('/check_status')
def check_status():
    session_id = request.cookies.get('session_id')
    if not session_id:
        return {'status': 'invalid'}
    
    session = session_manager.get_session(session_id)
    if not session:
        return {'status': 'invalid'}
    
    if session['status'] == 'approved':
        return {'status': 'approved', 'redirect_url': 'https://localhost:5000/content'}
    return {'status': 'waiting'}

@app.route('/logout')
def logout():
    session_id = request.cookies.get('session_id')
    if session_id:
        session_manager.remove_session(session_id)
    response = make_response(redirect('/'))
    response.delete_cookie('session_id')
    return response

if __name__ == '__main__':
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    context.load_cert_chain('cert.pem', 'key.pem')
    app.run(host='0.0.0.0', port=443, ssl_context=context, debug=True) 