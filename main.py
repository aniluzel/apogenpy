import sys

from PyQt5.QtWidgets import QApplication

import gui


if __name__ == '__main__':
    app = QApplication(sys.argv)
    showMain = gui.Main()
    sys.exit(app.exec_())