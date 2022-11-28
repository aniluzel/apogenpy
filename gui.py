import time
from urllib.parse import urlparse
from PyQt5.QtCore import QUrl, QCoreApplication
from PyQt5.QtWidgets import QApplication, QMainWindow, QLineEdit, QVBoxLayout, QProgressBar, QPushButton, QListWidget, \
    QAbstractItemView, QWidget, QHBoxLayout, QCheckBox, QComboBox, QMessageBox, QFileDialog
from PyQt5.QtWidgets import QLabel

import sys
import crawl
import pomgen
import advertools as adv
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from PyQt5 import QtCore, QtGui, QtWidgets, QtWebEngineWidgets
import utils

default_settings = [False, False, 1, 0.92, 0.88, None, True, 2]
filtered_data = []


def crawl_filter_func(textbox):
    global filtered_data

    c = crawl.CrawlerProcess({})
    if (default_settings[5] == None):
        c.crawl(crawl.CrawlingSpider, start_urls=[textbox.text()], allowed_domains=default_settings[5])
    else:
        c.crawl(crawl.CrawlingSpider, start_urls=[textbox.text()], allowed_domains=[default_settings[5]])
    c.start()

    # self.pbar.setValue(30)
    url_data = adv.url_to_df(textbox.text())
    domain = url_data["scheme"] + "://" + url_data["netloc"]
    # print(domain[0],"<- domain")
    tmp = []
    # self.pbar.setValue(50)
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_driver_path = utils.chromedriver_path_name()
    # print(chrome_driver_path)
    driver = webdriver.Chrome(executable_path=chrome_driver_path, options=chrome_options)
    if default_settings[6]:
        if default_settings[5] == None:
            tmp = crawl.looping(crawl.crawl_one(textbox.text(), domain[0], driver), domain[0], driver,
                                limit=20000)
        else:
            tmp = crawl.looping(crawl.crawl_one(textbox.text(), default_settings[5], driver),
                                default_settings[5], driver,
                                limit=20000)

    driver.quit()
    # driver.close()
    # print(len(tmp),"tmp")
    for i in tmp:
        if i not in crawl.crawled_links:
            if domain[0] in str(i):
                crawl.crawled_links.append(i)

        # self.loading_label.setText("Filtering")
        # self.pbar.setValue(70)
    filtered_data = crawl.sim_check(data=crawl.crawled_links, check_sim=default_settings[0],
                                    check_url_sim=default_settings[1], param=default_settings[2],
                                    web_page_similarity_percentage=default_settings[3],
                                    web_path_similarity_percentage=default_settings[4])

    # self.pbar.setValue(100)
    # self.second_page()
    # self.QtStack.setCurrentIndex(1)
    #     else:
    #         self.QtStack.setCurrentIndex(0)
    #         QMessageBox.about(self, "Error", "Url is not valid")
    # except TypeError as e:
    #     QMessageBox.about(self, "Error has acquired", str(e))

