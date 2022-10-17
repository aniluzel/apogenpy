import PySimpleGUI as sg
import crawl
import pomgen


def gui_run(check_sim, check_url_sim):
    sg.theme('Dark Blue')
    layout = [[sg.Text('Enter the URL of a domain that you want to crawl')],
              [sg.Text('URL'), sg.InputText()],
              [sg.Button('Crawl'), sg.Button('Exit')], [sg.Button('Settings')]]
    window = sg.Window('ApogenPy', layout, size=(600, 250))

    while True:
        event, values = window.read()
        if event == 'Crawl':
            def image_loading():
                global flag
                flag = True
                while flag:
                    sg.popup_animated(sg.DEFAULT_BASE64_LOADING_GIF, no_titlebar=True)

                sg.PopupAnimated(image_source=None)

            c = crawl.CrawlerProcess({})
            c.crawl(crawl.CrawlingSpider, start_urls=[values[0]])
            c.start()

            filtered_data = crawl.sim_check(data=crawl.crawled_links, check_sim=check_sim, check_url_sim=check_url_sim)

            window.close()

            open_table_window(filtered_data)
        elif event == 'Settings':
            settings_window()

        elif event == sg.WIN_CLOSED or event == 'Exit':
            window.close()
            break

    window.close()


default_settings = ["sim_check = no", "url_sim = no"]


def settings_window():
    layout = [[sg.T("")], [sg.T("        "), sg.Button('Save Settings', size=(20, 4), key="save_button")], [sg.T("")],
              [sg.T("                   "), sg.Checkbox('Structure Similarity Check', default=False, key="sim_check")],
              [sg.T("                   "), sg.Checkbox('URL Similarity Check', default=False, key="url_sim")]]

    window = sg.Window('Settings', layout, size=(300, 300))

    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == "Exit":
            break
        # True values of settings
        elif values["url_sim"] and values["sim_check"] and event == 'save_button':
            default_settings[0] = "sim_check = yes"
            default_settings[1] = "url_sim = yes"
        elif values["sim_check"] and event == 'save_button':
            default_settings[0] = "sim_check = yes"
        elif values["url_sim"] and event == 'save_button':
            default_settings[1] = "url_sim = yes"
        # False values of settings
        elif not values["url_sim"] and not values["sim_check"] and event == 'save_button':
            default_settings[0] = "sim_check = no"
            default_settings[1] = "url_sim = no"
        elif not values["sim_check"] and event == 'save_button':
            default_settings[0] = "sim_check = no"
        elif not values["url_sim"] and event == 'save_button':
            default_settings[1] = "url_sim = no"

    window.close()


def open_table_window(filtered):
    sg.theme('Dark Blue')

    def value_to_nums(val):
        tmp = val["-TABLE-"]
        return tmp

    def make_table(num_rows, num_cols):
        data = [[j for j in range(num_cols)] for i in range(num_rows)]
        for i in range(len(filtered)):
            data[i] = [filtered[i]]

        return data

    table_size = len(filtered)
    if table_size > 15:
        table_size = 15

    data = make_table(num_rows=table_size, num_cols=1)
    headings = ["                    Crawled Links     "]

    layout = [[sg.Table(values=data[0:][:], headings=headings, max_col_width=500,
                        auto_size_columns=True,
                        display_row_numbers=True,
                        justification='right',
                        num_rows=table_size,
                        alternating_row_color='#000020',
                        select_mode=sg.TABLE_SELECT_MODE_EXTENDED,
                        enable_events=True,
                        key='-TABLE-',
                        col_widths=400,
                        row_height=35)],
              [sg.Text('Additional URL'), sg.InputText(key='url'), sg.Button('Add URL')],
              [sg.Button('Continue with All'), sg.Button('Continue with Selected')],
              [sg.Text('Add URL = Adds a new domain to the list')],
              [sg.Text('Continue with All = Generate files with all available URLs')],
              [sg.Text('Continue with Selected = Generate files with selected URLs')]]

    window = sg.Window('ApogenPy', layout, finalize=True, size=(520, 530))
    table = window['-TABLE-']

    user_click = True
    selected = []
    added_links_array = []
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED:
            break
            window['-TABLE-'].update(values=data)
        elif event == 'Continue with All':
            for i in data:
                # DEMO.demo_fun(i[0])
                pomgen.file_gen(i[0])

        elif event == 'Continue with Selected':
            needed = value_to_nums(values)
            for i in needed:
                # added_links_array.append(array[0][i])
                # DEMO.demo_fun(data[i][0]
                pomgen.file_gen(data[i][0])

        # adds url to current set
        elif event == 'Add URL':
            # print(data[0])
            data.append([values['url']])
            # print(data)
            window['-TABLE-'].update(values=data)
            # print("url appended", values['url'])

        # table click stuff
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
