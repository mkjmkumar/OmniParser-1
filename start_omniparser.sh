#!/bin/bash

# Create startup monitor script
cat > /opt/app-root/src/OmniParser/monitor_app.sh << 'EOL'
#!/bin/bash

# Log file location
LOG_FILE="/opt/app-root/src/OmniParser/monitor.log"

# Function to start the app
start_app() {
    cd /opt/app-root/src/OmniParser
    
    # Check if virtual environment exists
    if [ ! -d "venv" ]; then
        echo "$(date): Creating virtual environment..." >> $LOG_FILE
        python3 -m venv venv
        source venv/bin/activate
        pip install --upgrade pip
        
        if [ -f "requirements.txt" ]; then
            pip install -r requirements.txt
        fi
    else
        source venv/bin/activate
    fi
    
    # Check if app is already running
    if ! pgrep -f "python gradio_demo_4_api.py" > /dev/null; then
        echo "$(date): Starting application..." >> $LOG_FILE
        nohup python gradio_demo_4_api.py > /opt/app-root/src/OmniParser/omniparser.log 2>&1 &
    else
        echo "$(date): Application already running" >> $LOG_FILE
    fi
}

# Start the app
start_app

# Start monitoring loop in background
(
    while true; do
        # If app not running, restart it
        if ! pgrep -f "python gradio_demo_4_api.py" > /dev/null; then
            echo "$(date): Application not running, restarting..." >> $LOG_FILE
            start_app
        fi
        sleep 60
    done
) &

# Save monitor PID to allow termination if needed
echo $! > /opt/app-root/src/OmniParser/monitor.pid
EOL

# Make the script executable
chmod +x /opt/app-root/src/OmniParser/monitor_app.sh

# Start the monitor now
/opt/app-root/src/OmniParser/monitor_app.sh

echo "Monitor started. The application will now keep running and restart automatically if it crashes."
echo "To view logs: tail -f /opt/app-root/src/OmniParser/omniparser.log"
echo "To view monitor logs: tail -f /opt/app-root/src/OmniParser/monitor.log"