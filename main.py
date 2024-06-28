# GUIdemo1.py
# Demo1 of GUI by PqYt5
# Copyright 2021 Youcans, XUPT
# Crated：2021-10-06


import sys
import os
from PyQt5.QtWidgets import QApplication, QMainWindow
from ui_thread import InitForm
import multiprocessing
# from qt_material import apply_stylesheet


# 资源文件目录访问
def source_path(relative_path):
    # 是否Bundle Resource
    if getattr(sys, 'frozen', False):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

# 修改当前工作目录，使得资源文件可以被正确访问
cd = source_path('')
os.chdir(cd)

if __name__ == "__main__":
    multiprocessing.freeze_support()
    app = QApplication(sys.argv)
    # apply_stylesheet(app, theme='light_cyan_500.xml')
    w1 = InitForm()
    w1.show()
    sys.exit(app.exec_())


