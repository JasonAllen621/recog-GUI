from ui.IR_releated_subwidget import Ui_IR_related_subwidget
from PyQt5.QtWidgets import QWidget


class IR_related_subwidget_class(QWidget, Ui_IR_related_subwidget):
    def __init__(self):
        super(IR_related_subwidget_class, self).__init__()
        self.setupUi(self)