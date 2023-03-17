from typing import TYPE_CHECKING
from PySide6.QtWidgets import QPushButton, QGridLayout
from variables import MEDIUM_FONT_SIZE
from utils import IsNumOrDot, isEmpty, IsValidNumber
from PySide6.QtCore import Slot
from math import pow
if TYPE_CHECKING:
    from display import Display, Info
    from main_window import MainWindow


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
    def __init__(self, display: 'Display', info: 'Info', window: 'MainWindow',
                 * args, **kwargs):
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
        self.window = window

        self._equation = ''
        self._equationInitialValue = 'Sua Conta'
        self._left = None
        self._right = None
        self._op = None
        self._makeGrid()

        self._equation = self._equationInitialValue

    @property
    def equation(self):
        return self._equation

    @equation.setter
    def equation(self, value):
        self._equation = value
        self.info.setText(value)

    def _makeGrid(self):

        self.display.delPressed.connect(self.display.backspace)
        self.display.clearPressed.connect(self._clear)

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

        if text == '◀':
            self._buttonClicked(button, self.display.backspace)

        if text in '+-/*^':
            self._buttonClicked(button, self._makeSlot(
                self._operatorClicked, button))

        if text == '=':
            self._buttonClicked(button, self._eq)

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
        self._left = None
        self._right = None
        self._op = None
        self.equation = self._equationInitialValue
        self.display.clear()

    # Definition the equation

    def _operatorClicked(self, button):
        buttonText = button.text()
        displayText = self.display.text()
        self.display.clear()

        if not IsValidNumber(displayText) and self._left is None:
            self._showError('Você nao digitou nada.')
            return

        if self._left is None:
            self._left = float(displayText)

        self._op = buttonText
        self.equation = f'{self._left} {self._op} ??'

    # Definition the result

    def _eq(self):
        displayText = self.display.text()

        if not IsValidNumber(displayText):
            self._showError('Operação Incompleta.')

            return

        self._right = float(displayText)
        self.equation = f'{self._left} {self._op} {self._right}'
        result = 'error'
        try:
            if not self._op:
                self._showError('Operação Incompleta.')
                self.equation = f'{self._right}'

            if '^' in self.equation and isinstance(self._left, float):
                result = pow(self._left, self._right)
            else:
                result = eval(self.equation)

        except ZeroDivisionError:
            result = 'Operação Inválida'
            self._showError('Não é possivel dividir por zero.')

        except OverflowError:
            result = 'Operação Inválida'
            self._showError('Operação Inválida')

        self.display.clear()
        self.info.setText(f'{self.equation} = {result}')
        self._left = result
        self._right = None

        if result == 'ERROR':
            self._left = None

    # Show error to user

    def _showError(self, text):
        msgBox = self.window.makeMsgBox()
        msgBox.setText(text)
        msgBox.setIcon(msgBox.Icon.Critical)
        msgBox.exec()
