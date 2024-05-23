from ui.IR_releated_subwidget import Ui_IR_related_subwidget
from ui.IR_bkg_set_instance import IR_bkg_set_class
from PyQt5.QtWidgets import QWidget, QFileDialog


class IR_related_subwidget_class(QWidget, Ui_IR_related_subwidget):
    def __init__(self):
        super(IR_related_subwidget_class, self).__init__()
        self.setupUi(self)
        self.img_read_root_path = None

        self.pushButton_set_bkg.clicked.connect(self.open_set_bkg_widget)
        self.pushButton_read_img_root_path.clicked.connect(self.select_img_read_root_path)

    def open_set_bkg_widget(self):
        self.IR_bkg_set_widget = IR_bkg_set_class()
        self.IR_bkg_set_widget.show()
        # self.IR_bkg_set_widget.exec_()

    def select_img_read_root_path(self):
        options = QFileDialog.Options()
        directory = QFileDialog.getExistingDirectory(None, "选取文件夹", "./", options=options)  # 起始路径
        self.label_show_img_root_path.setText(directory)
