from PyQt5 import QtWidgets, uic
from PyQt5.QtCore import pyqtSlot


class Window(QtWidgets.QMainWindow):
    def __init__(self):
        super(Window, self).__init__()
        uic.loadUi('res/planner.ui', self)
        self.setFixedSize(800, 849)
        self.show()

        self.submit.clicked.connect(self.on_click)
        self.data_edit.returnPressed.connect(self.submit.click)

    @pyqtSlot()
    def on_click(self):
        print('PyQt5 button click')
        print(self.data_edit.text())
        self.data_edit.setText('')


if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    window = Window()
    app.exec_()
