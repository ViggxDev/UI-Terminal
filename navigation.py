import json
import os
import subprocess

currentPath = ""

def getConfigItem(item):
    try:
        with open("config.json") as f:
            data = json.load(f)
            return data[item]
    except:
        print(f"Could not find item : {item}")

def setPathToDefault():
    global currentPath
    if currentPath != "":
        return
    currentPath = getConfigItem("defaultDirectory")

def getCurrentPath():
    return currentPath

def goBackPath():
    global currentPath
    if currentPath:
        currentPath = os.path.dirname(currentPath)

def goToPath(toAdd):
    global currentPath
    newPath = os.path.realpath(currentPath + f"/{toAdd}")
    if os.path.isdir(newPath):
        currentPath = newPath
    else:
        print(f"Directory '{toAdd}' does not exist.")
    
def openPath():
    path = os.path.realpath(currentPath)
    os.startfile(path)

def openCode():
    print(f"Opening VS Code at path: {currentPath}")

    vscode_path = r"C:\Users\viggo\AppData\Local\Programs\Microsoft VS Code\Code.exe"

    try:
        subprocess.run([vscode_path, currentPath], check=True)
    except FileNotFoundError:
        print("Error: 'code' command not found. Make sure Visual Studio Code is installed and the command is available in your PATH.")
    except subprocess.CalledProcessError as e:
        print(f"Error: The subprocess encountered an error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

#Auto fill
possibilites = []
current = 0
lastWord = ""

def autoFill(command):
    global possibilites
    global current
    global lastWord

    if not "cd" in command:
        return

    word = command[3:len(command)]

    if word != lastWord or command == "":
        possibilites = []
        current = 0

        if command == "":
            lastWord = lastWord
        else:
            lastWord = word

        dir = currentPath

        for item in os.listdir(dir):
            if os.path.isdir(os.path.join(dir, item)):
                if str.lower(item[0:len(word)]) == str.lower(word):
                    possibilites.append(item)

    if len(possibilites) >= 2:
        current += 1
        if current > len(possibilites):
            current = 0
        return possibilites[current-1]
    else:
        try:
            return possibilites[0]
        except:
            return ""