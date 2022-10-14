import csv
import threading

import PySimpleGUI as sg

from scrapy.crawler import CrawlerProcess


import table_test
import crawl
import loading_window

from sim_check import sim_check
# crawl functions
c = CrawlerProcess({
    #'USER_AGENT': 'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.93 Safari/537.36',
    'FEED_FORMAT': 'csv',
    'FEED_URI': 'output.csv',
})





def main():
    sg.theme('Dark Blue')  # Add a touch of color
    # All the stuff inside your window.
    layout = [[sg.Text('Past link below that you want to crawl')],
            [sg.Text('Crawl domain'), sg.InputText()],
            [sg.Button('Crawl'), sg.Button('exit')], sg.Button('Settings')
              ]

    # Create the Window
    window = sg.Window('ApogenPy', layout, size=(600, 250))
    #   Event Loop to process "events" and get the "values" of the inputs
    while True:
        event, values = window.read()
        if event == 'Crawl':
            print("here")

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


            c.crawl(crawl.CrawlingSpider, start_urls=[values[0]])
            #t1 = threading.Thread(target=run())
            #t2 = threading.Thread(target=c.crawl())
           ## t2.start()
          #  t1.start()
            #tmp = loading_window.loading_win()


            #c.start()
           # t = threading.Thread(target=image_loading().start)
            flag = False
            c.start()
            #t.join(c)
            #loading animation

            # find all cites



            # filter
            #sim_check()
            #end loading animation

            #close window before entering new

            window.close()
            stop_threads = True
            #t1.join()
            print("thread killed")
            #next window
            table_test.open_window()
        elif event == 'Settings':

            window.close()

        elif event == sg.WIN_CLOSED or event == 'exit': # if user closes window or clicks cancel
            window.close()
            break
        #print(values[0])

    window.close()


if __name__ == "__main__":
    main()