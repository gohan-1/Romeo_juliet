import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QLabel

class OpeningScreen(QMainWindow):
    def _init_(self):
        super()._init_()
        self.initUI()

    def initUI(self):
        # Set window properties
        self.setWindowTitle('Romeo Game')
        self.setGeometry(100, 100, 800, 600)

        # Create a central widget and layout
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        # Add a title label
        title_label = QLabel('Welcome to Romeo Game', self)
        title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(title_label)

        # Add a start game button
        start_button = QPushButton('Start Game', self)
        start_button.clicked.connect(self.start_game)
        layout.addWidget(start_button)

    def start_game(self):
        # Implement logic to start the game
        print("Starting the game...")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    opening_screen = OpeningScreen()
    opening_screen.show()
    sys.exit(app.exec_())