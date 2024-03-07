import sys
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtWidgets import QApplication,  QWidget, QGridLayout, QLabel
from PyQt5.QtGui import QBrush,  QPixmap, QPainter

from game import Game
from position import Position


class CardGrid(QWidget):
    progress_signal = pyqtSignal(str)
    player_signal = pyqtSignal(str)

    def __init__(self, parent=None, game: Game = None):
        super().__init__(parent)

        if game is None:
            game = Game()

        self.setWindowTitle("Romeo and Juliet")
        self.grid_layout = QGridLayout()
        self.grid_layout.setSpacing(3)
        self.setLayout(self.grid_layout)

        self.game = game
        self.is_move = False
        self.is_swap = False
        self.possible_clicks = []
        self.picked_joker = None
        self.create_grid()

    def card_clicked(self, position_x, position_y, event):
        self.progress_signal.emit(
            f'clicked {self.game.board[position_x][position_y]}')
        if self.is_move and Position(position_x, position_y) in self.possible_clicks:
            self.game.perform_move(Position(position_x, position_y))
            self.is_move = False
            self.is_swap = False
            self.possible_clicks = []
            self.create_grid()
            self.place_red_romeo()
            self.place_black_romeo()
            return
        if self.is_swap and Position(position_x, position_y) == self.picked_joker:
            self.is_move = False
            self.is_swap = False
            self.possible_clicks = []
            self.create_grid()
            return
        if self.is_swap and Position(position_x, position_y) in self.possible_clicks:
            self.game.perform_swap(
                self.picked_joker, Position(position_x, position_y))
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
            self.is_swap = False
            return
        position = self.is_joker_position(position_x, position_y)
        if position is not None:
            self.picked_joker = position
            possible_swaps = self.game.list_possible_swaps(position)
            self.highlight_cards(possible_swaps)
            self.possible_clicks = possible_swaps
            self.is_swap = True
            self.is_move = False
            return

        self.show_message()

    def show_message(self):
        if self.is_move:
            # show in screen
            self.progress_signal.emit("Invalid move")
        elif self.is_swap:
            # show in screen
            self.progress_signal.emit(
                "This card is not swappable. Please select another card or click joker again to change.")
        else:
            self.progress_signal.emit("Invalid click")

    def highlight_cards(self, positions):
        game = self.game
        for position in self.possible_clicks:
            card = self.grid_layout.itemAtPosition(
                position.x, position.y).widget()
            original_pixmap = QPixmap(
                game.board[position.x][position.y].get_image_path())
            original_pixmap = original_pixmap.scaledToWidth(
                64, Qt.TransformationMode.SmoothTransformation)
            card.setPixmap(original_pixmap)

        for position in positions:
            card = self.grid_layout.itemAtPosition(
                position.x, position.y).widget()
            original_pixmap = QPixmap(
                game.board[position.x][position.y].get_image_path())
            original_pixmap = original_pixmap.scaledToWidth(
                64, Qt.TransformationMode.SmoothTransformation)
            result_pixmap = QPixmap(original_pixmap.size())
            result_pixmap.fill(Qt.transparent)

            painter = QPainter(result_pixmap)
            painter.drawPixmap(0, 0, original_pixmap)
            painter.setOpacity(0.2)  # Set opacity to 50%
            painter.setBrush(QBrush(Qt.red, Qt.SolidPattern))
            # Draw a rectangle covering the entire pixmap
            painter.drawRect(result_pixmap.rect())
            painter.end()
            card.setPixmap(result_pixmap)

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
                item = self.grid_layout.itemAtPosition(row, col)

                if item is None:
                    card_label = QLabel(str(card))
                    card_label.setStyleSheet("border: 1px solid black")
                    self.grid_layout.addWidget(card_label, row, col)
                else:
                    card_label = item.widget()
                    self.grid_layout.addWidget(card_label, row, col)

                pixmap = QPixmap(card.get_image_path())
                pixmap = pixmap.scaledToWidth(
                    64, Qt.TransformationMode.SmoothTransformation)
                card_label.setPixmap(pixmap)  # Set or update pixmap
                # card_label.setScaledContents(True)

                card_label.mousePressEvent = lambda event, row=row, col=col: self.card_clicked(
                    row, col, event)

        self.place_red_romeo()
        self.place_black_romeo()

    def place_red_romeo(self):
        game = self.game
        red_position = game.red_player.position

        item = self.grid_layout.itemAtPosition(red_position.x, red_position.y)
        card_label = item.widget()

        red_coin = QPixmap("assets/coins/red_coin.svg")
        red_coin = red_coin.scaledToWidth(
            54, Qt.TransformationMode.SmoothTransformation)

        painter = QPainter(card_label.pixmap())
        painter.setCompositionMode(QPainter.CompositionMode_SourceOver)
        painter.drawPixmap(5, 20, red_coin)
        painter.end()

    def place_black_romeo(self):
        game = self.game
        black_position = game.black_player.position

        item = self.grid_layout.itemAtPosition(
            black_position.x, black_position.y)
        card_label = item.widget()

        coin = QPixmap("assets/coins/black_coin.svg")
        coin = coin.scaledToWidth(
            54, Qt.TransformationMode.SmoothTransformation)

        painter = QPainter(card_label.pixmap())
        painter.setCompositionMode(QPainter.CompositionMode_SourceOver)
        painter.drawPixmap(5, 20, coin)
        painter.end()
