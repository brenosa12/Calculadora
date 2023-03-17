from PySide6.QtWidgets import QMainWindow, QVBoxLayout, QWidget, QMessageBox


class MainWindow(QMainWindow):
    def __init__(self, parent: QWidget | None = None, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.central_widget = QWidget()
        self.vLayout = QVBoxLayout()
        self.central_widget.setLayout(self.vLayout)

        self.setCentralWidget(self.central_widget)

        # Para ajustar o tamanho da calculadora

    def adjustFixedSize(self):
        self.adjustSize()
        self.setFixedSize(self.width(), self.height())

    def addWidgetToVLayout(self, widget):
        self.vLayout.addWidget(widget)

    def makeMsgBox(self):
        return QMessageBox(self)
