import csv

import PySimpleGUI as sg



def settings():

        #writer.writerow("")


    layout = [[sg.T("")], [sg.T("        "), sg.Button('Save Settings', size=(20, 4))], [sg.T("")],
              [sg.T("                   "), sg.Checkbox('Advanced url cleaning', default=False, key="url_clean")]]

    ###Setting Window
    window = sg.Window('Push my Buttons', layout, size=(300, 200))

    ###Showing the Application, also GUI functions can be placed here.

    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == "Exit":
            break
        elif values["url_clean"] == True:
            with open('settings.csv', 'w', newline='') as f:
               # writer = csv.writer(f)
                f.write("yes")
                f.close()
            print("yes")

    window.close()


settings()