import threading
import time
from gui import start_gui
from voice import listen_for_commands, load_commands

def run_voice_command_recognition():
    """Start voice command recognition in a separate thread."""
    commands = load_commands()  # Load commands from JSON
    listen_for_commands(commands)

def main():
    # Start the GUI in a separate thread
    gui_thread = threading.Thread(target=start_gui)
    gui_thread.start()

    # Give some time for the GUI to start
    time.sleep(1)

    # Start voice command recognition
    run_voice_command_recognition()

if __name__ == "__main__":
    main()
