from PySide6.QtWidgets import QLineEdit, QLabel
from variables import BIG_FONT_SIZE, TEXT_MARGIN, MINIMUM_WIDHT
from variables import DARKER_PRIMARY_COLOR, DARKEST_PRIMARY_COLOR
from variables import PRIMARY_COLOR, SMALL_FONT_SIZE
from PySide6.QtCore import Qt
import qdarktheme


class Display(QLineEdit):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.configStyle()

    def configStyle(self):
        self.setStyleSheet(f'font-size:{BIG_FONT_SIZE}px')
        self.setMinimumHeight(BIG_FONT_SIZE*2)
        self.setMinimumWidth(MINIMUM_WIDHT)
        self.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.setTextMargins(*[TEXT_MARGIN for text in range(4)])


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
