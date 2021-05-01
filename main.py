import threading
import PySimpleGUI as sg
from utils import checkServer, incrementIP, settingsMenu, creditsmenu

settings = {'startIP': '1.1.1.1', 'endIP': '255.255.255.255', 'maxThreads': '500'}

global updateScreen
updateScreen = False
global validServers
validServers = []

def checkThread(ipA):
    global validServers
    global updateScreen

    if checkServer(ipA):
        validServers.append(ipA)
        updateScreen = True

sg.theme("DarkGrey2")
layout = [
    [sg.Text("Minecraft Server Finder", font=("Arial", 25))],
    [sg.Multiline(size=(50, 20), disabled=True, key="validDisplay")],
    [sg.Button("Start", size=(46, 1))],
    [sg.Button("Pause", size=(46, 1), disabled=True)],
    [sg.Button("Stop", size=(46, 1), disabled=True)],
    [sg.Button("Settings", size=(46, 1))],
    [sg.Button("Credits", size=(46, 1))],
    [sg.Text("Status: Idle", size=(48, 1), key="statusText")],
]
window = sg.Window("Minecraft Server Finder", layout=layout)

searchActive = False
paused = False

while True:
    event, values = window.read(timeout=0)

    if event == sg.WINDOW_CLOSED:
        break

    if event == "Credits":
        credits = creditsmenu()

    if event == "Settings":
        settings = settingsMenu(settings)

    if event == "Start":
        window["statusText"].Update("Status: Searching...")
        if not paused:
            ipA = settings["startIP"]
            validServers = []
        searchActive = True
        paused = False
        window["Start"].Update(disabled=True)
        window["Pause"].Update(disabled=False)
        window["Stop"].Update(disabled=False)
        window["Settings"].Update(disabled=True)
        window["validDisplay"].Update("\n".join(validServers))
    
    if event == "Pause":
        window["statusText"].Update("Status: Paused..." + ipA)
        searchActive = False
        paused = True
        window["Start"].Update(disabled=False)
        window["Pause"].Update(disabled=True)
        window["Stop"].Update(disabled=False)
    
    if event == "Stop":
        if sg.popup_yes_no("Warning, stoping the search will delete all current progress!\nAre you sure you want to stop searching?") == "Yes":
            window["statusText"].Update("Status: Idle")
            searchActive = False
            paused = False
            window["Start"].Update(disabled=False)
            window["Pause"].Update(disabled=True)
            window["Stop"].Update(disabled=True)
            window["Settings"].Update(disabled=False)
    
    if paused:
        window["statusText"].Update("Status: Paused..." + ipA + " | Active Threads: " + str(threading.active_count()-1))
    
    if updateScreen:
        window["validDisplay"].Update("\n".join(validServers))
        updateScreen = False

    if searchActive:
        try:
            if threading.active_count()-1 < int(settings["maxThreads"])+1:
                ipATMP = incrementIP(ipA)
                window["statusText"].Update("Status: Searching... " + ipA + " | Active Threads: " + str(threading.active_count()-1))
                threading.Thread(target=checkThread, args=(ipA,)).start()
                ipA = ipATMP
        except RuntimeError:
            pass

        if ipA == settings["endIP"]:
            window["statusText"].Update("Status: Search complete")
            searchActive = False
            paused = False
            window["Start"].Update(disabled=False)
            window["Pause"].Update(disabled=True)
            window["Stop"].Update(disabled=True)
            window["Settings"].Update(disabled=False)
