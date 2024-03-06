import re
import sys
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QGridLayout, QLabel, QPushButton,QGraphicsOpacityEffect
from PyQt5.QtGui import QPixmap

from game import Game
from position import Position


class CardGrid(QWidget):
    def __init__(self, parent=None, game: Game = None):
        super().__init__(parent)
        if game is None:
            game = Game()
        self.setWindowTitle("Card Grid")
        self.setGeometry(80, 80, 1000, 1000)
        self.game = game
        self.is_move = False
        self.is_swap = False
        self.possible_clicks = []
        self.grid_layout = QGridLayout()
        self.setLayout(self.grid_layout)

        self.create_grid()
        self.red_romeo()
        self.black_romeo()
        self.resize(600, 600)
        self.button = QPushButton("Click me")  # Button creation moved here

    def card_clicked(self, position_x, position_y, event):
        print(f"position clicked {position_x} {position_y}")
        if self.is_move and Position(position_x, position_y) in self.possible_clicks:
            self.game.perform_move(Position(position_x, position_y))
            self.is_move = False
            self.is_swap = False
            self.possible_clicks = []
            self.create_grid()
            self.red_romeo()
            self.black_romeo()
           
            return
        if self.is_swap and Position(position_x, position_y) in self.possible_clicks:
            self.game.perform_swap(Position(position_x, position_y))
            self.is_move = False
            self.is_swap = False
            self.possible_clicks = []
            self.create_grid()
            return
        current_player_position = self.game.current_player.position
        if current_player_position.x == position_x and current_player_position.y == position_y:
            possible_moves = self.game.list_possible_moves_for_current_player()
            self.highlight_cards(possible_moves)
            self.possible_clicks = possible_moves
            self.is_move = True
            return
        position = self.is_joker_position(position_x, position_y)
        if position is not None:
            possible_swaps = self.game.list_possible_swaps(position)
            self.highlight_cards(possible_swaps)
            self.possible_clicks = possible_swaps
            self.is_swap = True
            return

        self.show_message()

    def show_message(self):
        if self.is_move:
            # show in screen
            print("Invalid move")
        elif self.is_swap:
            # show in screen
            print("Invalid swap")
        else:
            print("Invalid click")

    def highlight_cards(self, positions):
        game = self.game
        board = game.board  
        for row in range(game.MATRIX_SIZE):
            for col in range(game.MATRIX_SIZE):
                found = False
                for position in positions:
                    if position.x == row and position.y == col:
                        found = True
                        break
                if not found:
                    cell_widget = self.grid_layout.itemAtPosition(row, col).widget()
                    opacity_effect = QGraphicsOpacityEffect()
                    opacity_effect.setOpacity(0.5)  # Adjust opacity as needed
                    cell_widget.setGraphicsEffect(opacity_effect)
                    cell_widget.setStyleSheet("background-color: yellow;")
       
          
            # QTimer.singleShot(1000, lambda: cell_widget.setGraphicsEffect(None))

    def is_joker_position(self, position_x, position_y):
        joker_positions = self.game.get_swappable_jokers()
        for position in joker_positions:
            if position.x == position_x and position.y == position_y:
                return position
        return None

    def create_grid(self):
        game = self.game
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
                card_label.mousePressEvent = lambda event, row=row, col=col: self.card_clicked(
                    row, col, event)
                self.grid_layout.addWidget(card_label, row, col)

    def red_romeo(self):  
        game = self.game
        board = game.board     
        red_position = game.red_player.position
        red_lable = QLabel()
        red_pixmap = QPixmap("assets/coins/red_coin.png")
        red_pixmap = red_pixmap.scaledToWidth(
            64, Qt.TransformationMode.SmoothTransformation)
        red_lable.mousePressEvent = lambda event: self.card_clicked(
            red_position.x, red_position.y, event)
        red_lable.setPixmap(red_pixmap)
        self.grid_layout.addWidget(red_lable, red_position.x, red_position.y)
    def black_romeo(self):
        game = self.game
        board = game.board  
        black_position = game.black_player.position
        black_lable = QLabel()
        black_pixmap = QPixmap("assets/coins/black_coin.png")
        black_pixmap = black_pixmap.scaledToWidth(
            64, Qt.TransformationMode.SmoothTransformation)
        black_lable.mousePressEvent = lambda event: self.card_clicked(
            black_position.x, black_position.y, event)
        black_lable.setPixmap(black_pixmap)
        self.grid_layout.addWidget(
            black_lable, black_position.x, black_position.y)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    card_grid = CardGrid(game=Game())
    card_grid.show()
    sys.exit(app.exec_())
