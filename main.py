import sys

from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QApplication
from info import Info
from dispay import Display
from main_window import MainWindow
from variables import WINDOW_ICON_PATH

if __name__ == '__main__':
    # Creating the apllication
    app = QApplication(sys.argv)
    window = MainWindow()

    # Defining the icon
    icon = QIcon(str(WINDOW_ICON_PATH))
    window.setWindowIcon(icon)
    window.adjustFixedSize()

    # Info
    info = Info('10 * 10')
    window.addToVLayout(info)
    # Display
    display = Display()
    window.addToVLayout(display)

    # Execute
    window.show()
    app.exec()
