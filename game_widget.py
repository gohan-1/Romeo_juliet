from enum import Enum
from PyQt5.QtCore import QObject, QThread, Qt, pyqtSignal
from PyQt5.QtWidgets import QWidget, QGridLayout, QLabel, QMessageBox
from PyQt5.QtGui import QBrush,  QPixmap, QPainter

from alpha_beta_pruning import AlphaBetaPruningPlayer
from game import Game, TurnType
from player import PlayerType
from position import Position
from random_ai import RandomAIPlayer
from turn import Turn


class GameMode(Enum):
    NORMAL = 1
    AI = 2


class GameWidget(QWidget):
    progress_signal = pyqtSignal(str)
    player_signal = pyqtSignal(str)

    def __init__(self, parent=None, game: Game = None, mode: GameMode = GameMode.NORMAL, to_home_screen=None):
        super().__init__(parent)

        if game is None:
            game = Game()

        self.setWindowTitle("Romeo and Juliet")
        self.grid_layout = QGridLayout()
        self.grid_layout.setSpacing(3)
        self.setLayout(self.grid_layout)

        self.game = game
        self.ai_player = AlphaBetaPruningPlayer()
        self.ai_player_color = PlayerType.BLACK
        self.mode = mode
        self.is_move = False
        self.is_swap = False
        self.possible_clicks = []
        self.picked_joker = None
        self.create_grid()
        self.to_home_screen = to_home_screen
        if self.mode == GameMode.AI and self.ai_player_color == PlayerType.RED:
            self.make_ai_move()

    def evaluate_current_player_postion(self):
        msg = QMessageBox()
        msg.setWindowTitle("Game Finished")
        msg.setStandardButtons(QMessageBox.Ok)
        msg.buttonClicked.connect(self.to_home_screen)
        if self.game.red_player.position == self.game.BLACK_INITIAL_POSITION:
            self.progress_signal.emit(
                "<span style='color: red'><b>RED wins</b></span>")
            msg.setText("RED wins")
            msg.exec_()
        elif self.game.black_player.position == self.game.RED_INITAL_POSTION:
            self.progress_signal.emit(
                "<span style='color: black'><b>BLACK wins</b></span>")
            msg.setText("BLACK wins")
            msg.exec_()
        else:
            self.emit_progress_signal(
                f"It's {self.game.current_player.name}'s turn")

    def make_ai_move(self):
        if not self.game.current_player.color == self.ai_player_color:
            return

        def handle_ai_move(turn: Turn):
            if turn is None:
                self.progress_signal.emit("AI cannot make a move")
                return
            if turn.type == TurnType.MOVE:
                self.perform_move(turn.end)
            elif turn.type == TurnType.SWAP:
                self.perform_swap(turn.start, turn.end)

            self.create_grid()
            self.evaluate_current_player_postion()

        self.thread = QThread()
        self.worker = Worker()
        self.worker.moveToThread(self.thread)
        self.thread.started.connect(
            lambda: self.worker.run(self.ai_player, self.game))
        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)
        self.worker.finished.connect(handle_ai_move)

        self.thread.start()

    def reset_game(self, mode: GameMode = None, ai_player_color: PlayerType = None):
        self.game = Game()
        if mode is not None:
            self.mode = mode
        if ai_player_color is not None:
            self.ai_player_color = ai_player_color
        self.is_move = False
        self.is_swap = False
        self.possible_clicks = []
        self.picked_joker = None
        self.player_signal.emit("a")
        self.progress_signal.emit(
            "Welcome to the game!\nClick on the Romeo to move and click to the Joker to swap. \nGood luck!")
        self.emit_progress_signal('RED plays first')
        self.create_grid()
        if self.mode == GameMode.AI and self.ai_player_color == PlayerType.RED:
            self.make_ai_move()

    def emit_progress_signal(self, text, is_instruction=False):
        if is_instruction:
            color = 'black'
        else:
            color = 'red' if self.game.current_player.color == PlayerType.RED else 'blue'
        full_string = f"<span style='color: {color}'>{text}</span>"
        self.progress_signal.emit(full_string)

    def perform_move(self, position: Position):
        self.emit_progress_signal(
            f'{self.game.current_player.name} moved from {self.game.current_player.position} to {position}')
        self.game.perform_move(position)

    def card_clicked(self, position_x, position_y, event):
        # self.progress_signal.emit(
        #     f'You clicked {self.game.board[position_x][position_y]}')

        if self.is_move and Position(position_x, position_y) == self.game.current_player.position:
            self.is_move = False
            self.is_swap = False
            self.possible_clicks = []
            self.create_grid()
            return
        if self.is_move and Position(position_x, position_y) in self.possible_clicks:
            self.perform_move(Position(position_x, position_y))
            self.is_move = False
            self.is_swap = False
            self.possible_clicks = []
            self.create_grid()
            self.evaluate_current_player_postion()
            if self.mode == GameMode.AI:
                self.make_ai_move()
            return
        if self.is_swap and Position(position_x, position_y) == self.picked_joker:
            self.is_move = False
            self.is_swap = False
            self.possible_clicks = []
            self.create_grid()
            return
        if self.is_swap and Position(position_x, position_y) in self.possible_clicks:
            self.perform_swap(self.picked_joker,
                              Position(position_x, position_y))
            self.is_move = False
            self.is_swap = False
            self.possible_clicks = []
            self.create_grid()
            self.evaluate_current_player_postion()
            if self.mode == GameMode.AI:
                self.make_ai_move()
            return
        current_player_position = self.game.current_player.position
        if current_player_position.x == position_x and current_player_position.y == position_y:
            possible_moves = self.game.list_possible_moves_for_current_player()
            if len(possible_moves) == 0:
                self.emit_progress_signal(
                    "No possible moves for the current player.")
                self.is_move = False
                self.is_swap = False
                self.possible_clicks = []
                return
            self.highlight_cards(possible_moves)
            self.possible_clicks = possible_moves
            self.is_move = True
            self.is_swap = False
            return
        position = self.is_joker_position(position_x, position_y)
        if position is not None:
            self.picked_joker = position
            possible_swaps = self.game.list_possible_swaps(position)
            if len(possible_swaps) == 0:
                self.emit_progress_signal(
                    "No possible swaps for this joker.")
                self.is_move = False
                self.is_swap = False
                self.possible_clicks = []
                return
            self.highlight_cards(possible_swaps)
            self.possible_clicks = possible_swaps
            self.is_swap = True
            self.is_move = False
            return

        self.show_message()

    def perform_swap(self, joker_position, new_joker_position):
        self.emit_progress_signal(
            f'{self.game.current_player.name} swapped Joker from {joker_position} to {new_joker_position}')
        self.game.perform_swap(
            joker_position, new_joker_position)

    def show_message(self):
        if self.is_move:
            # show in screen
            self.emit_progress_signal(
                "Cannot move to this position. Please select highlighted card or click Romeo again to change.")

        elif self.is_swap:
            # show in screen
            self.emit_progress_signal(
                "This card is not swappable. Please select another card or click joker again to change.")
        else:
            self.emit_progress_signal("Invalid click")

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
        if len(joker_positions) == 0:
            self.progress_signal.emit("No joker to swap")
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


class Worker(QObject):
    finished = pyqtSignal(Turn)

    def run(self, player, game):
        decision = player.make_decision(game)
        self.finished.emit(decision)
