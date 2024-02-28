import sys
import os
from PyQt5.QtWidgets import QApplication, QWidget, QGridLayout, QLabel
from PyQt5.QtGui import QPixmap

class CardGrid(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Card Grid")
        self.setGeometry(80, 80, 1000, 1000)

        self.grid_layout = QGridLayout()
        self.setLayout(self.grid_layout)

        self.create_grid()

    def create_grid(self):
        # Load card images from the "cardss" folder and add them to the grid
        path = "cards"
        for i, filename in enumerate(os.listdir(path)):
            row = i // 7
            col = i % 7

            card_label = QLabel(self)
            pixmap = QPixmap(os.path.join(path, filename))
            pixmap = pixmap.scaledToWidth(55) 
            card_label.setPixmap(pixmap)
            self.grid_layout.addWidget(card_label, row, col)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    card_grid = CardGrid()
    card_grid.show()
    sys.exit(app.exec_())
