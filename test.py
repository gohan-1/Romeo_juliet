import sys
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QGridLayout, QLabel
from PyQt5.QtGui import QPixmap

from game import Game


class CardGrid(QWidget):
    def __init__(self, parent=None, game: Game = None):
        super().__init__(parent)

        self.setWindowTitle("Card Grid")
        self.setGeometry(80, 80, 1000, 1000)

        self.grid_layout = QGridLayout()
        self.setLayout(self.grid_layout)

        self.create_grid(game)
        self.resize(600, 600)

    def create_grid(self, game: Game):
        board = game.board
        for row in range(game.MATRIX_SIZE):
            for col in range(game.MATRIX_SIZE):
                card = board[row][col]
                card_label = QLabel(str(card))
                pixmap = QPixmap(card.get_image_path())
                pixmap = pixmap.scaledToWidth(
                    64, Qt.TransformationMode.SmoothTransformation)
                card_label.setPixmap(pixmap)
                self.grid_layout.addWidget(card_label, row, col)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    card_grid = CardGrid(game=Game())
    card_grid.show()
    sys.exit(app.exec_())
