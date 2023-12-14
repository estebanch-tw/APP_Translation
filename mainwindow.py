# MIT License

# Copyright (c) 2017 Gerard Marull-Paretas <gerardmarull@gmail.com>

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import sys
from time import sleep
from os.path import join, dirname, abspath, basename, isdir
from os import listdir

from qtpy import uic
from qtpy.QtCore import Slot, QThread, Signal
from qtpy.QtWidgets import QApplication, QMainWindow, QMessageBox, QTreeWidgetItem

import qtmodern.styles
import qtmodern.windows


_UI = join(dirname(abspath(__file__)), 'mainwindow.ui')


class ProgressThread(QThread):
    update = Signal(int)

    def run(self):
        progress = 20
        while True:
            progress += 1
            if progress == 100:
                progress = 0

            self.update.emit(progress)
            sleep(0.5)


class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)

        uic.loadUi(_UI, self)  # Load the ui into self

        self.tooltiplabel.setToolTip("This is a tool tip that shows a tip about the tool")

        self.actionLight.triggered.connect(self.lightTheme)
        self.actionDark.triggered.connect(self.darkTheme)

        self.thread = ProgressThread()
        self.thread.update.connect(self.update_progress)
        self.thread.start()

        self.load_project_structure(dirname(dirname(abspath(__file__))), self.treeWidget)

        for i in range(100):
            self.comboBox_2.addItem("item {}".format(i))

    def load_project_structure(self, startpath, tree):
        for element in listdir(startpath):
            path_info = startpath + "/" + element
            parent_itm = QTreeWidgetItem(tree, [basename(element)])
            if isdir(path_info):
                self.load_project_structure(path_info, parent_itm)

    def update_progress(self, progress):
        self.progressBar.setValue(progress)

    def lightTheme(self):
        qtmodern.styles.light(QApplication.instance())

    def darkTheme(self):
        qtmodern.styles.dark(QApplication.instance())

    @Slot()
    def on_pushButton_clicked(self):
        self.close()

    @Slot()
    def closeEvent(self, event):
        event.accept()


if __name__ == '__main__':
    app = QApplication(sys.argv)

    qtmodern.styles.dark(app)
    mw = qtmodern.windows.ModernWindow(MainWindow())
    mw.show()

    sys.exit(app.exec_())
