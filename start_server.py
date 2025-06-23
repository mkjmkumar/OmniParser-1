#!/usr/bin/env python3
import os
import sys
import subprocess
from dotenv import load_dotenv

def start_server():
    # Load environment variables from .env file
    load_dotenv()
    
    # Get configuration from environment variables
    flask_app = os.getenv('FLASK_APP')
    host = os.getenv('SERVER_HOST')
    port = os.getenv('SERVER_PORT')
    workers = os.getenv('WORKERS')
    log_level = os.getenv('LOG_LEVEL')
    access_log = os.getenv('ACCESS_LOG_FILE')
    error_log = os.getenv('ERROR_LOG_FILE')
    capture_output = os.getenv('CAPTURE_OUTPUT', 'true').lower() == 'true'
    timeout = os.getenv('REQUEST_TIMEOUT')
    
    # Build the gunicorn command
    cmd = [
        'gunicorn',
        '-w', workers,
        '-b', f'{host}:{port}',
        flask_app,
        '--log-level', log_level,
        '--access-logfile', access_log,
        '--error-logfile', error_log,
        '--timeout', timeout
    ]
    
    if capture_output:
        cmd.append('--capture-output')
    
    # Print the command being executed
    print(f"Starting server with command: {' '.join(cmd)}")
    
    # Execute the command
    try:
        subprocess.run(cmd)
    except KeyboardInterrupt:
        print("\nServer stopped by user")
    except Exception as e:
        print(f"Error starting server: {e}")
        sys.exit(1)

if __name__ == "__main__":
    start_server()