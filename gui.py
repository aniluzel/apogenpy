import PySimpleGUI as sg
import crawl
import pomgen
import sys
from PyQt5.QtWidgets import QMainWindow,QWidget,QApplication
from PyQt5.QtWebEngineWidgets import QWebEngineView as QWebView
from PyQt5.QtCore import QUrl
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *


default_settings = [True, False, "Structural similarity", 0.92, 0.88, None]
def gui_run():
    def table_data(filtered):
        sg.theme('Dark Blue')

        def make_table(num_rows, num_cols):
            data = [[j for j in range(num_cols)] for i in range(num_rows)]
            for i in range(len(filtered)):
                data[i] = [filtered[i]]

            return data

        table_size = len(filtered)
        if table_size > 15:
            table_size = 15

        data = make_table(num_rows=table_size, num_cols=1)
        return data

    def value_to_nums(val):
        tmp = val["-TABLE-"]
        return tmp

    def loading_crawl(val):
        layout = [[sg.T("Crawling", key="crawl_text")], [sg.ProgressBar(100, orientation='h', k="loading_bar")]]

        window = sg.Window('Loading', layout, finalize=True, size=(300, 300))

        window['loading_bar'].update(10)
        # crawling
        c = crawl.CrawlerProcess({})
        c.crawl(crawl.CrawlingSpider, start_urls=[val], allowed_domains=default_settings[5])
        c.start()
        window['loading_bar'].update(50)
        window['crawl_text'].update("Similarity Check")
        # filtering
        filtered_data = crawl.sim_check(data=crawl.crawled_links, check_sim=default_settings[0],
                                        check_url_sim=default_settings[1], param=default_settings[2],
                                        web_page_similarity_percentage=default_settings[3],
                                        web_path_similarity_percentage=default_settings[4])
        #print(filtered_data)
        window['loading_bar'].update(100)
        window.close()

        while True:
            event, values = window.read()
            if event == sg.WIN_CLOSED or event == "Exit":
                break
            # True values of settings

        return filtered_data
        window.close()


    # ----------- Create the 3 layouts this Window will display -----------
    start_layout = [[sg.Text('Enter the URL of a domain that you want to crawl')],
                    [sg.Text('URL'), sg.InputText()],
                    [sg.Button('Crawl'), sg.Button('Exit')], [sg.Button('Settings')]]

    # table stuff
    filtered = []

    data = table_data(filtered)
    headings = ["                    Crawled Links     "]
    table_layout = [[sg.Table(values=data[0:][:], headings=headings, max_col_width=500,
                              auto_size_columns=True,
                              display_row_numbers=True,
                              justification='right',
                              num_rows=10,
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
    # table stuf end

    settings_layout = [[sg.T("")], [sg.T("        "), sg.Button('Save Settings', size=(20, 4), key="save_button")],
                       [sg.T("")],
                       [sg.T("                   "),
                        sg.Checkbox('Structure Similarity Check', default=default_settings[0], key="sim_check")],
                       [sg.T("                   "),
                        sg.Checkbox('URL Similarity Check', default=default_settings[1], key="url_sim")],
                       [sg.T("Similarity percentage value"), sg.InputText("", key="sim_input")],
                       [sg.T("Url Similarity percentage value"), sg.InputText("", key="url_input")],
                       [sg.T("Enter domain "), sg.InputText("", key="domain_input")],
                       [sg.T("Choose Similarity"),
                        sg.OptionMenu(["Joint similarity", "Structural similarity", "Style similarity"],
                                      default_value=default_settings[2], key='sim_type')]]

    # ----------- Create actual layout using Columns and a row of Buttons
    layout = [[sg.Column(start_layout, key='-COL1-'), sg.Column(settings_layout, visible=False, key='-COL2-'),
               sg.Column(table_layout, visible=False, key='-COL3-')]]

    window = sg.Window('Swapping the contents of a window', layout)
    table = window['-TABLE-']
    user_click = True
    selected = []
    layout = 1  # The currently visible layout
    while True:
        event, values = window.read()
        print(event, values)
        if event in (sg.WIN_CLOSED, 'Exit'):
            break
        elif event == 'Crawl':

            window[f'-COL1-'].update(visible=False)
            filtered_data = loading_crawl(values[0])
            data = table_data(filtered_data)
            window['-TABLE-'].update(values=data)
            window[f'-COL3-'].update(visible=True)

        elif event == 'Settings':
            window[f'-COL1-'].update(visible=False)
            window[f'-COL2-'].update(visible=True)
        elif event == 'save_button':
            default_settings[0] = values["sim_check"]
            default_settings[1] = values["url_sim"]
            default_settings[2] = values["sim_type"]
            if values["sim_input"] != '':
                default_settings[3] = values["sim_input"]
            if values["url_input"] != '':
                default_settings[4] = values["url_input"]
            default_settings[5] = values["domain_input"]
            # print(default_settings)
            window[f'-COL2-'].update(visible=False)
            window[f'-COL1-'].update(visible=True)
            sg.popup_auto_close("Saved", auto_close_duration=1, no_titlebar=True)

        elif event == 'Continue with All':
            tmp = []
            for i in data:
                tmp.append(i[0])
                # DEMO.demo_fun(i[0])

                #web stuf
            print("data =" ,data)
            window.close()
            web_list(tmp)


                #pomgen.file_gen(i[0])

        elif event == 'Continue with Selected':
            needed = value_to_nums(values)
            print("needed = ",needed)
            selected_urls =[]
            for i in needed:
                selected_urls.append(data[i][0])

                # added_links_array.append(array[0][i])
                # DEMO.demo_fun(data[i][0]

                #add data later
                #print("selected urls = ",selected_urls)
            window.close()
            web_list(selected_urls)

                #pomgen.file_gen(data[i][0],pomgen.elemfinder(data[i][0]))

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
        elif event == sg.WIN_CLOSED or event == 'Exit':
            window.close()
            break
    window.close()



#web page and list function
class ListWidget(QListWidget):
    def clicked(self, item):
        #when clicked element selected higlight form html code
        QMessageBox.information(self, "ListWidget", "ListWidget: " + item.text())


# array with elment that are needed for web testing here
def add_item_windget(windget, data):
    for i in data:
        windget.addItem(i)


def get_url_from_web_view(web_view):
    return web_view.url().toString()

#temp data for list
data_tmp = ["Item 1","Item 2","Item 3","item 4"]

def update_counter(val):
    global counter
    counter = val
    return counter


#counter = 0
def on_click(web,button,url,listWidget,counter):

    if counter == len(url) - 1:
        button.hide()
    else:
        counter += 1
        web.load(QUrl(url[counter]))
        data = pomgen.idfinder(url[counter])
        listWidget.clear()
        for i in data:
            listWidget.addItem(i)
            listWidget.repaint()
    #print("next button clicked")
    update_counter(counter)
def web_list(url):
    global counter
    counter = 0

    app = QApplication(sys.argv)
    listWidget = QListWidget()
    mainWindow = QMainWindow()
    widget = QWidget()
    web = QWebView()
    web.load(QUrl(url[counter]))
    data = pomgen.idfinder(url[counter])
    next_button = QPushButton('Next page')
    generate_button = QPushButton('Generate for selected')
    gen_all_button = QPushButton('Generate all for this page')

    next_button.clicked.connect(lambda: on_click(web,next_button,url,listWidget,counter))
    generate_button.clicked.connect(generate_button_clicked)
    gen_all_button.clicked.connect(lambda: gen_all_button_cliked(url[counter]))

    #print(get_url_from_web_view(web))
    main_layout = QHBoxLayout()
    but_list_layout = QVBoxLayout()
    but_list_layout.addWidget(listWidget)
    but_list_layout.addWidget(next_button)
    but_list_layout.addWidget(generate_button)
    but_list_layout.addWidget(gen_all_button)

    main_layout.addWidget(web)

    listWidget.resize(300, 120)
    add_item_windget(listWidget, data)
    listWidget.setSelectionMode(QAbstractItemView.MultiSelection)
    listWidget.setVerticalScrollMode(QAbstractItemView.ScrollPerPixel)
    #listWidget.itemClicked.connect(listWidget.clicked)
    listWidget.itemClicked.connect(lambda: printItemText(listWidget))

    #hor_Layout.addWidget(listWidget)
    #hor_Layout.addWidget(button)
    main_layout.addLayout(but_list_layout)
    mainWindow.resize(1000,800)
    widget.setLayout(main_layout)
    mainWindow.setCentralWidget(widget)
    mainWindow.setWindowTitle("Apogenpy")

    mainWindow.show()
    sys.exit(app.exec_())

def printItemText(listWidget):
        items = listWidget.selectedItems()
        global selected
        selected = []
        for i in range(len(items)):
            selected.append(str(listWidget.selectedItems()[i].text()))


def generate_button_clicked():
    global selected
    for item in selected:
        # genrete
        print("generated for ",item)

def gen_all_button_cliked(data):
    #data takes url
    for i in data:
        #genrate
        print(i)


#old gui
# def gui_run():
#     sg.theme('Dark Blue')
#     layout = [[sg.Text('Enter the URL of a domain that you want to crawl')],
#               [sg.Text('URL'), sg.InputText()],
#               [sg.Button('Crawl'), sg.Button('Exit')], [sg.Button('Settings')]]
#     window = sg.Window('ApogenPy', layout, size=(600, 250))
#
#     while True:
#         event, values = window.read()
#         if event == 'Crawl':
#             filtered_data = []
#
#
#             print(filtered_data)
#             #close current window
#             window.close()
#             #open table window
#             open_table_window(loading_crawl(values[0]))
#
#         elif event == 'Settings':
#             settings_window()
#
#         elif event == sg.WIN_CLOSED or event == 'Exit':
#             window.close()
#             break
#
#     window.close()
#
#
# # default loaded settings
# default_settings = [True, False, "Structural similarity",0.92,0.88,None]
#
#
# def settings_window():
#     layout = [[sg.T("")], [sg.T("        "), sg.Button('Save Settings', size=(20, 4), key="save_button")], [sg.T("")],
#               [sg.T("                   "),
#                sg.Checkbox('Structure Similarity Check', default=default_settings[0], key="sim_check")],
#               [sg.T("                   "),
#                sg.Checkbox('URL Similarity Check', default=default_settings[1], key="url_sim")],[sg.T("Similarity percentage value"),sg.InputText("",key="sim_input")],[sg.T("Url Similarity percentage value"),sg.InputText("",key="url_input")],[sg.T("Enter domain "),sg.InputText("",key="domain_input")],
#               [sg.T("Choose Similarity"),
#                sg.OptionMenu(["Joint similarity", "Structural similarity", "Style similarity"],
#                              default_value=default_settings[2], key='sim_type')]]
#
#     window = sg.Window('Settings', layout, size=(300, 300))
#
#     while True:
#         event, values = window.read()
#         if event == sg.WIN_CLOSED or event == "Exit":
#             break
#         # True values of settings
#         elif event == 'save_button':
#             default_settings[0] = values["sim_check"]
#             default_settings[1] = values["url_sim"]
#             default_settings[2] = values["sim_type"]
#             default_settings[3] = values["sim_input"]
#             default_settings[4] = values["url_input"]
#             default_settings[5] = values["domain_input"]
#             #print(default_settings)
#             window.close()
#             sg.popup_auto_close("Saved",auto_close_duration=1,no_titlebar=True)
#
#
#     window.close()
#
#
# def loading_crawl(val):
#     layout = [[sg.T("Crawling", key="crawl_text")], [sg.ProgressBar(100, orientation='h', k="loading_bar")]]
#
#     window = sg.Window('Loading', layout, finalize=True, size=(300, 300))
#
#     window['loading_bar'].update(10)
#     # crawling
#     c = crawl.CrawlerProcess({})
#     c.crawl(crawl.CrawlingSpider, start_urls=[val],allowed_domains=default_settings[5])
#     c.start()
#     window['loading_bar'].update(50)
#     window['crawl_text'].update("Similarity Check")
#     # filtering
#     print(default_settings[3],"def")
#     filtered_data = crawl.sim_check(data=crawl.crawled_links, check_sim=default_settings[0],
#                                     check_url_sim=default_settings[1], param=default_settings[2],web_page_similarity_percentage=default_settings[3],web_path_similarity_percentage=default_settings[4])
#     print(filtered_data)
#     window['loading_bar'].update(100)
#     window.close()
#
#     while True:
#         event, values = window.read()
#         if event == sg.WIN_CLOSED or event == "Exit":
#             break
#         # True values of settings
#
#     return filtered_data
#     window.close()
#
# def open_table_window(filtered):
#     sg.theme('Dark Blue')
#
#     def value_to_nums(val):
#         tmp = val["-TABLE-"]
#         return tmp
#
#     def make_table(num_rows, num_cols):
#         data = [[j for j in range(num_cols)] for i in range(num_rows)]
#         for i in range(len(filtered)):
#             data[i] = [filtered[i]]
#
#         return data
#
#     table_size = len(filtered)
#     if table_size > 15:
#         table_size = 15
#
#     data = make_table(num_rows=table_size, num_cols=1)
#     headings = ["                    Crawled Links     "]
#
#     layout = [[sg.Table(values=data[0:][:], headings=headings, max_col_width=500,
#                         auto_size_columns=True,
#                         display_row_numbers=True,
#                         justification='right',
#                         num_rows=table_size,
#                         alternating_row_color='#000020',
#                         select_mode=sg.TABLE_SELECT_MODE_EXTENDED,
#                         enable_events=True,
#                         key='-TABLE-',
#                         col_widths=400,
#                         row_height=35)],
#               [sg.Text('Additional URL'), sg.InputText(key='url'), sg.Button('Add URL')],
#               [sg.Button('Continue with All'), sg.Button('Continue with Selected')],
#               [sg.Text('Add URL = Adds a new domain to the list')],
#               [sg.Text('Continue with All = Generate files with all available URLs')],
#               [sg.Text('Continue with Selected = Generate files with selected URLs')]]
#
#     window = sg.Window('ApogenPy', layout, finalize=True, size=(520, 530))
#     table = window['-TABLE-']
#
#     user_click = True
#     selected = []
#     added_links_array = []
#     while True:
#         event, values = window.read()
#         if event == sg.WIN_CLOSED:
#             break
#             window['-TABLE-'].update(values=data)
#         elif event == 'Continue with All':
#             for i in data:
#                 # DEMO.demo_fun(i[0])
#                 pomgen.file_gen(i[0])
#
#         elif event == 'Continue with Selected':
#             needed = value_to_nums(values)
#             for i in needed:
#                 # added_links_array.append(array[0][i])
#                 # DEMO.demo_fun(data[i][0]
#                 pomgen.file_gen(data[i][0])
#
#         # adds url to current set
#         elif event == 'Add URL':
#             # print(data[0])
#             data.append([values['url']])
#             # print(data)
#             window['-TABLE-'].update(values=data)
#             # print("url appended", values['url'])
#
#         # table click stuff
#         elif event == '-TABLE-':
#             if user_click:
#                 if len(values['-TABLE-']) == 1:
#                     select = values['-TABLE-'][0]
#                     if select in selected:
#                         selected.remove(select)
#                     else:
#                         selected.append(select)
#                     table.update(select_rows=selected)
#                     user_click = False
#             else:
#                 user_click = True
#
#     window.close()
