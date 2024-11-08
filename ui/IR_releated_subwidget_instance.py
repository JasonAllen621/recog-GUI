import os
import time
from recog_thread import object_recog
from ui.IR_releated_subwidget import Ui_IR_related_subwidget
from ui.IR_bkg_set_instance import IR_bkg_set_class
from PyQt5.QtWidgets import QWidget, QFileDialog, QMessageBox
from PyQt5.QtCore import pyqtSignal, QThread
from change_IR_bkg_thread import change_IR_bkg


class IR_related_subwidget_class(QWidget, Ui_IR_related_subwidget):
    object_img_root_path_signal_recieve = pyqtSignal(str)

    def __init__(self):
        super(IR_related_subwidget_class, self).__init__()
        self.setupUi(self)
        self.thread_IR_subwedgit_init()
        self.thread_recog_init()
        self.param_init()
        self.ui_slot_init()

    def ui_slot_init(self):
        self.pushButton_set_bkg.clicked.connect(self.open_set_bkg_widget)
        self.pushButton_read_img_root_path.clicked.connect(self.select_img_read_root_path)
        self.pushButton_start_generate.clicked.connect(self.start_generate)
        self.object_img_root_path_signal_recieve.connect(self.receive_object_img_root_path)
        self.pushButton_save.clicked.connect(self.save_processed_imgs)
        self.pushButton_start_IR_recog.clicked.connect(self.start_recog)

    def param_init(self):
        self.img_read_root_path = None
        self.csv_path = None
        self.cfg_dict = None
        self.object_img_root_path = None
        self.img_list = None

    def thread_IR_subwedgit_init(self):
        self.process_thread = QThread()
        self.process_func = change_IR_bkg()
        self.process_func.moveToThread(self.process_thread)
        self.process_thread.start()
        self.process_func.rand_set_signal_recieve.connect(self.process_func.rand_set_bkg)
        self.process_func.custom_set_signal_recieve.connect(self.process_func.custom_set_bkg)
        self.process_func.QMessage_signal_send.connect(self.show_func_msg)

    def thread_recog_init(self):
        self.recog_thread = QThread()
        self.recog = object_recog()
        self.recog.moveToThread(self.recog_thread)
        self.recog_thread.start()
        self.recog.recog_image_signal_receive.connect(self.recog.recog)
        self.recog.class_n_prob_signal_send.connect(self.get_class_n_prob)
        self.recog.net_id_signal_recieve.connect(self.recog.net_select)

    def start_recog(self):
        if self.img_list != None:
            self.recog.net_id_signal_recieve.emit("INFRAD", 0)
            self.recog.recog_image_signal_receive.emit(self.img_list)
            self.pushButton_start_IR_recog.setEnabled(False)
            self.label_IR_recog_state.setText("识别中……")
            self.label_IR_recog_state.setStyleSheet("color:black;")
        else:
            self.label_IR_recog_state.setText("未生成图像，无法识别")
            self.label_IR_recog_state.setStyleSheet("color:red;")

    def get_class_n_prob(self, msg):
        text = self.class_prob2text(msg)
        self.textBrowser_class_n_prob.setText(text)
        self.label_IR_recog_state.setText("识别结束")
        self.pushButton_start_IR_recog.setEnabled(True)

    def class_prob2text(self, class_n_prob):
        text = ''
        count = 0
        for i in class_n_prob:
            count = count + 1
            text = text + f"{count}. {i[0]}  {i[1]}\n"

        return text

    def show_func_msg(self, content):
        QMessageBox.about(self, "提示", content)

    def receive_object_img_root_path(self, path):
        self.object_img_root_path = path

    def select_img_read_root_path(self):
        if self.img_read_root_path != None:
            options = QFileDialog.Options()
            default_path = r"F:\1A研究生\研究方向\remote_ship\IR\IRship\irships/"
            if not os.path.exists:
                default_path = "./"
            fileName_list, filetype = QFileDialog.getOpenFileNames(self, "选择文件",
                                                                   default_path, "表格文件(*.csv)",
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

    def start_generate(self):
        if self.cfg_dict != None:
            if self.cfg_dict["mode"] == 0:
                self.process_func.rand_set_signal_recieve.emit(self.csv_path, self.cfg_dict, self.object_img_root_path)
            else:
                self.process_func.custom_set_signal_recieve.emit(self.csv_path, self.cfg_dict, self.object_img_root_path)
        else:
            QMessageBox.about(self, "提示", "未设置背景参数")

    def process_cfg_info(self, cfg_dict):
        self.cfg_dict = cfg_dict
        show_msg = ""
        if cfg_dict["mode"] == 0:
            show_msg = show_msg + "随机背景\n" + f"索引范围：{cfg_dict['idx'][0], cfg_dict['idx'][1]}\n" \
            + f"背景图路径：{cfg_dict['path']}"

        else:
            show_msg = show_msg + "自定义背景\n" + f"索引范围：{cfg_dict['idx'][0], cfg_dict['idx'][1]}\n" \
                       + f"海：图像路径：{cfg_dict['sea'][0]}，强度：{cfg_dict['sea'][1]}\n" \
                       + f"天：图像路径：{cfg_dict['sky'][0]}，强度：{cfg_dict['sky'][1]}\n"  \
                       + f"其它：图像路径：{cfg_dict['clutter'][0]}，强度：{cfg_dict['clutter'][1]}\n"
        self.textBrowser_show_param.setText(show_msg)

    def save_processed_imgs(self):
        if self.img_list != None:
            path = f"./processed_img/{time.strftime('%Y-%m-%d %H-%M-%S', time.localtime())}"
            if not os.path.exists(path):
                os.makedirs(path)
            count = 0
            # try:
            for img in self.img_list:
                    count = count + 1
                    img.save(os.path.join(path, f"{count}.png"))
            self.label_show_save_path.setText(f"已保存至{path}")
            self.label_show_save_path.setStyleSheet("color:black;")



