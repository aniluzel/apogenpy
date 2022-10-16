# main_gui.py, table_test.py ve settings.py bu sayfada olacak
# GUI ile alakalı bütün elementler bu sayfada
import csv
import DEMO
import FILE_GEN
import PySimpleGUI as sg
import crawl

def gui_run(check_sim, check_url_sim):
    print("gui_run test")
    sg.theme('Dark Blue')  # Add a touch of color
    # All the stuff inside your window.
    layout = [[sg.Text('Past link below that you want to crawl')],
              [sg.Text('Crawl domain'), sg.InputText()],
              [sg.Button('Crawl'), sg.Button('exit')], [sg.Button('Settings')]]
    # settings
    # Create the Window
    window = sg.Window('ApogenPy', layout, size=(600, 250))

    #   Event Loop to process "events" and get the "values" of the inputs
    while True:
        event, values = window.read()
        if event == 'Crawl':
            # print("here")

            # def run():
            #     while True:
            #         print('thread running')
            #         loading_window.loading_win()
            #         global stop_threads
            #         if stop_threads:
            #             break

            def image_loading():
                global flag
                flag = True
                while flag:
                    sg.popup_animated(sg.DEFAULT_BASE64_LOADING_GIF, no_titlebar=True)

                sg.PopupAnimated(image_source=None)



            # find all cites
            c = crawl.CrawlerProcess({})
            c.crawl(crawl.CrawlingSpider, start_urls=[values[0]])
            c.start()

            # filtering function
            filtered_data =crawl.sim_check(data=crawl.crawled_links,check_sim=check_sim,check_url_sim=check_url_sim)

            # close window before entering new
            window.close()

            # next window
            open_table_window(filtered_data)
        elif event == 'Settings':
            settings_window()


        elif event == sg.WIN_CLOSED or event == 'exit':  # if user closes window or clicks cancel
            window.close()
            break
        # print(values[0])

    window.close()


default_settings = ["sim_check = no", "url_sim = no"]

#used to write settings
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



    window = sg.Window('Settings', layout, size=(300, 300))



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





def open_table_window(filtered):
    sg.theme('Dark Blue')
    # readfiltered to array



    def value_to_nums(val):

        tmp = val["-TABLE-"]
        return tmp

    def make_table(num_rows, num_cols):
        data = [[j for j in range(num_cols)] for i in range(num_rows)]
        for i in range(len(filtered)):
            data[i] = [filtered[i]]

        # for i in range(len(array)):
        #     print(array[0][i],"asfdasdf")
        #     data[i] = [array[0][i]]

        return data

    # ------ Make the Table Data ------
    table_size = len(filtered)
    #print(len(array[0]))
    if table_size > 15:
        table_size = 15

    data = make_table(num_rows=table_size, num_cols=1)
    headings = ["                    Crawled links     "]

    # ------ Window Layout ------
    layout = [[sg.Table(values=data[0:][:], headings=headings, max_col_width=500,
                        # background_color='light blue',
                        auto_size_columns=True,
                        display_row_numbers=True,
                        justification='right',
                        num_rows=table_size,
                        alternating_row_color='#000020',
                        select_mode=sg.TABLE_SELECT_MODE_EXTENDED,
                        enable_events=True,
                        key='-TABLE-',
                        col_widths=400,
                        row_height=35,
                        tooltip='This is a table')],[sg.Text('Additional url here'), sg.InputText(key='url'),sg.Button('Add url')],
              [sg.Button('Continue with all'), sg.Button('Continue with selected')],
              [sg.Text('Add url = Adds url to the list')],
              [sg.Text('Continue with all = generate files with all available urls')],
              [sg.Text('Continue with selected = generate files with selected urls')]]

    # ------ Create Window ------
    window = sg.Window('ApogenPy', layout, finalize=True, size=(600, 500)
                       # font='Helvetica 25',
                       )
    table = window['-TABLE-']
    # ------ Event Loop ------

    user_click = True
    selected = []
    added_links_array = []
    while True:
        event, values = window.read()
        #print(event, values,"fasdfasdf")
        if event == sg.WIN_CLOSED:
            break
            window['-TABLE-'].update(values=data)
        elif event == 'Continue with all':
            for i in data:
                print("breakpoint ", i[0])
                DEMO.demo_fun(i[0])
                FILE_GEN.gen(i[0])
                print("func called", i)
        # add button func
        elif event == 'Continue with selected':
            needed = value_to_nums(values)
            for i in needed:
                #added_links_array.append(array[0][i])
                print("needed",data[i][0])
                DEMO.demo_fun(data[i][0])

                FILE_GEN.gen(data[i][0])
            print("func called")
        #adds url to current set
        elif event == 'Add url':
           # print(data[0])
            data.append([values['url']])
            #print(data)
            window['-TABLE-'].update(values=data)
            #print("url appended", values['url'])

        #table click stuff
        elif event == '-TABLE-':
            if user_click:
                if len(values['-TABLE-']) == 1:
                    select = values['-TABLE-'][0]
                    if select in selected:
                        selected.remove(select)
                    else:
                        selected.append(select)
                    table.update(select_rows=selected)
                    user_click = False
            else:
                user_click = True

    window.close()