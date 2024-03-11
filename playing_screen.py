import sys
from PyQt5.QtWidgets import QApplication, QHBoxLayout, QLabel, QTextEdit, QVBoxLayout, QWidget, QPushButton

from card_grid import GameWidget


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
        self.game_widget = GameWidget()
        main_layout.addWidget(self.game_widget)
        log_widget = LogWidget(
            self.game_widget, "Welcome to the game!\nClick on the Romeo to move and click to the Joker to swap. \nGood luck!\nRED plays first. ")
        right_layout = QVBoxLayout()
        right_layout.addWidget(log_widget)
        main_layout.addLayout(right_layout)
        self.setLayout(main_layout)
        start_button = QPushButton("Reset Game", self)
        start_button.clicked.connect(self.reset_game)
        right_layout.addWidget(start_button)

    def reset_game(self):
        # Add code here to start the game when the button is clicked
        self.game_widget.reset_game()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setApplicationDisplayName("Romeo and Juliet")
    playing_screen = PlayingScreen()
    playing_screen.show()
    sys.exit(app.exec_())