class SearchPanel(QtWidgets.QWidget):
    searched = QtCore.pyqtSignal(str, QtWebEngineWidgets.QWebEnginePage.FindFlag)
    closed = QtCore.pyqtSignal()

    def __init__(self, parent=None):
        super(SearchPanel, self).__init__(parent)
        lay = QtWidgets.QHBoxLayout(self)
        done_button = QtWidgets.QPushButton('&Done')
        self.case_button = QtWidgets.QPushButton('Match &Case', checkable=True)
        next_button = QtWidgets.QPushButton('&Next')
        prev_button = QtWidgets.QPushButton('&Previous')
        self.search_le = QtWidgets.QLineEdit()
        self.setFocusProxy(self.search_le)
        done_button.clicked.connect(self.closed)
        next_button.clicked.connect(self.update_searching)
        prev_button.clicked.connect(self.on_preview_find)
        self.case_button.clicked.connect(self.update_searching)
        for btn in (self.case_button, self.search_le, next_button, prev_button, done_button, done_button):
            lay.addWidget(btn)
            if isinstance(btn, QtWidgets.QPushButton): btn.clicked.connect(self.setFocus)
        self.search_le.textChanged.connect(self.update_searching)
        self.search_le.returnPressed.connect(self.update_searching)
        self.closed.connect(self.search_le.clear)

        QtWidgets.QShortcut(QtGui.QKeySequence.FindNext, self, activated=next_button.animateClick)
        QtWidgets.QShortcut(QtGui.QKeySequence.FindPrevious, self, activated=prev_button.animateClick)
        QtWidgets.QShortcut(QtGui.QKeySequence(QtCore.Qt.Key_Escape), self.search_le, activated=self.closed)

    @QtCore.pyqtSlot()
    def on_preview_find(self):
        self.update_searching(QtWebEngineWidgets.QWebEnginePage.FindBackward)

    @QtCore.pyqtSlot()
    def update_searching(self, direction=QtWebEngineWidgets.QWebEnginePage.FindFlag()):
        flag = direction
        if self.case_button.isChecked():
            flag |= QtWebEngineWidgets.QWebEnginePage.FindCaseSensitively
        self.searched.emit(self.search_le.text(), flag)

    # self.searched.emit("ERROR", flag)

    @QtCore.pyqtSlot()
    def text_fi(self, text, direction=QtWebEngineWidgets.QWebEnginePage.FindFlags()):
        flag = direction
        # print(flag)
        # flag |= QtWebEngineWidgets.QWebEnginePage.FindCaseSensitively
        # for i in flag:
        # print(self.searched.)

        # self.searched.emit("ERROR", flag)
        self.searched.emit(text, flag)

    def showEvent(self, event):
        super(SearchPanel, self).showEvent(event)
        self.setFocus(True)


class Ui_Main(QtWidgets.QWidget):
    def setupUi(self, Main):
        Main.setObjectName("Main")
        Main.resize(800, 480)
        self.QtStack = QtWidgets.QStackedLayout()
        self.first_page_stack = QtWidgets.QWidget()
        self.second_page_stack = QtWidgets.QWidget()
        self.third_page_stack = QtWidgets.QWidget()
        self.settings_stack = QtWidgets.QWidget()
        self.loading_stack = QtWidgets.QWidget()
        self.first_page_stack.setWindowTitle("ApogenPy")
        self.second_page_stack.setWindowTitle("ApogenPy")
        self.third_page_stack.setWindowTitle("ApogenPy")
        self.settings_stack.setWindowTitle("ApogenPy")
        self.loading_stack.setWindowTitle("ApogenPy")
        self.first_page()

        self.QtStack.addWidget(self.first_page_stack) #0
        self.QtStack.addWidget(self.second_page_stack) #1
        self.QtStack.addWidget(self.third_page_stack) #2
        self.QtStack.addWidget(self.settings_stack) #3
        self.QtStack.addWidget(self.loading_stack) #4

    # frist page start
    def first_page(self):
        self.htmls_arr = []
        layout = QVBoxLayout()
        # self.first_page_stack.resize(800, 480)
        label1 = QLabel("Enter the URL of a domain that you want to crawl")
        textbox = QLineEdit()
        textbox.move(20, 20)
        textbox.resize(280, 40)
        # PushButton1#
        crawl_button = QtWidgets.QPushButton()
        crawl_button.setText("Crawl")
        crawl_button.setGeometry(QtCore.QRect(10, 10, 100, 100))
