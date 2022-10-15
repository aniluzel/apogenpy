import csv

import PySimpleGUI as sg

default_settings = ["sim_check = no", "url_sim = no"]


def write():
    with open('settings.csv', 'w', newline='') as f:
        # writer = csv.writer(f)
        for i in default_settings:
            f.write(i+"\n")
        f.close()
    print("write complete")


def settings_window():
    # writer.writerow("")

    layout = [[sg.T("")], [sg.T("        "), sg.Button('Save Settings', size=(20, 4), key="save_button")], [sg.T("")],
              [sg.T("                   "), sg.Checkbox('structure similarity check', default=False, key="sim_check")],
              [sg.T("                   "), sg.Checkbox('url similarity check', default=False, key="url_sim")]]



    window = sg.Window('Push my Buttons', layout, size=(300, 300))



    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == "Exit":
            break
        #True values of settings
        elif values["url_sim"] == True and values["sim_check"] == True and event == 'save_button':
            default_settings[0] = "sim_check = yes"
            default_settings[1] = "url_sim = yes"
            write()
            print("both")
        elif values["sim_check"] == True and event == 'save_button':
            default_settings[0] = "sim_check = yes"
            write()
            print("sim")
        elif values["url_sim"] == True and event == 'save_button':
            default_settings[1] = "url_sim = yes"
            write()
            print("url")
        # False values of settings
        elif values["url_sim"] == False and values["sim_check"] == False and event == 'save_button':
            default_settings[0] = "sim_check = no"
            default_settings[1] = "url_sim = no"
            write()
            print("both")
        elif values["sim_check"] == False and event == 'save_button':
            default_settings[0] = "sim_check = no"
            write()
            print("sim")
        elif values["url_sim"] == False and event == 'save_button':
            default_settings[1] = "url_sim = no"
            write()
            print("url")

    window.close()


#settings()
