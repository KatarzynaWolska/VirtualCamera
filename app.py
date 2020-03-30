from display_module.display import MainWindow
from file_module.file_handler import FileHandler
from PyQt5.QtWidgets import (QApplication)
import sys


def main():
    fileHandler = FileHandler()
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()