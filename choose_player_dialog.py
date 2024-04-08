from PyQt5.QtWidgets import QDialog, QHBoxLayout, QLabel, QMessageBox, QPushButton, QRadioButton, QVBoxLayout


class ChoosePlayerDialog(QMessageBox):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Choose player")
        self.layout = QVBoxLayout()
        message = QLabel("Choose Romeo you want to play")
        self.layout.addWidget(message)
        red = self.addButton('Red Romeo (plays first)')
        black = self.addButton('Black Romeo (plays second)')
        self.setModal(True)
        self.setLayout(self.layout)
