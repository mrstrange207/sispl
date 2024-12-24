import speech_recognition as sr
import json
import time
from crestron import send_command_to_crestron
import pyttsx3  # Import pyttsx3 for text-to-speech functionality

# Initialize the pyttsx3 engine for TTS
engine = pyttsx3.init()

def speak(text):
    """Function to speak out text using TTS."""
    engine.say(text)
    engine.runAndWait()

def load_commands():
    """Loads commands from the JSON file."""
    try:
        with open("commands.json", "r") as file:
            data = json.load(file)
            return data["commands"]
    except FileNotFoundError:
        return []

def save_commands(commands):
    """Saves commands to the JSON file."""
    with open("commands.json", "w") as file:
        json.dump({"commands": commands}, file, indent=4)

def listen_for_commands(commands):
    """Listen for voice commands and match them to stored actions."""
    recognizer = sr.Recognizer()
    system_awake = False
    last_command_time = time.time()  # Track time of the last command

    with sr.Microphone() as source:
        speak("Say 'Hello System' to wake up...")
        print("Say 'Hello System' to wake up...")

        while True:
            # Listen for the wake word and any subsequent commands
            audio = recognizer.listen(source)
            try:
                command = recognizer.recognize_google(audio).lower()
                print(f"You said: {command}")

                if not system_awake:
                    if "hello" in command:
                        speak("System activated! Listening for commands...")
                        print("System activated! Listening for commands...")
                        system_awake = True
                        last_command_time = time.time()  # Reset last command time
                    else:
                        speak("Wake word not detected.")
                        print("Wake word not detected.")
                else:
                    # Match against stored commands
                    command_found = False
                    for cmd in commands:
                        if cmd["command"] in command:
                            speak(f"Action triggered: {cmd['action']}")
                            print(f"Action triggered: {cmd['action']}")
                            send_command_to_crestron(cmd["action"])
                            command_found = True
                            
                            last_command_time = time.time()  # Reset last command time
                            break

                    if not command_found:
                        print("Command not recognized.")
                    
                    # Check if system should go to sleep due to inactivity (1 minute)
                    if time.time() - last_command_time > 60:
                        speak("No command recognized for 1 minute, going to sleep...")
                        print("No command recognized for 1 minute, going to sleep...")
                        system_awake = False

            except sr.UnknownValueError:
                print("Could not understand the audio.")
                
            except sr.RequestError as e:
                print(f"API error: {e}")
            except sr.WaitTimeoutError:
                print("Listening timed out, but continuing...")
                continue  # Ignore timeout and continue listening
