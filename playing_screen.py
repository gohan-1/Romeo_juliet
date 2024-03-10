from ast import main
from distutils.log import Log
from math import log
import sys
from turtle import right
from PyQt5.QtGui import QBrush,  QPixmap, QPainter
from PyQt5.QtWidgets import QApplication, QHBoxLayout, QLabel, QTextEdit, QVBoxLayout, QWidget,QPushButton

from test import CardGrid


class InitialScreen(QWidget):
    def __init__(self) -> None:
        super().__init__()
        layout = QVBoxLayout(self)
        self.setWindowTitle("Initial Screen")
        image_label = QLabel(self)
        pixmap = QPixmap("assets/coins/image.png").scaled(700, 600) # Replace "path/to/your/image.png" with the path to your image
        image_label.setPixmap(pixmap)
        image_label.mousePressEvent = self.start_game
        layout.addWidget(image_label)

    def start_game(self, event):
        # Switch to the game screen when the image is clicked
        self.game_screen = PlayingScreen()
        self.game_screen.show()
        self.close()


class LogWidget(QWidget):
    def __init__(self, emitter,initial_text="") -> None:
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
        self.setWindowTitle("Game Screen")
        main_layout = QHBoxLayout()
        left_layout = CardGrid()
        main_layout.addWidget(left_layout)
        log_widget = LogWidget(left_layout,"Welcome to the game! \n Current Player RED")
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
        

def update_current_player(self):
        self.current_player_label.setText(f'Current Player: {self.card_grid.game.current_player.name}')


if __name__ == "__main__":
    app = QApplication(sys.argv)
    initial_screen = InitialScreen()
    initial_screen.show()
    sys.exit(app.exec_())