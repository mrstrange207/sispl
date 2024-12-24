import tkinter as tk
from tkinter import messagebox
from voice import load_commands, save_commands

def refresh_command_list(listbox):
    """Refresh the Listbox to show the current commands."""
    listbox.delete(0, tk.END)  # Clear existing list
    commands = load_commands()  # Load commands from JSON
    for cmd in commands:
        listbox.insert(tk.END, f"{cmd['command']} - Action: {cmd['action']}")

def add_command(listbox, command_entry, action_entry):
    """Add a new command to the list and save it to the JSON file."""
    command = command_entry.get()
    action = action_entry.get()

    if command and action:
        commands = load_commands()
        commands.append({"command": command, "action": action})
        save_commands(commands)

        refresh_command_list(listbox)  # Refresh the listbox to show the new command
        command_entry.delete(0, tk.END)  # Clear the input fields
        action_entry.delete(0, tk.END)
        messagebox.showinfo("Success", "Command added successfully.")
    else:
        messagebox.showwarning("Input Error", "Please enter both command and action.")

def remove_command(listbox):
    """Remove the selected command from the list and update the JSON file."""
    selected = listbox.curselection()
    if selected:
        command_text = listbox.get(selected[0])
        command = command_text.split(" - ")[0]
        
        commands = load_commands()
        commands = [cmd for cmd in commands if cmd["command"] != command]
        save_commands(commands)

        refresh_command_list(listbox)  # Refresh the listbox to remove the command
        messagebox.showinfo("Success", f"Command '{command}' removed successfully.")
    else:
        messagebox.showwarning("Selection Error", "Please select a command to remove.")

def start_gui():
    """Start the GUI to add/remove voice commands."""
    root = tk.Tk()
    root.title("Voice Command Manager")

    # Command List Section
    listbox_frame = tk.Frame(root)
    listbox_frame.pack(pady=10)

    listbox_label = tk.Label(listbox_frame, text="Stored Commands:")
    listbox_label.pack()

    listbox = tk.Listbox(listbox_frame, width=50, height=10, selectmode=tk.SINGLE)
    listbox.pack()

    refresh_command_list(listbox)  # Populate listbox with existing commands

    # Add Command Section
    add_frame = tk.Frame(root)
    add_frame.pack(pady=10)

    command_label = tk.Label(add_frame, text="Enter Command:")
    command_label.grid(row=0, column=0, padx=10)

    command_entry = tk.Entry(add_frame, width=30)
    command_entry.grid(row=0, column=1, padx=10)

    action_label = tk.Label(add_frame, text="Enter Action:")
    action_label.grid(row=1, column=0, padx=10)

    action_entry = tk.Entry(add_frame, width=30)
    action_entry.grid(row=1, column=1, padx=10)

    add_button = tk.Button(add_frame, text="Add Command", command=lambda: add_command(listbox, command_entry, action_entry))
    add_button.grid(row=2, columnspan=2, pady=10)

    # Remove Command Section
    remove_button = tk.Button(root, text="Remove Selected Command", command=lambda: remove_command(listbox))
    remove_button.pack(pady=10)

    root.mainloop()

