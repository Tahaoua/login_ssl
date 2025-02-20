import json
import os
from datetime import datetime

class SessionManager:
    def __init__(self):
        self.sessions = {}
        self.session_file = 'sessions.json'
        self.load_sessions()

    def load_sessions(self):
        if os.path.exists(self.session_file):
            try:
                with open(self.session_file, 'r') as f:
                    data = json.load(f)
                    # Convert string timestamps back to datetime objects
                    for session in data.values():
                        session['timestamp'] = datetime.fromisoformat(session['timestamp'])
                    self.sessions = data
            except:
                self.sessions = {}

    def save_sessions(self):
        # Convert datetime to string for JSON serialization
        sessions_copy = {}
        for session_id, session_data in self.sessions.items():
            sessions_copy[session_id] = session_data.copy()
            sessions_copy[session_id]['timestamp'] = session_data['timestamp'].isoformat()
        
        with open(self.session_file, 'w') as f:
            json.dump(sessions_copy, f)

    def add_session(self, session_id, username):
        self.sessions[session_id] = {
            'username': username,
            'status': 'waiting',
            'timestamp': datetime.now()
        }
        self.save_sessions()

    def get_session(self, session_id):
        self.load_sessions()  # Reload to get latest data
        return self.sessions.get(session_id)

    def approve_session(self, session_id):
        if session_id in self.sessions:
            self.sessions[session_id]['status'] = 'approved'
            self.save_sessions()
            return True
        return False

    def remove_session(self, session_id):
        if session_id in self.sessions:
            del self.sessions[session_id]
            self.save_sessions()

    def get_pending_sessions(self):
        self.load_sessions()  # Reload to get latest data
        return {
            session_id: session_data 
            for session_id, session_data in self.sessions.items() 
            if session_data['status'] == 'waiting'
        }

# Create a global session manager instance
session_manager = SessionManager() 