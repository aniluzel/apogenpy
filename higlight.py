from PyQt5 import QtCore, QtGui, QtWidgets, QtWebEngineWidgets

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

    def showEvent(self, event):
        super(SearchPanel, self).showEvent(event)
        self.setFocus(True)

class Browser(QtWidgets.QMainWindow):
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
                self.statusBar().show()
                self.statusBar().showMessage('Not found')
            else:
                self.statusBar().hide()
        self._view.findText(text, flag, callback)

    def create_menus(self):
        menubar = self.menuBar()
        file_menu = menubar.addMenu('&File')
        file_menu.addAction('&Find...', self.search_toolbar.show, shortcut=QtGui.QKeySequence.Find)

if __name__ == '__main__':
    import sys

    app = QtWidgets.QApplication.instance()
    if app is None:
        app = QtWidgets.QApplication(sys.argv)
    w = Browser()
    w.show()
    sys.exit(app.exec_())