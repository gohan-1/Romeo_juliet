from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor, QLinearGradient, QPainter, QPixmap
from PyQt5.QtWidgets import QGraphicsOpacityEffect, QHBoxLayout, QPushButton, QVBoxLayout, QWidget
button_style = """background: rgba(255, 255, 255, .9); 
color: #000; 
font-size: 20px; 
padding: 10px; 
border-radius: 10px; 
border: 2px solid #000; 
width:250px;
font-family:'Courier'"""


class OpeningScreen(QWidget):
    def __init__(self, handle_button_click, handle_ai_button_click):
        super().__init__()
        hbox = QHBoxLayout(self)
        layout = QVBoxLayout()
        hbox.addLayout(layout)
        hbox.setAlignment(Qt.AlignCenter)
        self.play_button = QPushButton('Play in turn', self)
        self.play_button.setStyleSheet(button_style)
        self.play_button.clicked.connect(handle_button_click)

        self.play_ai_button = QPushButton('Play with machine', self)
        self.play_ai_button.setStyleSheet(button_style)
        self.play_ai_button.clicked.connect(handle_ai_button_click)
        layout.addWidget(self.play_button)
        layout.addWidget(self.play_ai_button)

        self.setLayout(hbox)

    def paintEvent(self, a0):
        painter = QPainter(self)
        pixmap = QPixmap('assets/card.png')
        pixmap = pixmap.scaled(
            self.size(), Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation)
        painter.drawPixmap(0, 0, pixmap)
