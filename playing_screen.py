import sys
from PyQt5.QtWidgets import QApplication, QHBoxLayout, QLabel, QTextEdit, QVBoxLayout, QWidget, QPushButton

from card_grid import GameWidget

button_style = """background: rgba(255, 255, 255, 1); 
color: #000; 
font-size: 15px; 
padding: 5px; 
border-radius: 10px; 
border: 2px solid #000; 
width:60px;
font-family:'Courier'"""


class LogWidget(QWidget):
    def __init__(self, emitter, initial_text="") -> None:
        super().__init__()

        self.textArea = QTextEdit(self)
        self.textArea.setReadOnly(True)
        self.textArea.setStyleSheet("font-size: 12px; font-family: Courier;")
        self.layout = QVBoxLayout(self)
        self.textArea.append(initial_text)
        self.layout.addWidget(self.textArea)
        emitter.progress_signal.connect(self.updateTextArea)
        emitter.player_signal.connect(self.resetTextArea)

    def updateTextArea(self, text):
        self.textArea.append(text)

    def resetTextArea(self):
        self.textArea.clear()


class PlayingScreen(QWidget):
    def __init__(self, change_screen_click) -> None:
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
        reset_button = QPushButton("Reset Game", self)
        reset_button.setStyleSheet(button_style)
        reset_button.clicked.connect(self.reset_game)
        quit_button = QPushButton("Quit Game", self)
        quit_button.setStyleSheet(button_style)
        quit_button.clicked.connect(change_screen_click)
        right_layout.addWidget(reset_button)
        right_layout.addWidget(quit_button)

    def reset_game(self):
        # Add code here to start the game when the button is clicked
        self.game_widget.reset_game()
