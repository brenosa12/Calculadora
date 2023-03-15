from typing import TYPE_CHECKING
from PySide6.QtWidgets import QPushButton, QGridLayout
from variables import MEDIUM_FONT_SIZE
from utils import IsNumOrDot, isEmpty, IsValidNumber
from PySide6.QtCore import Slot

if TYPE_CHECKING:
    from display import Display, Info


class Button(QPushButton):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.configStyle()

    def configStyle(self):
        font = self.font()
        font.setPixelSize(MEDIUM_FONT_SIZE)
        self.setFont(font)
        self.setMinimumSize(75, 75)


class ButtonGrid(QGridLayout):
    def __init__(self, display: 'Display', info: 'Info', *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._gridMask = [
            ['C', '◀', '^', '/'],
            ['7', '8', '9', '*'],
            ['4', '5', '6', '-'],
            ['1', '2', '3', '+'],
            ['',  '0', '.', '='],
        ]
        self.display = display
        self.info = info
        self._equation = ''
        self._makeGrid()

    @property
    def equation(self):
        return self._equation

    @equation.setter
    def equation(self, value):
        self._equation = value
        self.info.setText(value)

    def _makeGrid(self):
        for i, row in enumerate(self._gridMask):
            for j, buttonText in enumerate(row):
                button = Button(buttonText)
                if not IsNumOrDot(buttonText) and not isEmpty(buttonText):
                    button.setProperty('cssClass', 'specialButton')
                    self._configSpecialButton(button)
                self.addWidget(button, i, j)
                slot = self._makeSlot(self._insertTextToDisplay,
                                      button)
                self._buttonClicked(button, slot)

    def _buttonClicked(self, button, slot):
        button.clicked.connect(slot)  # type: ignore

    def _configSpecialButton(self, button):
        text = button.text()

        if text == 'C':
            self._buttonClicked(button, self._clear)

    # Make the real slot
    def _makeSlot(self, func, *args, **kwargs):
        @Slot()
        def realSlot(_):
            func(*args, **kwargs)
        return realSlot

    # Insert the Text of Button in Display
    def _insertTextToDisplay(self, button):
        buttonText = button.text()
        newDisplayValue = self.display.text() + buttonText

        if not IsValidNumber(newDisplayValue):
            return

        self.display.insert(buttonText)

    def _clear(self):
        self.display.clear()
