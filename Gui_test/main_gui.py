import csv

import PySimpleGUI as sg

from scrapy.crawler import CrawlerProcess


import table_test
import crawl

from sim_check import sim_check
# crawl functions
c = CrawlerProcess({
    #'USER_AGENT': 'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.93 Safari/537.36',
    'FEED_FORMAT': 'csv',
    'FEED_URI': 'output.csv',
})





def main():
    sg.theme('DarkAmber')   # Add a touch of color
    # All the stuff inside your window.
    layout = [  [sg.Text('Past link below that you want to crawl')],
            [sg.Text('Crawl domain'), sg.InputText()],
            [sg.Button('Crawl'), sg.Button('exit')] ]

    # Create the Window
    window = sg.Window('Window Title', layout)
    #   Event Loop to process "events" and get the "values" of the inputs
    while True:
        event, values = window.read()
        if event == 'Crawl':
            # find all cites
            c.crawl(crawl.CrawlingSpider, start_urls=[values[0]])
            c.start()
            # filter
            sim_check()
            #next window
            table_test.open_window()
            window.close()
        elif event == sg.WIN_CLOSED or event == 'exit': # if user closes window or clicks cancel
            break
        #print(values[0])

    window.close()


if __name__ == "__main__":
    main()