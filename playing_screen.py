from ast import main
from distutils.log import Log
from math import log
import sys
from turtle import right
from PyQt5.QtGui import QBrush,  QPixmap, QPainter
from PyQt5.QtWidgets import QApplication, QHBoxLayout, QLabel, QTextEdit, QVBoxLayout, QWidget, QPushButton
from pygame.mixer_music import play

from card_grid import CardGrid


class LogWidget(QWidget):
    def __init__(self, emitter, initial_text="") -> None:
        super().__init__()

        self.textArea = QTextEdit(self)
        self.textArea.setReadOnly(True)
        self.layout = QVBoxLayout(self)
        self.textArea.append(initial_text)
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
        log_widget = LogWidget(
            left_layout, "Welcome to the game!\nClick on the Romeo to move and click to the Joker to swap. \nGood luck!\nRED plays first. ")
        right_layout = QVBoxLayout()
        right_layout.addWidget(log_widget)
        main_layout.addLayout(right_layout)
        self.setLayout(main_layout)
        start_button = QPushButton("Reset Game", self)
        start_button.clicked.connect(self.reset_game)
        right_layout.addWidget(start_button)

    def reset_game(self):
        # Add code here to start the game when the button is clicked
        print('Reset Game ')


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setApplicationName("Romeo and Juliet")
    playing_screen = PlayingScreen()
    playing_screen.show()
    sys.exit(app.exec_())
