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
initialCurrentDirFontSize = 12

# UI Elements
title = tk.Label(root, text="TERMINAL", font=titleFont, bg=bgClr, fg='white')
title.pack()

error = tk.Label(root, text="", font=("Helvetica", initialCurrentDirFontSize), bg=bgClr, fg="red")
error.pack(side=tk.BOTTOM, fill=tk.X, pady=10)

commandLine = tk.Entry(root, textvariable=tk.StringVar(None), width=600)
commandLine.pack(side=tk.BOTTOM)
commandLine.focus()

currentDirectory = tk.Label(root, font=("Helvetica", initialCurrentDirFontSize), text=nav.getCurrentPath(), bg=bgClr, fg='white', pady="10px")
currentDirectory.pack(side=tk.BOTTOM, fill=tk.X)

# Create a frame for the directory contents
contentFrame = tk.Frame(root)
contentFrame.pack(fill=tk.BOTH, expand=True)

# Add a canvas to the content frame
canvas = tk.Canvas(contentFrame, bg=bgClr, highlightthickness=0)
canvas.pack(fill=tk.BOTH, expand=True)

# Create a frame inside the canvas to hold the directory items
scrollable_frame = tk.Frame(canvas, bg=bgClr)
window = canvas.create_window((0, 0), window=scrollable_frame, anchor="center")
canvas.itemconfig(window, anchor="center")

# Update the scroll region whenever the size of the frame changes
def onFrameConfigure(event=None):
    canvas.configure(scrollregion=canvas.bbox("all"))
    canvas.itemconfig(window, anchor="center")

scrollable_frame.bind("<Configure>", onFrameConfigure)

# Functions
def adjustFontSize(label, text, initialFontSize):
    currentFontSize = initialFontSize
    label.config(font=("Helvetica", currentFontSize))
    label.update_idletasks()  # Make sure label's geometry is updated

    while label.winfo_reqwidth() > label.winfo_width() and currentFontSize > 6:
        currentFontSize -= 1
        label.config(font=("Helvetica", currentFontSize))
        label.update_idletasks()  # Update geometry after changing font size

def updateCurrentDir():
    current_path = nav.getCurrentPath()
    currentDirectory.config(text=current_path)
    adjustFontSize(currentDirectory, current_path, initialCurrentDirFontSize)

def displayDirectoryContents():
    global loopUpdate

    # Clear the current contents of the scrollable frame
    for widget in scrollable_frame.winfo_children():
        widget.destroy()

    # List the contents of the current directory
    current_path = nav.getCurrentPath()
    for item in os.listdir(current_path):
        item_label = tk.Label(scrollable_frame, text=item, font=("Helvetica", initialCurrentDirFontSize), bg=bgClr, fg='white')
        item_label.pack(fill=tk.BOTH, expand=True)
        item_label.pack_configure(anchor="center")

    # Ensure the scrollable_frame width matches the canvas width
    scrollable_frame.update_idletasks()
    canvas.config(scrollregion=canvas.bbox("all"))
    canvas_width = canvas.winfo_width()
    scrollable_frame.config(width=canvas_width)

    # Recenter the window
    canvas.itemconfig(window, anchor="center")

    if loopUpdate:
        loopUpdate = False
        root.after(100, displayDirectoryContents)

root.after_idle(displayDirectoryContents)
updateCurrentDir()

def _on_mouse_wheel(event):
    canvas.yview_scroll(-1 * (event.delta // 120), "units")

# Bind mouse wheel events to the canvas
canvas.bind_all("<MouseWheel>", _on_mouse_wheel)

# Run wanted command
def runCommand(command):
    error.configure(text="")
    if len(command) <= 0:
        return
    if command == "cd .." or command == "cd..":
        nav.goBackPath()
    elif "cd" in command:
        r = nav.goToPath(command[3:])
        if r == False:
            error.configure(text="PATH NOT FOUND!")
    elif command == "start .":
        nav.openPath()
    elif command == "code .":
        r = nav.openCode()
        error.configure(text=r)
    elif command == "home:":
        nav.setPathToDefault(True)
    else:
        error.configure(text="COMMAND NOT FOUND!")
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
            commandLine.icursor(tk.END)
        else:
            lastKeyPress = "Tab"
            newWord = f'cd {nav.autoFill(commandLine.get())}'
            commandLine.delete(0, tk.END)
            commandLine.insert(0, newWord)
            commandLine.icursor(tk.END)
    else:
        lastKeyPress = key

root.bind('<KeyPress>', keyPress)

root.mainloop()
