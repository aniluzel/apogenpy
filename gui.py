import PySimpleGUI as sg
import crawl
import pomgen


def gui_run():
    sg.theme('Dark Blue')
    layout = [[sg.Text('Enter the URL of a domain that you want to crawl')],
              [sg.Text('URL'), sg.InputText()],
              [sg.Button('Crawl'), sg.Button('Exit')], [sg.Button('Settings')]]
    window = sg.Window('ApogenPy', layout, size=(600, 250))

    while True:
        event, values = window.read()
        if event == 'Crawl':
            filtered_data = []


            print(filtered_data)
            #close current window
            window.close()
            #open table window
            open_table_window(loading_crawl(values[0]))

        elif event == 'Settings':
            settings_window()

        elif event == sg.WIN_CLOSED or event == 'Exit':
            window.close()
            break

    window.close()


# default loaded settings
default_settings = [True, False, "Structural similarity",0.92,0.88,None]


def settings_window():
    layout = [[sg.T("")], [sg.T("        "), sg.Button('Save Settings', size=(20, 4), key="save_button")], [sg.T("")],
              [sg.T("                   "),
               sg.Checkbox('Structure Similarity Check', default=default_settings[0], key="sim_check")],
              [sg.T("                   "),
               sg.Checkbox('URL Similarity Check', default=default_settings[1], key="url_sim")],[sg.T("Similarity percentage value"),sg.InputText("",key="sim_input")],[sg.T("Url Similarity percentage value"),sg.InputText("",key="url_input")],[sg.T("Enter domain "),sg.InputText("",key="domain_input")],
              [sg.T("Choose Similarity"),
               sg.OptionMenu(["Joint similarity", "Structural similarity", "Style similarity"],
                             default_value=default_settings[2], key='sim_type')]]

    window = sg.Window('Settings', layout, size=(300, 300))

    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == "Exit":
            break
        # True values of settings
        elif event == 'save_button':
            default_settings[0] = values["sim_check"]
            default_settings[1] = values["url_sim"]
            default_settings[2] = values["sim_type"]
            default_settings[3] = values["sim_input"]
            default_settings[4] = values["url_input"]
            default_settings[5] = values["domain_input"]
            #print(default_settings)
            window.close()

    window.close()


def loading_crawl(val):
    layout = [[sg.T("Crawling", key="crawl_text")], [sg.ProgressBar(100, orientation='h', k="loading_bar")]]

    window = sg.Window('Loading', layout, finalize=True, size=(300, 300))

    window['loading_bar'].update(10)
    # crawling
    c = crawl.CrawlerProcess({})
    c.crawl(crawl.CrawlingSpider, start_urls=[val],allowed_domains=default_settings[5])
    c.start()
    window['loading_bar'].update(50)
    window['crawl_text'].update("Similarity Check")
    # filtering
    print(default_settings[3],"def")
    filtered_data = crawl.sim_check(data=crawl.crawled_links, check_sim=default_settings[0],
                                    check_url_sim=default_settings[1], param=default_settings[2],web_page_similarity_percentage=default_settings[3],web_path_similarity_percentage=default_settings[4])
    print(filtered_data)
    window['loading_bar'].update(100)
    window.close()

    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == "Exit":
            break
        # True values of settings

    return filtered_data
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