#        self.loadingUI()
        crawl_button.clicked.connect(lambda: self.crawl_button_action(textbox))

        # PushButton2#
        setting_button = QtWidgets.QPushButton()
        setting_button.setText("Settings")
        self.settings_page()
        # self.loadingUI()
        setting_button.setGeometry(QtCore.QRect(150, 150, 100, 100))
        setting_button.clicked.connect(self.settings_clicked)

        # continue iwthout crawling
        con_craw = QtWidgets.QPushButton("Select Multiple Files")
        con_craw.clicked.connect(self.con_crawl_action)
        # PushButton3#
        exit_button = QtWidgets.QPushButton()
        exit_button.setText("Exit")
        exit_button.setGeometry(QtCore.QRect(150, 150, 100, 100))
        exit_button.clicked.connect(QCoreApplication.instance().quit)
        #
        if not utils.chromedriver_checker():
            QMessageBox.about(self, "Generated", "Chrome driver not downloaded please download from settings_page")

        # layout
        layout.addWidget(label1)
        layout.addWidget(textbox)
        layout.addWidget(crawl_button)
        layout.addWidget(con_craw)
        layout.addWidget(setting_button)
        layout.addWidget(exit_button)
        self.first_page_stack.setLayout(layout)

    def crawl_button_action(self, textbox):
        try:
            self.loadingUI()
            self.QtStack.setCurrentIndex(4)
            if self.valid_url(textbox.text()):
                crawl_filter_func(textbox)
                self.second_page()
                self.QtStack.setCurrentIndex(1)
            else:
                self.QtStack.setCurrentIndex(0)
                QMessageBox.about(self, "Error", "Url is not valid")

        except TypeError as e:
            QMessageBox.about(self, "Error has acquired", str(e))


    def settings_clicked(self):
        self.QtStack.setCurrentIndex(3)

    def con_crawl_action(self):
        file, check = QFileDialog.getOpenFileNames(None, "QFileDialog.getOpenFileName()",
                                                   "", "All Files (*);;Html files (*.html)")
        if check:
            for i in file:
                self.htmls_arr.append(i)
                # crawl.crawled_links.append(i)

            self.second_page()
            self.QtStack.setCurrentIndex(1)
            # print(file)
        # self.second_page()()
        # self.QtStack.setCurrentIndex(1)

    # First pages end

    # Second page start
    def second_page(self):
        global filtered_data
        self.second_page_stack.resize(700, 400)
        data = filtered_data
        for i in self.htmls_arr:
            if i not in data:
                data.append(i)
        table_layout = QVBoxLayout()
        table = QListWidget()
        table.resize(300, 120)
        for i in data:
            table.addItem(i)
        table.setSelectionMode(QAbstractItemView.MultiSelection)
        table.setVerticalScrollMode(QAbstractItemView.ScrollPerPixel)
        table.repaint()
        table.update()
        table.itemClicked.connect(lambda: self.add_selected(table))

        add_url_layout = QHBoxLayout()
        add_url_label = QLabel("Additional url")
        add_url_textbox = QLineEdit()
        add_url_layout.addWidget(add_url_label)
        add_url_layout.addWidget(add_url_textbox)

        # print(filtered_data )
        # self.table_layout.addWidget()
        # self.second_page_stack.setLayout(self.load_layout)

        sel = QPushButton('Selected')
        all_sel = QPushButton('All')
        add = QPushButton('Add url')
        add_path = QPushButton('Select file')

        sel.clicked.connect(lambda: self.selected_url_click())
        all_sel.clicked.connect(lambda: self.all_sel_click(data))
        add.clicked.connect(lambda: self.add_click(table, add_url_textbox.text(), data))
        add_path.clicked.connect(lambda: self.dialog(table))

        table_layout.addWidget(table)
        table_layout.addLayout(add_url_layout)
        table_layout.addWidget(sel)
        table_layout.addWidget(all_sel)
        table_layout.addWidget(add)
        table_layout.addWidget(add_path)

        # if (not self.second_page_stack.layout()):
        self.second_page_stack.setLayout(table_layout)

    def add_selected(self, listWidget):
        items = listWidget.selectedItems()
        global selected
        selected = []
        for i in range(len(items)):
            selected.append(str(listWidget.selectedItems()[i].text()))

    def selected_url_click(self):
        try:
            global selected
            if (len(selected) != 0):
                self.third_page(selected)
                self.QtStack.setCurrentIndex(2)
            else:
                QMessageBox.about(self, "Generated", "No links were selected")
        except NameError:
            QMessageBox.about(self, "Generated", "No links were selected")

    def all_sel_click(self, data):
        if (len(data) != 0):
            self.third_page(data)
            self.QtStack.setCurrentIndex(2)
        else:
            QMessageBox.about(self, "Generated", "No link are in the list")

    def update_table(self, table, data):
        table.addItem(data)
        table.repaint()

    def add_click(self, table, data, arr):
        if len(data) == 0:
            QMessageBox.about(self, "Generated", "Empty field provided")
        else:
            arr.append(data)
            self.update_table(table, data)

    def dialog(self, table):
        file, check = QFileDialog.getOpenFileName(None, "QFileDialog.getOpenFileName()",
                                                  "", "All Files (*);;Html files (*.html)")
        if check:
            table.addItem(file)
            table.repaint()
            print(file)

    # second page end

    # settings page start
    def settings_page(self):
        settings_layout = QVBoxLayout()
        search_bars = QVBoxLayout()
        text_laoyout = QVBoxLayout()
        comb_layout = QHBoxLayout()
        # performing sim similarity check
        checkbox_layout = QHBoxLayout()
        sim_check = QCheckBox("Structure Similarity Check")
        sim_check.setChecked(default_settings[0])
        checkbox_layout.addWidget(sim_check)
        # chrome driver button
        chrome_driver_down = QPushButton("Download latest chrome driver")
        chrome_driver_down.clicked.connect(self.chorme_dr_down)

        # perfroming url similarity check
        url_sim = QCheckBox("URL Similarity Check")
        url_sim.setChecked(default_settings[1])
        checkbox_layout.addWidget(url_sim)
        # advanced crawl
        add_crawl = QCheckBox("Advanced crawling")
        add_crawl.setChecked(default_settings[6])
        checkbox_layout.addWidget(add_crawl)

        #
        percentage_layout = QHBoxLayout()
        percentage_sim_label = QLabel("Similarity percentage value")
        percentage_sim_textbox = QLineEdit()
        text_laoyout.addWidget(percentage_sim_label)
        # percentage_layout.addWidget(percentage_sim_label)
        # percentage_layout.addWidget(percentage_sim_textbox)
        search_bars.addWidget(percentage_sim_textbox)
        #
        url_layout = QHBoxLayout()
        percentage_url_label = QLabel("Url Similarity percentage value")
        percentage_url_textbox = QLineEdit()
        text_laoyout.addWidget(percentage_url_label)
        # url_layout.addWidget(percentage_url_label)
        # url_layout.addWidget(percentage_url_textbox)
        search_bars.addWidget(percentage_url_textbox)

        domain_layout = QHBoxLayout()
        domain_label = QLabel("Enter domain ")
        domain_textbox = QLineEdit()
        text_laoyout.addWidget(domain_label)
        # domain_layout.addWidget(domain_label)
        # domain_layout.addWidget(domain_textbox)
        search_bars.addWidget(domain_textbox)

        combobox1 = QComboBox()
        combobox1.addItem('Joint similarity')
        combobox1.addItem('Structural similarity')
        combobox1.addItem('Style similarity')

        combobox1.setCurrentIndex(default_settings[2])

        save_button = QPushButton("Save and Close")
        save_button.clicked.connect(
            lambda: self.save_cliked(sim_check.isChecked(), url_sim.isChecked(), combobox1.currentIndex(),
                                     percentage_sim_textbox.text(), percentage_url_textbox.text(),
                                     domain_textbox.text(), add_crawl.isChecked()))

        settings_layout.addLayout(checkbox_layout)
        comb_layout.addLayout(text_laoyout)
        comb_layout.addLayout(search_bars)
        settings_layout.addLayout(comb_layout)
        # settings_layout.addLayout(percentage_layout)
        # settings_layout.addLayout(url_layout)
        # settings_layout.addLayout(domain_layout)
        settings_layout.addWidget(combobox1)
        settings_layout.addWidget(save_button)
        settings_layout.addWidget(chrome_driver_down)
        self.settings_stack.setLayout(settings_layout)

    def chorme_dr_down(self):
        # fucntions
        utils.chrome_driver_downloader()
        chrome_version = utils.chromedriver_autoinstaller.get_chrome_version()
        QMessageBox.about(self, "driver", "Version " + chrome_version + " downloaded")

    def save_cliked(self, sim, url, index, per_sim, per_url, dom, add_crawl):
        # print("saved")
        default_settings[0] = sim
        default_settings[1] = url
        default_settings[2] = index
        default_settings[6] = add_crawl
        all_correct = True;
        try:
            if per_sim != '':
                if 0.1 <= float(per_sim) < 0.99:
                    default_settings[3] = per_sim
                else:
                    all_correct = False
                    QMessageBox.about(self, "Input error", "Input must be between 0.1 < 0.99")
            if per_url != '':
                if 0.1 <= float(per_url) < 0.99:
                    default_settings[4] = per_url
                else:
                    all_correct = False
                    QMessageBox.about(self, "Input error", "Input must be between 0.1 < 0.99")

            if dom != '':
                # if self.valid_url(dom):
                default_settings[5] = dom
            # else:
            #    all_correct = False
            #    QMessageBox.about(self, "Error", "Url is not valid")
            if all_correct:
                self.QtStack.setCurrentIndex(0)
            else:
                self.QtStack.setCurrentIndex(3)
        except Exception:
            QMessageBox.about(self, "Error", "Not valid input")

    def valid_url(self, to_validate: str) -> bool:
        o = urlparse(to_validate)
        return True if o.scheme and o.netloc else False

    # settings end

    # loading page start
    def loadingUI(self):
        # creating progress bar
        loading_label = QLabel("Loading...");
        loading_layout = QVBoxLayout()
        loading_layout.addWidget(loading_label)
        self.loading_stack.setLayout(loading_layout)
        #self.QtStack.setCurrentIndex(4)


    # loading end

    # third page start
    def third_page(self, url):
        self.counter = 0
        self.selected_elements = []
        listWidget = QListWidget()
        # self.web = QWebView()
        self.web = Browser()
        self.web.show()
        self.third_page_stack.resize(1000, 800)

        if self.valid_url(url[self.counter]):
            self.web._view.load(QUrl(url[self.counter]))
        else:
            self.web._view.load(QtCore.QUrl.fromLocalFile(str(url[self.counter])))
        data = [[]]
        self.headers = []
        for x in pomgen.elemfinder(url[self.counter]):
            data.append([x.name, x.type])
            self.headers.append(x.type)

        # print(data)

        # data = pomgen.elemfinder(url[self.counter])
        next_button = QPushButton('Next page')
        generate_button = QPushButton('Generate for selected')
        gen_all_button = QPushButton('Generate all for this page')
        current_url_label = QLabel("Elements of " + url[self.counter])

        next_button.clicked.connect(
            lambda: self.table_cleaner(self.web, next_button, url, listWidget, current_url_label))
        generate_button.clicked.connect(lambda: self.generate_button_clicked(url[self.counter]))
        gen_all_button.clicked.connect(lambda: self.gen_all_button_cliked(url[self.counter]))
        if (len(url) == 1):
            next_button.hide()

        main_layout = QHBoxLayout()
        but_list_layout = QVBoxLayout()
        but_list_layout.addWidget(current_url_label)
        but_list_layout.addWidget(listWidget)
        but_list_layout.addWidget(next_button)
        but_list_layout.addWidget(generate_button)
        but_list_layout.addWidget(gen_all_button)

        main_layout.addWidget(self.web)

        listWidget.resize(300, 150)
        self.add_to_list(listWidget, data)
        listWidget.setSelectionMode(QAbstractItemView.MultiSelection)
        listWidget.setVerticalScrollMode(QAbstractItemView.ScrollPerPixel)
        listWidget.itemClicked.connect(lambda: self.web_elements_selected_list(listWidget))

        main_layout.addLayout(but_list_layout)
        self.third_page_stack.setLayout(main_layout)

    def add_to_list(self, windget, data):
        header = ""
        for i in data:
            if len(i) < 2:
                print("empty arr")
            elif header == "":
                header = i[1]
                windget.addItem("Type : " + i[1])
            elif header == i[1]:
                windget.addItem(i[0])
            else:
                header = i[1]
                windget.addItem("Type : " + i[1])

    def update_counter(self, val):
        # global self.counter
        self.counter = val
        return self.counter

    def table_cleaner(self, web, button, url, listWidget, current_url_label):
        self.counter += 1
        if self.counter == len(url) - 1:
            button.hide()
        if self.valid_url(url[self.counter]):
            web._view.load(QUrl(url[self.counter]))
        else:
            web._view.load(QtCore.QUrl.fromLocalFile(str(url[self.counter])))

        # self.headers = []
        self.data = [[]]

        for x in pomgen.elemfinder(url[self.counter]):
            self.data.append([x.name, x.type])
            if x.type not in self.headers:
                self.headers.append(x.type)

        # data = pomgen.elemfinder(url[self.counter])
        listWidget.clear()
        self.add_to_list(listWidget, self.data)

        listWidget.repaint()
        # print("next button clicked")
        current_url_label.setText("Elements of " + url[self.counter])
        self.update_counter(self.counter)

    def generate_button_clicked(self, url):
        try:
            # global selected_elements
            for i in self.headers:
                if i in self.selected_elements:
                    self.selected_elements.remove(i)
            # print(self.headers)
            # print(selected_elements)
            tmp = []
            for g in pomgen.elemfinder(url):
                for k in self.selected_elements:
                    if k == g.name:
                        tmp.append(g)
            print(tmp)

            if len(self.selected_elements) != 0:
                pomgen.file_gen(url, tmp)  #### burası fixlencek
        except NameError:
            QMessageBox.about(self, "Generated", "No elements were selected")
        else:
            # print("generated for ", item)
            QMessageBox.about(self, "Generated", "Generated for selected")

    def gen_all_button_cliked(self, data):
        # data takes url
        pomgen.file_gen(data, pomgen.elemfinder(data))
        ####burası fixlencek
        QMessageBox.about(self, "Generated", "Generated for all")

    def web_elements_selected_list(self, listWidget):
        items = listWidget.selectedItems()
        # global selected_elements
        # selected_elements = []
        if (len(items) != 0):
            for i in range(len(items)):
                self.selected_elements.append(str(listWidget.selectedItems()[i].text()))
                # for x in self.headers:
                #     if str(listWidget.selectedItems()[i].text()) == x:
                #         selected_elements.append(listWidget.get)

                # input example nav-bar output HOME,ERROR
                # while True:
                # self.web._search_panel.text_fi("HOME")
                # time.sleep(2)
                # self.web._search_panel.text_fi("ERROR")
                # time.sleep(2)
        else:
            self.web._search_panel.text_fi("")


