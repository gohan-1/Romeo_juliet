from ast import main
from distutils.log import Log
from math import log
import sys
from turtle import right

from PyQt5.QtWidgets import QApplication, QHBoxLayout, QLabel, QTextEdit, QVBoxLayout, QWidget

from test import CardGrid


class LogWidget(QWidget):
    def __init__(self, emitter) -> None:
        super().__init__()

        self.textArea = QTextEdit(self)
        self.textArea.setReadOnly(True)
        self.layout = QVBoxLayout(self)
        self.layout.addWidget(self.textArea)
        emitter.progress_signal.connect(self.updateTextArea)

    def updateTextArea(self, text):
        self.textArea.append(text)


class PlayingScreen(QWidget):
    def __init__(self) -> None:
        super().__init__()
        main_layout = QHBoxLayout()
        left_layout = CardGrid()
        main_layout.addWidget(left_layout)
        log_widget = LogWidget(left_layout)
        right_layout = QVBoxLayout()
        right_layout.addWidget(log_widget)
        main_layout.addLayout(right_layout)
        self.setLayout(main_layout)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    screen = PlayingScreen()
    screen.show()

    sys.exit(app.exec_())
