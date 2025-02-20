from flask import Flask, render_template, request, redirect
import ssl
from shared_session import session_manager

protected_app = Flask(__name__)

@protected_app.route('/')
def protected_home():
    pending_sessions = session_manager.get_pending_sessions()
    return render_template('admin_dashboard.html', pending_sessions=pending_sessions)

@protected_app.route('/content')
def protected_content():
    session_id = request.cookies.get('session_id')
    if not session_id:
        return redirect('https://localhost:443')
    
    session = session_manager.get_session(session_id)
    if not session or session['status'] != 'approved':
        return redirect('https://localhost:443')
    
    return render_template('protected.html', 
                         username=session['username'])

@protected_app.route('/approve/<session_id>', methods=['POST'])
def approve_session(session_id):
    if session_manager.approve_session(session_id):
        return redirect('/')
    return "Invalid session", 400

@protected_app.route('/deny/<session_id>', methods=['POST'])
def deny_session(session_id):
    session_manager.remove_session(session_id)
    return redirect('/')

if __name__ == '__main__':
    # SSL context for protected server
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    context.load_cert_chain('cert.pem', 'key.pem')
    
    # Run protected content server on port 5000
    protected_app.run(host='0.0.0.0', port=5000, ssl_context=context, debug=True) 