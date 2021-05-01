def checkServer(serverIP, port=25565):
    from mcstatus import MinecraftServer
    try:
        MinecraftServer.lookup(f"{serverIP}:{port}").ping()
        return True
    except:
        return False

def incrementIP(ip):
    if ip == "255.255.255.255":
        return "0.0.0.0"

    values = ip.split(".")
    if len(values) > 4:
        return None
    
    values[-1] = str(int(values[-1])+1)
    for num in range(4):
        if values[num-4] == "256":
            values[num-4] = "0"
            values[(num-1)-4] = str(int(values[(num-1)-4])+1)
        
    return ".".join(values)

def settingsMenu(currentSettings):
    import PySimpleGUI as sg

    sg.theme("DarkGrey2")
    layout = [
        [sg.Text("Minecraft Server Finder Settings", font=("Arial", 20))],
        [sg.Text("Made by SemegordenTheDev#6897", font=("Arial", 10))],
        [sg.Text("Starter IP: "), sg.InputText(currentSettings["startIP"], key="starterIPBox", size=(46, 1))],
        [sg.Text("End IP: "), sg.InputText(currentSettings["endIP"], key="endIPBox", size=(48, 1))],
        [sg.Text("Max Allowed Threads: "), sg.InputText(currentSettings["maxThreads"], key="maxThreadsBox", size=(10, 1))],
        [sg.Button("Submit", size=(50, 1))],
    ]
    window = sg.Window("Minecraft Server Finder Settings", layout=layout)
    while True:
        event, values = window.read()

        if event == sg.WINDOW_CLOSED:
            window.close()
            return currentSettings
    
        if event == "Submit":
            window.close()
            if int(values["maxThreadsBox"]) <= 1:
                sg.popup_error("Your max threads must be greator than or equal to 1")
            else:
                return {
                    'startIP': values["starterIPBox"],
                    'endIP': values["endIPBox"],
                    'maxThreads': values["maxThreadsBox"],
                }

def creditsmenu():
    import PySimpleGUI as sg
    import webbrowser

    sg.theme("DarkGrey2")
    layout = [
        [sg.Text("Made by SemegordenTheDev#6897", font=("Arial", 20))],
        [sg.Text("If you have any problems or ideas for an new update join my discord.", font=("Arial", 10))],
        [sg.Button("Join", size=(50, 1))]
    ]
    window =sg.Window("Made by SemegordenTheDev#6897", layout=layout)

    while True:
        event, values = window.read()

        if event == sg.WIN_CLOSED:
            break

        if event == "Join":
            window.close()
            webbrowser.open("https://discord.gg/QX6zaBMEkc")
