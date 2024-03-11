from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QLabel, QVBoxLayout, QWidget

from playing_screen import PlayingScreen


class OpeningScreen(QWidget):
    def __init__(self) -> None:
        super().__init__()
        layout = QVBoxLayout(self)
        image_label = QLabel(self)
        pixmap = QPixmap("assets/coins/image.png").scaled(700, 600)
        image_label.setPixmap(pixmap)
        image_label.mousePressEvent = self.start_game
        layout.addWidget(image_label)

    def start_game(self, event):
        # Switch to the game screen when the image is clicked
        self.game_screen = PlayingScreen()
        self.game_screen.show()
        self.close()
