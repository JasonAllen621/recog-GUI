# GUIdemo1.py
# Demo1 of GUI by PqYt5
# Copyright 2021 Youcans, XUPT
# Crated：2021-10-06


import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from ui_thread import InitForm



if __name__ == "__main__":
    app = QApplication(sys.argv)
    w1 = InitForm()
    w1.show()
    sys.exit(app.exec_())


