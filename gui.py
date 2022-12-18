import time
from urllib.parse import urlparse
from PyQt5.QtCore import QUrl, QCoreApplication, Qt, QThread, pyqtSignal, QObject, QEvent, QRect
from PyQt5.QtGui import QPainter, QColor, QPixmap
from PyQt5.QtWidgets import QApplication, QMainWindow, QLineEdit, QVBoxLayout, QPushButton, QListWidget, \
    QAbstractItemView, QHBoxLayout, QCheckBox, QComboBox, QMessageBox, QFileDialog, QListWidgetItem, QWidget, QTabWidget
from PyQt5.QtWidgets import QLabel
import sys
import pomgen
import advertools as adv
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from PyQt5 import QtCore, QtGui, QtWidgets, QtWebEngineWidgets
import utils
from settings import default_settings

filtered_data = []


class Overlay(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        self.setAttribute(Qt.WA_NoSystemBackground)
        self.setAttribute(Qt.WA_TransparentForMouseEvents)

    def paintEvent(self, event):
        QPainter(self).fillRect(self.rect(), QColor(80, 80, 255, 128))


class Filter(QObject):
    def __init__(self, parent=None):
        QObject.__init__(self, parent)
        self.m_overlay = None
        self.m_overlayOn = None

    def eventFilter(self, w, event):
        if w.isWidgetType():
            if event.type() == QEvent.MouseButtonPress:
                if not self.m_overlay:
                    self.m_overlay = Overlay(w.parentWidget());
                    self.m_overlay.setGeometry(w.geometry());
                    self.m_overlayOn = w;
                    self.m_overlay.show();
            elif event.type() == QEvent.Resize:
                if self.m_overlay and self.m_overlayOn is w:
                    self.m_overlay.setGeometry(w.geometry());
        return False


def crawl_filter_func(textbox):
    global filtered_data
    import crawl
    if default_settings[8] == True:
        #future_update
        c = crawl.CrawlerProcess({})
        # c.crawl(crawl.ScrapySpider)
        # c.start()
    else:
        if default_settings[5] is None:
            c = crawl.CrawlerProcess({})
            crawl.CrawlingSpider.set_sett(default_settings[12])
            c.crawl(crawl.CrawlingSpider, start_urls=[textbox.text()], allowed_domains=default_settings[5])
        else:
            c = crawl.CrawlerProcess({})
            c.crawl(crawl.CrawlingSpider, start_urls=[textbox.text()], allowed_domains=[urlparse(default_settings[5]).netloc])
        c.start()

        url_data = adv.url_to_df(textbox.text())
        domain = url_data["scheme"] + "://" + url_data["netloc"]


        tmp = []
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_driver_path = utils.chromedriver_path_name()
        # print(chrome_driver_path)
        driver = webdriver.Chrome(executable_path=chrome_driver_path, options=chrome_options)
        if default_settings[6]:
            if default_settings[5] is None:
                tmp = crawl.looping(crawl.crawl_one(textbox.text(), domain[0], driver), domain[0], driver,
                                    limit=default_settings[13])
            else:
                tmp = crawl.looping(crawl.crawl_one(textbox.text(), default_settings[5], driver),
                                    default_settings[5], driver,
                                    limit=default_settings[13])

        driver.quit()

        for i in tmp:
            if i not in crawl.crawled_links:
                if domain[0] in str(i):
                    crawl.crawled_links.append(i)

        filtered_data = crawl.sim_check(data=crawl.crawled_links, check_sim=default_settings[0],
                                        check_url_sim=default_settings[1], param=default_settings[2],
                                        web_page_similarity_percentage=default_settings[3],
                                        web_path_similarity_percentage=default_settings[4])


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
        self.searched.emit(text, flag)

    def showEvent(self, event):
        super(SearchPanel, self).showEvent(event)
        self.setFocus(True)


class Ui_Main(QtWidgets.QWidget):
    def setupUi(self, Main):
        Main.setObjectName("Main")
        Main.resize(800, 480)
        # fonts
        self.bold_font = QtGui.QFont()
        self.bold_font.setBold(True)

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

        self.QtStack.addWidget(self.first_page_stack)  # 0
        self.QtStack.addWidget(self.second_page_stack)  # 1
        self.QtStack.addWidget(self.third_page_stack)  # 2
        self.QtStack.addWidget(self.settings_stack)  # 3
        self.QtStack.addWidget(self.loading_stack)  # 4

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
        crawl_button.setText("Start crawling")
        crawl_button.setGeometry(QtCore.QRect(10, 10, 100, 100))
        #        self.loadingUI()
        crawl_button.clicked.connect(lambda: self.crawl_button_action(textbox))

        # settings button#
        setting_button = QtWidgets.QPushButton()
        setting_button.setText("Settings")
        self.settings_page()
        # self.loadingUI()
        setting_button.setGeometry(QtCore.QRect(150, 150, 100, 100))
        setting_button.clicked.connect(self.settings_clicked)
        self.loadingUI()
        # continue without crawling
        con_craw = QtWidgets.QPushButton("Select Multiple Files")
        con_craw.clicked.connect(self.con_crawl_action)
        # exit button#
        exit_button = QtWidgets.QPushButton()
        exit_button.setText("Exit")
        exit_button.setGeometry(QtCore.QRect(150, 150, 100, 100))
        exit_button.clicked.connect(QCoreApplication.instance().quit)


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
            self.QtStack.setCurrentIndex(4)
            QApplication.processEvents()
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

            self.second_page()
            self.QtStack.setCurrentIndex(1)

    # First pages end

    # Second page start
    def second_page(self):
        global filtered_data
        # Button creation
        sel = QPushButton('Selected')
        all_sel = QPushButton('All')
        add = QPushButton('Add url')
        add_path = QPushButton('Select file')

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
        add_url_layout.addWidget(add)

        # re crawl button
        re_crawl_button = QtWidgets.QPushButton("Re-Crawl")
        re_crawl_button.setGeometry(QtCore.QRect(150, 150, 100, 100))
        re_crawl_button.clicked.connect(self.re_crawl_action)

        # buttons action
        sel.clicked.connect(lambda: self.selected_url_click())
        all_sel.clicked.connect(lambda: self.all_sel_click(data))
        add.clicked.connect(lambda: self.add_click(table, add_url_textbox.text(), data))
        add_path.clicked.connect(lambda: self.dialog(table))

        table_layout.addWidget(table)
        table_layout.addLayout(add_url_layout)
        table_layout.addWidget(sel)
        table_layout.addWidget(all_sel)
        table_layout.addWidget(add_path)
        #table_layout.addWidget(re_crawl_button)

        # if (not self.second_page_stack.layout()):
        self.second_page_stack.setLayout(table_layout)

    def add_selected(self, listWidget):
        items = listWidget.selectedItems()
        global selected
        selected = []
        for i in range(len(items)):
            selected.append(str(listWidget.selectedItems()[i].text()))

    def re_crawl_action(self):
        self.QtStack.setCurrentIndex(0)
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

    # second page end

    # settings page start
    def settings_page(self):
        test_mode = False
        settings_layout = QHBoxLayout()
        crawl_settings_layout = QVBoxLayout()
        similarity_settings_layout = QVBoxLayout()
        generation_settings_layout = QVBoxLayout()
        buttons_layout = QVBoxLayout()
        search_bars_sim = QVBoxLayout()
        text_layout_sim = QVBoxLayout()
        comb_layout_sim = QHBoxLayout()

        search_bars_crawl = QVBoxLayout()
        text_layout_crawl = QVBoxLayout()
        comb_layout_crawl = QHBoxLayout()
        # performing sim similarity check
        sim_check = QCheckBox("Html Structure Similarity Check")
        sim_check.setChecked(default_settings[0])

        # chrome driver button
        chrome_driver_down = QPushButton("Download latest chrome driver")
        chrome_driver_down.clicked.connect(self.chorme_dr_down)

        # perfroming url similarity check
        url_sim = QCheckBox("URL Similarity Check")
        url_sim.setChecked(default_settings[1])

        # deep crawl
        deep_crawl_check = QCheckBox("Deep crawling")
        deep_crawl_check.setChecked(default_settings[6])

        # use login crawl
        log_crawl = QCheckBox("Login when crawl")
        log_crawl.setChecked(default_settings[8])
        #crawl laebl
        crawl_label = QLabel("Crawl settings")
        crawl_label.resize(50,10)

        #
        percentage_sim_label = QLabel("Html Similarity percentage value")
        percentage_sim_textbox = QLineEdit()
        text_layout_sim.addWidget(percentage_sim_label)
        search_bars_sim.addWidget(percentage_sim_textbox)
        #
        percentage_url_label = QLabel("Url Similarity percentage value")
        percentage_url_textbox = QLineEdit()
        text_layout_sim.addWidget(percentage_url_label)
        search_bars_sim.addWidget(percentage_url_textbox)

        #crawl limit setter
        limit_crawl_label = QLabel("Set depth of the crawler")
        limit_crawl_textbox = QLineEdit()
        text_layout_crawl.addWidget(limit_crawl_label)
        search_bars_crawl.addWidget(limit_crawl_textbox)
        #deep crawl limit
        limit_deep_label = QLabel("Set depth of the deep crawler")
        limit_deep_textbox = QLineEdit()
        text_layout_crawl.addWidget(limit_deep_label)
        search_bars_crawl.addWidget(limit_deep_textbox)

        #domian init
        domain_label = QLabel("Enter domain ")
        domain_textbox = QLineEdit()
        text_layout_crawl.addWidget(domain_label)
        search_bars_crawl.addWidget(domain_textbox)
        #
        lpage_label = QLabel("Enter login page url")
        lpage_textbox = QLineEdit()

        login_label = QLabel("Enter login")
        login_textbox = QLineEdit()

        pass_label = QLabel("Enter password")
        pass_textbox = QLineEdit()

        gen_label = QLabel("File generation settings")

        if test_mode:
            crawl_settings_layout.addWidget(log_crawl)
            search_bars_crawl.addWidget(lpage_textbox)
            text_layout_crawl.addWidget(lpage_label)
            search_bars_crawl.addWidget(login_textbox)
            text_layout_crawl.addWidget(login_label)
            search_bars_crawl.addWidget(pass_textbox)
            text_layout_crawl.addWidget(pass_label)

        similarity_label = QLabel("Similarity settings")
        similarity_combobox = QComboBox()
        similarity_combobox.addItem('Joint similarity')
        similarity_combobox.addItem('Structural similarity')
        similarity_combobox.addItem('Style similarity')

        #tab
        tabs = QTabWidget()
        crawl_tab = QWidget()
        similarity_tab = QWidget()
        gen_tab = QWidget()
        tabs.addTab(crawl_tab,"Crawl")
        tabs.addTab(similarity_tab,"Similariy")
        tabs.addTab(gen_tab,"Generation")


        similarity_combobox.setCurrentIndex(default_settings[2])

        save_button = QPushButton("Save and Close")
        save_button.clicked.connect(
            lambda: self.save_cliked(sim_check.isChecked(), url_sim.isChecked(), similarity_combobox.currentIndex(),
                                     percentage_sim_textbox.text(), percentage_url_textbox.text(),
                                     domain_textbox.text(), deep_crawl_check.isChecked(), log_crawl.isChecked(),
                                     login_textbox.text(), pass_textbox.text(), lpage_textbox.text(),limit_crawl_textbox.text(),limit_deep_textbox.text()))
        #button layout setup
        buttons_layout.addWidget(save_button)
        buttons_layout.addWidget(chrome_driver_down)

        #combo_sim
        comb_layout_sim.addLayout(text_layout_sim)
        comb_layout_sim.addLayout(search_bars_sim)

        #combo crawl
        comb_layout_crawl.addLayout(text_layout_crawl)
        comb_layout_crawl.addLayout(search_bars_crawl)

        #similarity layout
        similarity_settings_layout.addWidget(similarity_label)
        similarity_settings_layout.addWidget(url_sim)
        similarity_settings_layout.addWidget(sim_check)
        similarity_settings_layout.addLayout(comb_layout_sim)
        similarity_settings_layout.addWidget(similarity_combobox)

        #crawl layout
        crawl_settings_layout.addWidget(crawl_label)
        crawl_settings_layout.addWidget(deep_crawl_check)
        crawl_settings_layout.addLayout(comb_layout_crawl)


        #gen_layout
        generation_settings_layout.addWidget(gen_label)

        #tabs setup
        crawl_tab.setLayout(crawl_settings_layout)
        similarity_tab.setLayout(similarity_settings_layout)
        gen_tab.setLayout(generation_settings_layout)


        #setings layout

        settings_layout.addWidget(tabs)
        settings_layout.addLayout(buttons_layout)
        self.settings_stack.setLayout(settings_layout)

    def chorme_dr_down(self):
        # fucntions
        utils.chrome_driver_downloader()
        chrome_version = utils.chromedriver_autoinstaller.get_chrome_version()
        QMessageBox.about(self, "driver", "Version " + chrome_version + " downloaded")

    def save_cliked(self, sim, url, index, per_sim, per_url, dom, deep_crawl_check, log_crawl, login, password, lpage,crawl_limit,deep_limit):
        default_settings[0] = sim
        default_settings[1] = url
        default_settings[2] = index
        default_settings[6] = deep_crawl_check
        default_settings[8] = log_crawl
        default_settings[11] = lpage
        all_correct = True;
        try:
            if (crawl_limit !=""):
                default_settings[12] = int(crawl_limit)
            if (deep_limit !=""):
                default_settings[13] = int(deep_limit)

            if (log_crawl == True):
                if login == "" or password == "":
                    all_correct = False
                else:
                    default_settings[9] = login
                    default_settings[10] = password

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
                print(default_settings)
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
        self.loading_stack.resize(160, 70)
        self.loading_stack.setWindowFlag(Qt.FramelessWindowHint)
        self.loading_stack.setAttribute(Qt.WA_TranslucentBackground)
        self.loading_stack.setWindowOpacity(0.9)
        self.loading_stack.setStyleSheet("""
            background:rgb(255, 255, 255);
            border-top-left-radius:{0}px;
            border-bottom-left-radius:{0}px;
            border-top-right-radius:{0}px;
            border-bottom-right-radius:{0}px;
            """.format(15))

        loading_label = QLabel("  Crawling...");
        loading_label.setAlignment(QtCore.Qt.AlignCenter)
        loading_label.setFont(self.bold_font)
        loading_layout = QVBoxLayout()
        loading_layout.addWidget(loading_label)
        self.loading_stack.setLayout(loading_layout)

    # loading end

    # third page start
    def third_page(self, url):
        self.abspath = []
        self.counter = 0
        self.web = Browser()
        self.web.show()
        filter = Filter()
        self.web.installEventFilter(filter)

        self.all_objects = []
        self.selected_objects = []
        self.web.resize(1200, 900)
        self.web.setMaximumWidth(1200)
        # self.third_page_stack.resize(1000, 800)
        if self.valid_url(url[self.counter]):
            self.web._view.load(QUrl(url[self.counter]))
        else:
            self.web._view.load(QtCore.QUrl.fromLocalFile(str(url[self.counter])))

        listWidget = QListWidget()
        # listWidget.setFlags(QtCore.Qt.ItemIsUserCheckable)
        listWidget.resize(200, 800)
        # listWidget.setMaximumWidth(200)
        url_combo = QComboBox()
        for i in url:
            url_combo.addItem(i)

        url_combo.setCurrentIndex(self.counter)
        url_combo.activated.connect(lambda: self.update_web_combo(url_combo,self.web,next_button,url,listWidget,current_url_label))


        object_array = pomgen.HTMLFilterer(url[self.counter], pomgen.html_tags)

        for x in object_array:
            # listWidget.addItem(x.GUI_window_adder())
            self.table_add_obejct(listWidget, x)

        # listWidget.setSelectionMode(QAbstractItemView.MultiSelection)
        listWidget.setVerticalScrollMode(QAbstractItemView.ScrollPerPixel)
        listWidget.itemClicked.connect(lambda: self.printItemText(listWidget))
        next_button = QPushButton('Next page')
        generate_for_selected_button = QPushButton('Generate for selected elements')
        generate_all_button = QPushButton('Generate for all elements in current page')
        item_info = QPushButton('More info about item')
        current_url_label = QLabel("Elements of ")
        current_url_label.setFont(self.bold_font)
        url_and_combobox_layout = QHBoxLayout()
        url_and_combobox_layout.addWidget(current_url_label)
        url_and_combobox_layout.addWidget(url_combo)
        next_button.clicked.connect(
            lambda: self.table_cleaner(self.web, next_button, url, listWidget, url_combo))
        generate_for_selected_button.clicked.connect(
            lambda: self.generate_for_selected_button_action(url[self.counter]))
        generate_all_button.clicked.connect(
            lambda: self.generate_all_button_click(url[self.counter]))

        self.abspath = pomgen.get_page_screenshot(url[self.counter])
        item_info.clicked.connect(lambda: self.item_info_action(listWidget, url[self.counter],self.abspath))

        if len(url) == 1:
            next_button.hide()

        main_layout = QHBoxLayout()
        but_list_layout = QVBoxLayout()
        but_list_layout.addLayout(url_and_combobox_layout)
        but_list_layout.addWidget(listWidget)
        but_list_layout.addWidget(next_button)
        but_list_layout.addWidget(generate_for_selected_button)
        but_list_layout.addWidget(generate_all_button)
        but_list_layout.addWidget(item_info)

        main_layout.addWidget(self.web)

        main_layout.addLayout(but_list_layout)
        self.third_page_stack.setLayout(main_layout)


    def printItemText(self, listWidget):
        items = listWidget.findItems("*", Qt.MatchWildcard)
        s_item = listWidget.selectedItems()
        for i in range(len(items)):
            for t in self.all_objects:
                # higliht
                if len(s_item) != 0:
                    if t.GUI_window_adder() == s_item[0].text():
                        self.web._search_panel.text_fi(t.GUI_highlight_info())
                # if checked
                if items[i].checkState() == 2 and items[i].text() == t.GUI_window_adder() and t not in self.selected_objects:
                    self.selected_objects.append(t)
                    print(self.selected_objects)
                elif items[i].checkState() == 0 and t in self.selected_objects and items[i].text() == t.GUI_window_adder():
                    self.selected_objects.remove(t)


    def table_add_obejct(self, widget, x):
        self.all_objects.append(x)
        item = QListWidgetItem(x.GUI_window_adder())
        item.setCheckState(Qt.Unchecked)
        widget.addItem(item)
        widget.repaint()

    def update_web_combo(self,combobox,web,button,url,listWidget):
        print(combobox.currentIndex())
        self.counter = combobox.currentIndex()
        if self.counter == len(url) - 1:
            button.hide()
        elif button.isHidden() == True and self.counter < len(url):
            button.show()
        if self.valid_url(url[self.counter]):
            web._view.load(QUrl(url[self.counter]))
        else:
            web._view.load(QtCore.QUrl.fromLocalFile(str(url[self.counter])))

        listWidget.clear()
        object_array = pomgen.HTMLFilterer(url[self.counter], pomgen.html_tags)
        for x in object_array:
            self.table_add_obejct(listWidget, x)
        self.selected_objects.clear()
        self.abspath.clear()
        self.abspath = pomgen.get_page_screenshot(url[self.counter])


    def update_counter(self, val):
        # global self.counter
        self.counter = val
        return self.counter

    def table_cleaner(self, web, button, url, listWidget, combo_box):
        self.all_objects.clear()
        self.counter += 1
        combo_box.setCurrentIndex(self.counter)
        if self.counter == len(url) - 1:
            button.hide()
        if self.valid_url(url[self.counter]):
            web._view.load(QUrl(url[self.counter]))
        else:
            web._view.load(QtCore.QUrl.fromLocalFile(str(url[self.counter])))

        listWidget.clear()
        object_array = pomgen.HTMLFilterer(url[self.counter], pomgen.html_tags)
        for x in object_array:
            self.table_add_obejct(listWidget, x)
        self.selected_objects.clear()
        self.abspath.clear()
        self.abspath = pomgen.get_page_screenshot(url[self.counter])

    def item_info_action(self, listWidget, url,abspath):
        s_item = listWidget.selectedItems()
        info_layout = QVBoxLayout()
        if len(s_item) != 0:
            for i in self.all_objects:
                if (s_item[0].text() == i.GUI_window_adder()):
                    msg = QMessageBox()
                    msg.setText(i.GUI_window_more_info())
                    screenshot_loc = i.get_element_screenshot(url, abspath)
                    msg.setWindowTitle("Element Info " + i.GUI_window_adder())

                    label = QLabel()

                    # loading image
                    pixmap = QPixmap(screenshot_loc)

                    # adding image to label
                    label.setPixmap(pixmap)

                    # Optional, resize label to image size
                    label.resize(pixmap.width(),
                                      pixmap.height())
                    info_layout.addWidget(label)
                    msg.setLayout(info_layout)
                    msg.setIconPixmap(pixmap)
                    msg.resize(pixmap.width()+100,pixmap.height()+10)
                    print(screenshot_loc) ## CANNOT FIND FILE EXCEPTION HANDLING
                    returnValue = msg.exec()

    def generate_for_selected_button_action(self, url):
        try:
            for x in self.selected_objects:
                print(x.GUI_window_adder)

            if len(self.selected_objects) != 0:
                pomgen.file_gen(url, self.selected_objects)
                print("called generate for selected")
            else:
                QMessageBox.about(self, "Generated", "No elements were selected")

        except NameError:
            QMessageBox.about(self, "Generated", "Error")

        else:
            QMessageBox.about(self, "Generated", "Generated for selected")

    def generate_all_button_click(self, url):
        print(self.all_objects)
        pomgen.file_gen(url, self.all_objects)
        QMessageBox.about(self, "Generated", "Generated for all")


class Browser(QtWidgets.QMainWindow, ):
    def __init__(self, parent=None):
        super(Browser, self).__init__(parent)
        self._view = QtWebEngineWidgets.QWebEngineView()
        #filter = Filter()
        #self._view.installEventFilter(filter)
        self.setCentralWidget(self._view)
        # self._view.load(QtCore.QUrl())
        self._search_panel = SearchPanel()
        self.search_toolbar = QtWidgets.QToolBar()
        self.search_toolbar.addWidget(self._search_panel)
        self.addToolBar(QtCore.Qt.BottomToolBarArea, self.search_toolbar)
        self._search_panel.searched.connect(self.on_searched)
        self._search_panel.closed.connect(self.search_toolbar.hide)
        self.search_toolbar.hide()
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


    def create_menus(self):
        menubar = self.menuBar()
        menubar.hide()
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
