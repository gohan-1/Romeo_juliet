import sys
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QGridLayout, QLabel, QPushButton
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
        self.button = QPushButton("Click me")  # Button creation moved here

    def card_clicked(self, card):
        print(f"Card clicked {card}")

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
                card_label.setScaledContents(True)
                card_label.mousePressEvent = lambda event, row=row, col=col: self.card_clicked(board[row][col])
                self.grid_layout.addWidget(card_label, row, col)
        
        chess_coin_label = QLabel()
        chess_coin_pixmap = QPixmap("cards/red_coin.png")
        chess_coin_pixmap = chess_coin_pixmap.scaledToWidth(
            64, Qt.TransformationMode.SmoothTransformation)
        chess_coin_label.setPixmap(chess_coin_pixmap)
        self.grid_layout.addWidget(chess_coin_label, 6, 0)

        chess_coin_label = QLabel()
        chess_coin_pixmap = QPixmap("cards/black_coin.png")
        chess_coin_pixmap = chess_coin_pixmap.scaledToWidth(
            64, Qt.TransformationMode.SmoothTransformation)
        chess_coin_label.setPixmap(chess_coin_pixmap)
        self.grid_layout.addWidget(chess_coin_label, 0, 6)



if __name__ == "__main__":
    app = QApplication(sys.argv)
    card_grid = CardGrid(game=Game())
    card_grid.show()
    sys.exit(app.exec_())
