import socket

# Crestron IP and Port (Replace with actual values)
CRESTRON_IP = "192.168.1.10"  # Replace with the CP4's IP address
CRESTRON_PORT = 50000  # Default TCP/IP port, change if necessary

def send_command_to_crestron(command):
    """Sends a command to the Crestron CP4 processor via TCP/IP."""
    try:
        # Create a socket connection
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((CRESTRON_IP, CRESTRON_PORT))
            print(f"Sending command to Crestron: {command}")
            s.sendall(command.encode('utf-8'))  # Send the command as bytes
            s.close()
            print("Command sent successfully.")
    except Exception as e:
        print(f"Error sending command to Crestron: {e}")
