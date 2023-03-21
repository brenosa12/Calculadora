from PySide6.QtWidgets import QLineEdit, QLabel
from variables import BIG_FONT_SIZE, TEXT_MARGIN, MINIMUM_WIDHT
from variables import DARKER_PRIMARY_COLOR, DARKEST_PRIMARY_COLOR
from variables import PRIMARY_COLOR, SMALL_FONT_SIZE
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QKeyEvent
import qdarktheme
from utils import isEmpty, isNumOrDot


class Display(QLineEdit):
    eqTried = Signal()
    delPressed = Signal()
    clearPressed = Signal()
    inputPressed = Signal(str)
    operatorPressed = Signal(str)
    invertPressed = Signal()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.configStyle()

    def configStyle(self):
        self.setStyleSheet(f'font-size:{BIG_FONT_SIZE}px')
        self.setMinimumHeight(BIG_FONT_SIZE*2)
        self.setMinimumWidth(MINIMUM_WIDHT)
        self.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.setTextMargins(*[TEXT_MARGIN for text in range(4)])

    # Config the  key receptor

    def keyPressEvent(self, event: QKeyEvent) -> None:
        text = event.text().strip()
        key = event.key()
        KEYS = Qt.Key

        isEnter = key in [KEYS.Key_Enter, KEYS.Key_Return, KEYS.Key_Equal]
        isDel = key in [KEYS.Key_Delete, KEYS.Key_Backspace]
        isEsc = key in [KEYS.Key_Escape]
        isOperator = key in [KEYS.Key_Plus, KEYS.Key_Minus, KEYS.Key_Slash,
                             KEYS.Key_Asterisk, KEYS.Key_P]
        isInvert = key in [KEYS.Key_N]

        if isEnter:
            self.eqTried.emit()
            return event.ignore()

        if isDel:

            self.delPressed.emit()
            return event.ignore()

        if isEsc:
            self.clearPressed.emit()
            return event.ignore()

        if isEmpty(text):
            return event.ignore()

        if isNumOrDot(text):

            self.inputPressed.emit(text)
            return event.ignore()

        if isOperator:
            if text.lower() == 'p':
                text = '^'
            self.operatorPressed.emit(text)
            return event.ignore()

        if isInvert:
            self.invertPressed.emit()
            return event.ignore()


# Setup theme
qss = f"""
    QPushButton[cssClass="specialButton"] {{
        color: #fff;
        background: {PRIMARY_COLOR};
    }}
    QPushButton[cssClass="specialButton"]:hover {{
        color: #fff;
        background: {DARKER_PRIMARY_COLOR};
    }}
    QPushButton[cssClass="specialButton"]:pressed {{
        color: #fff;
        background: {DARKEST_PRIMARY_COLOR};
    }}
"""


def setupTheme():
    qdarktheme.setup_theme(
        theme='dark',
        corner_shape='rounded',
        custom_colors={"[dark]": {
            "primary": f"{PRIMARY_COLOR}",
        }, "[light]": {"primary": f"{PRIMARY_COLOR}",
                       }}, additional_qss=qss
    )


# Info from the top

class Info(QLabel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.configStyle()

    def configStyle(self):
        self.setStyleSheet(f'font-size: {SMALL_FONT_SIZE}px ')
        self.setAlignment(Qt.AlignmentFlag.AlignRight)
