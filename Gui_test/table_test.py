#!/usr/bin/env python
import PySimpleGUI as sg
import random
import string
import csv

import FILE_GEN
import DEMO





def open_window():
    sg.theme('Dark Blue')
    # readfiltered to array
    with open('filtered_output.csv', 'r') as read_obj:
        # csv_reader = reader(read_obj, delimiter=',')
        file_read = csv.reader(read_obj)

        array = list(file_read)
        read_obj.close()



    def value_to_nums(val):

        # print()
        tmp = val["-TABLE-"]
        return tmp

    def make_table(num_rows, num_cols):
        data = [[j for j in range(num_cols)] for i in range(num_rows)]
        # data[0] = [array[0][0]]
        # print(array[0][0])
        # print(len(array[0]))
        for i in range(len(array[0])):
            #  print(i)
            data[i] = [array[0][i]]

        # for i in range(len(array)):
        #     print(array[0][i],"asfdasdf")
        #     data[i] = [array[0][i]]

        return data

    # ------ Make the Table Data ------
    table_size = len(array[0])
    print(len(array[0]))
    if table_size > 15:
        table_size = 15

    data = make_table(num_rows=table_size, num_cols=1)
    headings = ["Crawled links"]

    # ------ Window Layout ------
    layout = [[sg.Table(values=data[0:][:], headings=headings, max_col_width=225,
                        # background_color='light blue',
                        auto_size_columns=True,
                        display_row_numbers=True,
                        justification='right',
                        num_rows=table_size,
                        alternating_row_color='#000020',
                        select_mode=sg.TABLE_SELECT_MODE_EXTENDED,
                        enable_events=True,
                        key='-TABLE-',
                        row_height=35,
                        tooltip='This is a table')],
              [sg.Button('Read'), sg.Button('Select all'), sg.Button('Add')],
              [sg.Text('Read = read which rows are selected')],
              [sg.Text('Change Colors = Changes the colors of rows 8 and 9')],
              [sg.Text('Continue with selected')]]

    # ------ Create Window ------
    window = sg.Window('The Table Element', layout, finalize=True,
                       # font='Helvetica 25',
                       )
    table = window['-TABLE-']
    # ------ Event Loop ------

    user_click = True
    selected = []
    added_links_array = []
    while True:
        event, values = window.read()
        # print(event, values,"fasdfasdf")
        if event == sg.WIN_CLOSED:
            break
            window['-TABLE-'].update(values=data)
        elif event == 'Select All':
            for i in array[0]:
                DEMO.demo_fun(i)
                FILE_GEN.gen(i)
                print("func called")
        # add button func
        elif event == 'Add':
            needed = value_to_nums(values)
            for i in needed:
                #added_links_array.append(array[0][i])

                DEMO.demo_fun(array[0][i])

                FILE_GEN.gen(array[0][i])
            print("func called")


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
