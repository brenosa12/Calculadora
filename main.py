import sys

from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QApplication

from buttons import ButtonGrid
from display import Display, Info, setupTheme
from main_window import MainWindow
from variables import WINDOW_ICON_PATH

if __name__ == '__main__':
    # Creating the apllication
    app = QApplication(sys.argv)
    setupTheme()
    window = MainWindow()

    # Defining the icon
    icon = QIcon(str(WINDOW_ICON_PATH))
    window.setWindowIcon(icon)

    # Info
    info = Info('')
    window.addWidgetToVLayout(info)

    # Display
    display = Display()
    window.addWidgetToVLayout(display)

    # Grid of Buttons
    buttonsGrid = ButtonGrid(display, info)
    window.vLayout.addLayout(buttonsGrid)

    # Ajust
    window.adjustFixedSize()

    # Execute
    window.show()
    app.exec()
