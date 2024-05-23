from ui.IR_bkg_set import Ui_IR_set_bkg_widget
from PyQt5.QtWidgets import QWidget

class IR_bkg_set_class(QWidget, Ui_IR_set_bkg_widget):
    def __init__(self):
        super(IR_bkg_set_class, self).__init__()
        self.setupUi(self)