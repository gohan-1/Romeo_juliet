from PyQt5 import QtWidgets

from game_widget import GameMode
from opening_screen import OpeningScreen
from player import Player, PlayerType
from playing_screen import PlayingScreen


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.stackedWidget = QtWidgets.QStackedWidget(self)
        self.setCentralWidget(self.stackedWidget)
        self.firstScreen = OpeningScreen(
            self.switch_to_normal_game, self.switch_to_ai_game)
        self.secondScreen = PlayingScreen(self.switchToFirstScreen)
        self.stackedWidget.addWidget(self.firstScreen)
        self.stackedWidget.addWidget(self.secondScreen)

    def switch_to_normal_game(self):
        self.secondScreen.game_widget.reset_game()
        self.stackedWidget.setCurrentIndex(1)

    def switch_to_ai_game(self):
        dlg = QtWidgets.QMessageBox()
        dlg.setStyleSheet("font-family:'Courier'; ")
        dlg.setWindowTitle("Choose player")
        dlg.setText("Choose Romeo you want to play")
        red = dlg.addButton('Red Romeo (plays first)',
                            QtWidgets.QMessageBox.ActionRole)
        black = dlg.addButton('Black Romeo (plays second)',
                              QtWidgets.QMessageBox.ActionRole)
        red_style = "QPushButton { background-color: #B20000; color: white; border: none; padding: 10px 20px; text-align: center; text-decoration: none; font-size: 16px; margin: 4px 2px; }"
        red.setStyleSheet(red_style)
        black_style = "QPushButton { background-color: #000000; color: white; border: none; padding: 10px 20px; text-align: center; text-decoration: none; font-size: 16px; margin: 4px 2px;  }"
        black.setStyleSheet(black_style)
        dlg.setModal(False)
        dlg.exec_()
        if dlg.clickedButton() == red:
            self.secondScreen.game_widget.reset_game(
                GameMode.AI, ai_player_color=PlayerType.BLACK)
        elif dlg.clickedButton() == black:
            self.secondScreen.game_widget.reset_game(
                GameMode.AI, ai_player_color=PlayerType.RED)
        else:
            return
        self.stackedWidget.setCurrentIndex(1)

    def switchToFirstScreen(self):
        self.stackedWidget.setCurrentIndex(0)


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec_())
