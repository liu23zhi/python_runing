"""
Web Mode Module with UUID-based Session Management

This module provides a Flask-based web interface with:
- Automatic UUID assignment for each session
- Session persistence across browser reopens
- Isolation between different users to prevent lag
"""

import uuid
import threading
from flask import Flask, request, redirect, url_for, session, render_template_string, jsonify
import secrets


# Global dictionary to store active sessions
# Format: {uuid_str: {'api': api_instance, 'last_access': timestamp, 'data': {...}}}
active_sessions = {}
sessions_lock = threading.Lock()


def create_app(api_instance, webview_ready_event):
    """
    Create and configure the Flask application with UUID-based session management.
    
    Args:
        api_instance: The Api instance from main.py
        webview_ready_event: Threading event to signal when pywebview is ready
    
    Returns:
        Flask application instance
    """
    app = Flask(__name__)
    app.secret_key = secrets.token_hex(32)  # Generate a secure secret key
    
    # Store the API instance and event for use in routes
    app.api_instance = api_instance
    app.webview_ready_event = webview_ready_event
    
    @app.route('/')
    def index():
        """
        Root route - handles initial access and UUID assignment.
        If no session UUID exists, generate one and redirect.
        """
        # Check if user already has a session UUID in Flask session
        session_uuid = session.get('uuid')
        
        if not session_uuid:
            # Generate new UUID for this session
            session_uuid = str(uuid.uuid4()).replace('-', '')
            session['uuid'] = session_uuid
            
            # Store in active sessions
            with sessions_lock:
                active_sessions[session_uuid] = {
                    'api': api_instance,
                    'created': threading.current_thread().getName(),
                    'data': {}
                }
            
            # Redirect to UUID-specific URL
            return redirect(url_for('session_view', session_uuid=session_uuid))
        else:
            # User has a session, redirect to their UUID URL
            return redirect(url_for('session_view', session_uuid=session_uuid))
    
    @app.route('/uuid=<session_uuid>')
    def session_view(session_uuid):
        """
        UUID-specific session view.
        Each UUID gets its own isolated session.
        """
        # Validate UUID format (32 hex chars for uuid4 without hyphens)
        if len(session_uuid) != 32 or not all(c in '0123456789abcdef' for c in session_uuid.lower()):
            return "Invalid session ID", 400
        
        # Store UUID in session if not already there
        if session.get('uuid') != session_uuid:
            session['uuid'] = session_uuid
        
        # Ensure session exists in active_sessions
        with sessions_lock:
            if session_uuid not in active_sessions:
                active_sessions[session_uuid] = {
                    'api': api_instance,
                    'created': threading.current_thread().getName(),
                    'data': {}
                }
        
        # Wait for pywebview to be ready (this ensures JS engine is available)
        if not webview_ready_event.is_set():
            webview_ready_event.wait(timeout=30)
        
        # Render the main HTML interface
        # We'll inject the session UUID into the page for client-side use
        try:
            with open('/home/runner/work/python_runing/python_runing/index.html', 'r', encoding='utf-8') as f:
                html_content = f.read()
            
            # Inject session UUID into the page
            html_with_uuid = html_content.replace(
                '<script>',
                f'<script>\nwindow.SESSION_UUID = "{session_uuid}";\n',
                1  # Only replace first occurrence
            )
            
            return html_with_uuid
        except FileNotFoundError:
            return "Application not properly configured", 500
    
    @app.route('/api/<path:api_method>', methods=['GET', 'POST'])
    def api_proxy(api_method):
        """
        Proxy API calls to the Python backend.
        Uses the session UUID to isolate data between users.
        """
        session_uuid = session.get('uuid')
        if not session_uuid:
            return jsonify({"success": False, "message": "No active session"}), 403
        
        with sessions_lock:
            if session_uuid not in active_sessions:
                return jsonify({"success": False, "message": "Session expired"}), 403
            
            session_data = active_sessions[session_uuid]
        
        # Get the API instance
        api = session_data['api']
        
        # Parse request data
        if request.method == 'POST':
            data = request.get_json() or request.form.to_dict()
        else:
            data = request.args.to_dict()
        
        # Call the appropriate API method
        try:
            # Convert api_method to Python method name
            method_name = api_method.replace('-', '_')
            
            if hasattr(api, method_name):
                method = getattr(api, method_name)
                
                # Call method with unpacked data
                if data:
                    result = method(**data)
                else:
                    result = method()
                
                return jsonify(result if result else {"success": True})
            else:
                return jsonify({"success": False, "message": f"Method {method_name} not found"}), 404
        
        except Exception as e:
            return jsonify({"success": False, "message": str(e)}), 500
    
    @app.route('/health')
    def health():
        """Health check endpoint"""
        return jsonify({
            "status": "ok",
            "active_sessions": len(active_sessions),
            "pywebview_ready": webview_ready_event.is_set()
        })
    
    @app.route('/sessions')
    def list_sessions():
        """Debug endpoint to list active sessions (can be disabled in production)"""
        with sessions_lock:
            return jsonify({
                "active_sessions": list(active_sessions.keys()),
                "count": len(active_sessions)
            })
    
    return app
