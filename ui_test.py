from ui.main_widght import Ui_main_widget
from ui.ui1 import Ui_Form1
from ui.ui2 import Ui_Form
from ui.IR_releated_subwidget import Ui_IR_related_subwidget
from ui.recog_subwidget import Ui_recog_subwidget
from PyQt5.QtWidgets import QWidget, QStackedLayout, QApplication
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import QThread
import sys

class ui1(QWidget, Ui_IR_related_subwidget):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

class ui2(QWidget, Ui_recog_subwidget):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

class mainForm(QWidget):
    def __init__(self):
        super(mainForm, self).__init__()
        self.ui = Ui_main_widget()
        self.ui.setupUi(self)

        self.recog_subwidget = ui1()
        self.IR_subwidget = ui2()

        self.frame = QStackedLayout(self.ui.frame)
        self.frame.addWidget(self.recog_subwidget)
        self.frame.addWidget(self.IR_subwidget)
        self.frame.setCurrentIndex(0)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = mainForm()
    window.show()
    sys.exit(app.exec_())
