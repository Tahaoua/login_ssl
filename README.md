# Secure Two-Factor Login System with SSL

A secure Flask-based login system that implements SSL encryption and two-factor authentication through an admin approval process. This project demonstrates secure authentication practices including HTTPS, secure cookie handling, and a two-server approval system.

## Features

- 🔒 SSL/HTTPS encryption on both servers
- 🔐 Two-factor authentication via admin approval
- 🍪 Secure session management with cookies
- 👤 User authentication
- 🛡️ Protected routes
- 📱 Responsive design
- 🔄 Real-time status updates
- ⚡ Automatic redirects after approval

## Prerequisites

- Python 3.x
- pip (Python package manager)
- OpenSSL (for certificate generation)

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd login_ssl
```

2. Install the required dependencies:
```bash
pip install -r requirements.txt
```

3. Generate SSL certificate (already done, but if needed):
```bash
openssl req -x509 -newkey rsa:4096 -nodes -out cert.pem -keyout key.pem -days 365 -subj "/CN=localhost"
```

## Project Structure

```
login_ssl/
├── app.py              # Login server (port 443)
├── protected_server.py # Admin approval server (port 5000)
├── shared_session.py   # Shared session management
├── requirements.txt    # Python dependencies
├── cert.pem           # SSL certificate
├── key.pem            # SSL private key
├── templates/
│   ├── login.html        # Login page template
│   ├── waiting.html      # Waiting for approval page
│   ├── protected.html    # Protected content page
│   └── admin_dashboard.html  # Admin approval dashboard
└── README.md          # This file
```

## Running the Application

1. Start both servers in separate terminal windows:
```bash
# Terminal 1 - Start login server
python app.py

# Terminal 2 - Start admin approval server
python protected_server.py
```

2. Access the application:
   - Users visit `https://localhost:443` for the login page
   - Admins visit `https://localhost:5000` for the approval dashboard
   - You may need to accept the self-signed certificate warning in your browser

## Authentication Flow

1. **Initial Login (Port 443)**
   - User enters credentials at `https://localhost:443`
   - Upon successful login, user enters a waiting state
   - Real-time status updates show approval progress

2. **Admin Approval (Port 5000)**
   - Admin visits `https://localhost:5000`
   - Views pending login requests in the dashboard
   - Can approve or deny each request
   - Dashboard auto-refreshes to show new requests

3. **Post-Approval**
   - Upon admin approval, user is automatically redirected to protected content
   - Session remains active until logout or denial
   - Admin can continue to monitor new login requests

## Test Credentials

For demonstration purposes, use these credentials:
- Username: `demo`
- Password: `password`

## Security Features

1. **SSL/HTTPS Encryption**
   - All traffic is encrypted using SSL on both servers
   - Self-signed certificate for development (use proper SSL cert for production)

2. **Secure Session Management**
   - Session IDs are cryptographically secure
   - Cookies are set with HTTPOnly and Secure flags
   - SameSite cookie attribute set to Strict
   - File-based session storage for server synchronization

3. **Two-Factor Authentication**
   - Initial password-based authentication
   - Secondary admin approval requirement
   - Real-time session status monitoring

4. **Protected Routes**
   - Authentication required for accessing protected pages
   - Automatic redirection for unauthorized access
   - Separate servers for login and protected content

## Production Considerations

Before deploying to production, implement the following:

1. Replace the self-signed certificate with a proper SSL certificate from a trusted CA
2. Implement a proper user database with password hashing
3. Use a production-grade session store (e.g., Redis) for sharing sessions between servers
4. Configure proper security headers
5. Implement rate limiting
6. Add logging and monitoring
7. Use environment variables for sensitive configuration
8. Consider using a reverse proxy for handling multiple servers
9. Implement session timeout and automatic cleanup
10. Add IP-based tracking for suspicious login attempts

## Contributing

Feel free to submit issues and enhancement requests!

## License

[MIT License](LICENSE)

## Security Notice

This is a demonstration project. While it implements several security best practices, additional security measures should be implemented for production use. The two-factor authentication implementation shown here is a simplified version for demonstration purposes. 