from PyQt5 import QtWidgets

from opening_screen import OpeningScreen
from playing_screen import PlayingScreen


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.stackedWidget = QtWidgets.QStackedWidget(self)
        self.setCentralWidget(self.stackedWidget)
        self.firstScreen = OpeningScreen(self.switchToSecondScreen)
        self.secondScreen = PlayingScreen(self.switchToFirstScreen)
        self.stackedWidget.addWidget(self.firstScreen)
        self.stackedWidget.addWidget(self.secondScreen)

    def switchToSecondScreen(self):
        self.secondScreen.game_widget.reset_game()
        self.stackedWidget.setCurrentIndex(1)

    def switchToFirstScreen(self):
        self.stackedWidget.setCurrentIndex(0)


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec_())
