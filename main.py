import tkinter as tk
import os
import navigation as nav

# Initial variables
loopUpdate = True

# Set default directory
nav.setPathToDefault()

# Initialize tkinter and set default properties
root = tk.Tk()
root.geometry("800x600")
bgClr = '#1a1a1a'
root.configure(bg=bgClr)

# Fonts
titleFont = ("Helvetica", 24)
currentDirFont = ("Helvetica", 12)

# UI Elements
title = tk.Label(root, text="TERMINAL", font=titleFont, bg=bgClr, fg='white')
title.pack()

commandLine = tk.Entry(root, textvariable=tk.StringVar(None), width=700)
commandLine.pack(side=tk.BOTTOM, pady=20)

currentDirectory = tk.Label(root, font=currentDirFont, text=nav.getCurrentPath(), bg=bgClr, fg='white', pady="10px")
currentDirectory.pack(side=tk.BOTTOM)

# Create a frame for the directory contents
contentFrame = tk.Frame(root)
contentFrame.pack(fill=tk.BOTH, expand=True)

# Add a canvas to the content frame
canvas = tk.Canvas(contentFrame, bg=bgClr, highlightthickness=0)
canvas.pack(fill=tk.BOTH, expand=True)

# Create a frame inside the canvas to hold the directory items
scrollable_frame = tk.Frame(canvas, bg=bgClr)
window = canvas.create_window((0, 0), window=scrollable_frame, anchor="center")
canvas.itemconfig(window, anchor="center")  # Add this line

# Update the scroll region whenever the size of the frame changes
def onFrameConfigure(event=None):
    canvas.configure(scrollregion=canvas.bbox("all"))
    canvas.itemconfig(window, anchor="center")  # Move this line here

scrollable_frame.bind("<Configure>", onFrameConfigure)

# Functions
def updateCurrentDir():
    currentDirectory.config(text=nav.getCurrentPath())

def displayDirectoryContents():
    global loopUpdate

    # Clear the current contents of the scrollable frame
    for widget in scrollable_frame.winfo_children():
        widget.destroy()

    # List the contents of the current directory
    current_path = nav.getCurrentPath()
    for item in os.listdir(current_path):
        item_label = tk.Label(scrollable_frame, text=item, font=currentDirFont, bg=bgClr, fg='white')
        item_label.pack(fill=tk.BOTH, expand=True)  # Pack with expand=True

        # Center the label after it's packed
        item_label.pack_configure(anchor="center")

    # Ensure the scrollable_frame width matches the canvas width
    scrollable_frame.update_idletasks()
    canvas.config(scrollregion=canvas.bbox("all"))
    canvas_width = canvas.winfo_width()
    scrollable_frame.config(width=canvas_width)

    # Recenter the window
    canvas.itemconfig(window, anchor="center")

    # Set anchor for the window after configuring canvas
    canvas.itemconfig(window, anchor="center")

    if loopUpdate == True:
        loopUpdate = False
        root.after(100, displayDirectoryContents)

root.after_idle(displayDirectoryContents)

def _on_mouse_wheel(event):
    canvas.yview_scroll(-1 * (event.delta // 120), "units")

# Bind mouse wheel events to the canvas
canvas.bind_all("<MouseWheel>", _on_mouse_wheel)

# Run wanted command
def runCommand(command):
    if len(command) <= 0:
        return
    if command == "cd .." or command == "cd..":
        nav.goBackPath()
    elif "cd" in command:
        nav.goToPath(command[3:])
    elif command == "start .":
        nav.openPath()
    elif command == "code .":
        print("Code")
    else:
        print('Command not found!')
    updateCurrentDir()
    displayDirectoryContents()

# Detect Key presses

lastKeyPress = ""

def keyPress(event):
    global lastKeyPress

    key = event.keysym
    if key == "Return":
        runCommand(commandLine.get())
        commandLine.delete(0, tk.END)
    elif key == "Tab":
        if lastKeyPress == "Tab":
            newWord = f'cd {nav.autoFill("cd")}'
            commandLine.delete(0, tk.END)
            commandLine.insert(0, newWord)
        else:
            lastKeyPress = "Tab"
            newWord = f'cd {nav.autoFill(commandLine.get())}'
            commandLine.delete(0, tk.END)
            commandLine.insert(0, newWord)
    else:
        lastKeyPress = key

root.bind('<KeyPress>', keyPress)

root.mainloop()
