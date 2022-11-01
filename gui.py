from urllib.parse import urlparse
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QUrl, QCoreApplication
from PyQt5.QtWidgets import QApplication, QMainWindow, QLineEdit, QVBoxLayout, QProgressBar, QPushButton, QListWidget, \
    QAbstractItemView, QWidget, QHBoxLayout, QCheckBox, QComboBox, QMessageBox
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWebEngineWidgets import QWebEngineView as QWebView
import sys
import crawl
import pomgen



default_settings = [True, False, 1, 0.92, 0.88, None]
filtered_data = []
class Ui_Main(QtWidgets.QWidget):
    def setupUi(self, Main):
        Main.setObjectName("Main")
        Main.resize(800, 480)
        self.QtStack = QtWidgets.QStackedLayout()


        self.stack1 = QtWidgets.QWidget()
        self.stack2 = QtWidgets.QWidget()
        self.stack3 = QtWidgets.QWidget()
        self.stack4 = QtWidgets.QWidget()
        self.stack1.setWindowTitle("ApogenPy")
        self.stack2.setWindowTitle("ApogenPy")
        self.stack3.setWindowTitle("ApogenPy")
        self.stack4.setWindowTitle("ApogenPy")
        self.first_page()


        self.QtStack.addWidget(self.stack1)
        self.QtStack.addWidget(self.stack2)
        self.QtStack.addWidget(self.stack3)
        self.QtStack.addWidget(self.stack4)

    def first_page(self):

        layout = QVBoxLayout()
        #self.stack1.resize(800, 480)
        label1 = QLabel("Enter the URL of a domain that you want to crawl")
        textbox = QLineEdit()
        textbox.move(20, 20)
        textbox.resize(280, 40)
        #PushButton1#
        PushButton1 = QtWidgets.QPushButton()
        PushButton1.setText("Crawl")
        PushButton1.setGeometry(QtCore.QRect(10, 10, 100, 100))
        PushButton1.clicked.connect(lambda: self.on_click(textbox))

        #PushButton2#
        setting_button = QtWidgets.QPushButton()
        setting_button.setText("Settings")
        setting_button.setGeometry(QtCore.QRect(150, 150, 100, 100))
        setting_button.clicked.connect(self.settings_clicked)

        # PushButton3#
        exit_button = QtWidgets.QPushButton()
        exit_button.setText("Exit")
        exit_button.setGeometry(QtCore.QRect(150, 150, 100, 100))
        exit_button.clicked.connect(QCoreApplication.instance().quit)

        #layout
        layout.addWidget(label1)
        layout.addWidget(textbox)
        layout.addWidget(PushButton1)
        layout.addWidget(setting_button)
        layout.addWidget(exit_button)
        self.stack1.setLayout(layout)


    def settings_clicked(self):
        self.settings()
        self.QtStack.setCurrentIndex(3)

    def update_table_with_arr(self, table, data):
        for i in data:
            table.addItem(i)
        table.repaint()

    def update_table(self, table, data):
        table.addItem(data)
        table.repaint()

    def tableUI(self):
        global filtered_data
        #self.stack2.resize(800, 480)
        data = filtered_data
        table_layout = QVBoxLayout()
        table = QListWidget()
        table.resize(300, 120)
        #update_table(table)
        for i in data:
            print(i)
            table.addItem(i)
        table.setSelectionMode(QAbstractItemView.MultiSelection)
        table.setVerticalScrollMode(QAbstractItemView.ScrollPerPixel)
        table.repaint()
        table.update()
        table.itemClicked.connect(lambda: self.add_selected(table))

        add_url_layout = QHBoxLayout()
        add_url_label = QLabel("Similarity percentage value")
        add_url_textbox = QLineEdit()
        add_url_layout.addWidget(add_url_label)
        add_url_layout.addWidget(add_url_textbox)


        #print(filtered_data )
        #self.table_layout.addWidget()
        #self.stack2.setLayout(self.load_layout)

        sel = QPushButton('Selected')
        all_sel = QPushButton('All')
        add = QPushButton('add url')

        sel.clicked.connect(lambda: self.selected_url_click())
        all_sel.clicked.connect(lambda: self.all_sel_click(data))
        add.clicked.connect(lambda: self.add_click(table,add_url_textbox.text()) )
        #self.all_sel.clicked.connect()
        #self.add.clicked.connect()


        table_layout.addWidget(table)
        table_layout.addLayout(add_url_layout)
        table_layout.addWidget(sel)
        table_layout.addWidget(all_sel)
        table_layout.addWidget(add)

        #if (not self.stack2.layout()):
        self.stack2.setLayout(table_layout)

    def all_sel_click(self,data):
        self.web_list(data)
        self.QtStack.setCurrentIndex(2)

    def add_click(self, table,data):
        self.update_table(table,data)

    def add_selected(self,listWidget):
        items = listWidget.selectedItems()
        global selected
        selected = []
        for i in range(len(items)):
            selected.append(str(listWidget.selectedItems()[i].text()))


    def selected_url_click(self):
        global selected
        self.web_list(selected)
        self.QtStack.setCurrentIndex(2)

    def settings(self):
        self.stack3.resize(800, 480)
        settings_layout = QVBoxLayout()
        #performing sim similarity check
        checkbox_layout = QHBoxLayout()
        sim_check = QCheckBox("Structure Similarity Check")
        sim_check.setChecked(default_settings[0])
        checkbox_layout.addWidget(sim_check)

        #perfroming url similarity check
        url_sim = QCheckBox("URL Similarity Check")
        url_sim.setChecked(default_settings[1])
        checkbox_layout.addWidget(url_sim)
        #
        percentage_layout = QHBoxLayout()
        percentage_sim_label = QLabel("Similarity percentage value")
        percentage_sim_textbox = QLineEdit()
        percentage_layout.addWidget(percentage_sim_label)
        percentage_layout.addWidget(percentage_sim_textbox)
        #
        url_layout =QHBoxLayout()
        percentage_url_label = QLabel("Url Similarity percentage value")
        percentage_url_textbox = QLineEdit()
        url_layout.addWidget(percentage_url_label)
        url_layout.addWidget(percentage_url_textbox)

        domain_layout = QHBoxLayout()
        domain_label = QLabel("Enter domain ")
        domain_textbox = QLineEdit()
        domain_layout.addWidget(domain_label)
        domain_layout.addWidget(domain_textbox)

        combobox1 = QComboBox()
        combobox1.addItem('Joint similarity')
        combobox1.addItem('Structural similarity')
        combobox1.addItem('Style similarity')

        combobox1.setCurrentIndex(default_settings[2])

        save_button = QPushButton("Save and Close")
        save_button.clicked.connect(lambda: self.save_cliked(sim_check.isChecked(),url_sim.isChecked(),combobox1.currentIndex(),percentage_sim_textbox.text(),percentage_url_textbox.text(),domain_textbox.text()))

        settings_layout.addLayout(checkbox_layout)
        settings_layout.addLayout(percentage_layout)
        settings_layout.addLayout(url_layout)
        settings_layout.addLayout(domain_layout)
        settings_layout.addWidget(combobox1)
        settings_layout.addWidget(save_button)
        self.stack4.setLayout(settings_layout)


    def save_cliked(self,sim, url, index,per_sim,per_url,dom):
        #print("saved")
        default_settings[0] = sim
        default_settings[1] = url
        default_settings[2] = index
        if per_sim != '':
            default_settings[3] = per_sim
        if per_url != '':
            default_settings[4] = per_url
        default_settings[5] = dom
        self.QtStack.setCurrentIndex(0)


    from urllib.parse import urlparse

    def valid_url(self,to_validate: str) -> bool:
        o = urlparse(to_validate)
        return True if o.scheme and o.netloc else False


    def on_click(self,textbox):
        global filtered_data
        self.QtStack.setCurrentIndex(1)
        c = crawl.CrawlerProcess({})
        #url validation
        try:
            if self.valid_url(textbox.text()):
                c.crawl(crawl.CrawlingSpider, start_urls=[textbox.text()], allowed_domains=default_settings[5])
                c.start()

                # filtering
                filtered_data = crawl.sim_check(data=crawl.crawled_links, check_sim=default_settings[0],
                                                check_url_sim=default_settings[1], param=default_settings[2],
                                                web_page_similarity_percentage=default_settings[3],
                                                web_path_similarity_percentage=default_settings[4])

                self.tableUI()
            else:
                self.QtStack.setCurrentIndex(0)
                QMessageBox.about(self, "Error", "Url is not valid")
        except Exception as e:
            QMessageBox.about(self, "Error has acquired", e)


    def web_list(self,url):
        global counter
        counter = 0
        listWidget = QListWidget()
        web = QWebView()
        web.load(QUrl(url[counter]))
        data = pomgen.elemfinder(url[counter])
        next_button = QPushButton('Next page')
        generate_button = QPushButton('Generate for selected')
        gen_all_button = QPushButton('Generate all for this page')
        current_url_label = QLabel("Elements of "+url[counter])

        next_button.clicked.connect(lambda: self.table_cleaner(web, next_button, url, listWidget, counter,current_url_label))
        generate_button.clicked.connect(lambda: self.generate_button_clicked(url[counter]))
        gen_all_button.clicked.connect(lambda: self.gen_all_button_cliked(url[counter]))
        if(len(url) == 1):
            next_button.hide()


        main_layout = QHBoxLayout()
        but_list_layout = QVBoxLayout()
        but_list_layout.addWidget(current_url_label)
        but_list_layout.addWidget(listWidget)
        but_list_layout.addWidget(next_button)
        but_list_layout.addWidget(generate_button)
        but_list_layout.addWidget(gen_all_button)

        main_layout.addWidget(web)

        listWidget.resize(300, 120)
        self.add_item_windget(listWidget, data)
        listWidget.setSelectionMode(QAbstractItemView.MultiSelection)
        listWidget.setVerticalScrollMode(QAbstractItemView.ScrollPerPixel)
        listWidget.itemClicked.connect(lambda: self.printItemText(listWidget))


        main_layout.addLayout(but_list_layout)
        self.stack3.setLayout(main_layout)

    def update_counter(self,val):
        global counter
        counter = val
        return counter

    def table_cleaner(self,web, button, url, listWidget, counter,current_url_label):
        if counter == len(url) - 1:
            button.hide()
        else:
            counter += 1
            web.load(QUrl(url[counter]))
            data = pomgen.elemfinder(url[counter])
            listWidget.clear()
            for i in data:
                listWidget.addItem(i)
                listWidget.repaint()
        # print("next button clicked")
        current_url_label.setText("Elements of "+url[counter])
        self.update_counter(counter)

    def printItemText(self,listWidget):
            items = listWidget.selectedItems()
            global selected
            selected = []
            for i in range(len(items)):
                selected.append(str(listWidget.selectedItems()[i].text()))

    def generate_button_clicked(self,url):
        global selected
       # for item in selected:
        print(selected)
        pomgen.file_gen(url,selected) #### burası fixlencek
        #print("generated for ", item)

    def gen_all_button_cliked(self,data):
        # data takes url
        pomgen.file_gen(data,pomgen.elemfinder(data))
        ####burası fixlencek
        #print(i)

    def add_item_windget(self, windget, data):
        for i in data:
            windget.addItem(i)

class Main(QMainWindow, Ui_Main):
    def __init__(self, parent=None):
        super(Main, self).__init__(parent)
        self.setupUi(self)

def gui_start():
    app = QApplication(sys.argv)
    showMain = Main()
    sys.exit(app.exec_())