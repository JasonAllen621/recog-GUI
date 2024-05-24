from ui.IR_releated_subwidget import Ui_IR_related_subwidget
from ui.IR_bkg_set_instance import IR_bkg_set_class
from PyQt5.QtWidgets import QWidget, QFileDialog, QMessageBox


class IR_related_subwidget_class(QWidget, Ui_IR_related_subwidget):
    def __init__(self):
        super(IR_related_subwidget_class, self).__init__()
        self.setupUi(self)
        self.img_read_root_path = None
        self.csv_path = None
        self.pushButton_set_bkg.clicked.connect(self.open_set_bkg_widget)
        self.pushButton_read_img_root_path.clicked.connect(self.select_img_read_root_path)


    def select_img_read_root_path(self):
        if self.img_read_root_path != None:
            options = QFileDialog.Options()
            fileName_list, filetype = QFileDialog.getOpenFileNames(self, "选择文件",
                                                                   r"F:\1A研究生\研究方向\remote_ship\IR\IRship\irships/", "表格文件(*.csv)",
                                                                 options=options)
            if len(fileName_list) != 0:
                self.label_show_img_root_path.setText(f"{fileName_list[0]}")
                self.label_show_img_root_path.setStyleSheet("color:black;")
                self.csv_path = fileName_list[0]
            else:
                self.label_show_img_root_path.setText("未选中文件")
                self.label_show_img_root_path.setStyleSheet("color:red;")
        else:
            self.label_show_img_root_path.setText("未选中图像根文件夹（左下角）")
            self.label_show_img_root_path.setStyleSheet("color:red;")

    def open_set_bkg_widget(self):
        if self.csv_path != None:
            self.IR_bkg_set_widget = IR_bkg_set_class()
            self.IR_bkg_set_widget.show()
            self.IR_bkg_set_widget.cfg_info_signal_send.connect(self.process_cfg_info)
        else:
            QMessageBox.about(self, "提示", "未选中图像序列文件")
        # self.IR_bkg_set_widget.exec_()

    def process_cfg_info(self, mode, cfg_dict):
        print("process", mode, cfg_dict)
        show_msg = ""
        if mode == 0:
            show_msg = show_msg + "随机背景\n" + f"背景图路径：{cfg_dict['path']}"
            self.label_show_IR_state.setText(show_msg)
        else:
            pass