class Browser(QtWidgets.QMainWindow, ):
    def __init__(self, parent=None):
        super(Browser, self).__init__(parent)
        self._view = QtWebEngineWidgets.QWebEngineView()
        self.setCentralWidget(self._view)
        self._view.load(QtCore.QUrl('http://localhost:8080/vets.html'))
        self._search_panel = SearchPanel()
        self.search_toolbar = QtWidgets.QToolBar()
        self.search_toolbar.addWidget(self._search_panel)
        self.addToolBar(QtCore.Qt.BottomToolBarArea, self.search_toolbar)
        self.search_toolbar.hide()
        self._search_panel.searched.connect(self.on_searched)
        self._search_panel.closed.connect(self.search_toolbar.hide)
        self.create_menus()

    @QtCore.pyqtSlot(str, QtWebEngineWidgets.QWebEnginePage.FindFlag)
    def on_searched(self, text, flag):
        def callback(found):
            if text and not found:
                # print(text)
                self.statusBar().show()
                self.statusBar().showMessage('Not found')
            else:
                self.statusBar().hide()

        self._view.findText(text, flag, callback)
        # self._view.findText()

        # self._view.findText("ERROR", flag, callback)

    def create_menus(self):
        menubar = self.menuBar()
        file_menu = menubar.addMenu('&File')
        file_menu.addAction('&Find...', self.search_toolbar.show, shortcut=QtGui.QKeySequence.Find)


class Main(QMainWindow, Ui_Main):
    def __init__(self, parent=None):
        super(Main, self).__init__(parent)
        self.setupUi(self)


def gui_start():
    app = QApplication(sys.argv)
    app.setWindowIcon(QtGui.QIcon('logo.png'))
    showMain = Main()
    sys.exit(app.exec_())
