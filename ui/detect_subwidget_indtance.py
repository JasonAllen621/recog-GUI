import time

from ui.detect_subwidget import Ui_detect_subwidget
from model.model.detect_thread import detect
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtWidgets import QWidget, QTextEdit, QMessageBox
import cv2
import threading
from PIL import Image


class detect_subwidget_class(QWidget, Ui_detect_subwidget):
    vedio_path_signal_receive = pyqtSignal(str)
    detected_img_signal_send = pyqtSignal(Image.Image, object)
    detected_info_signal_send = pyqtSignal(list)
    detected_info_signal_receive = pyqtSignal(str)

    def __init__(self):
        super(detect_subwidget_class, self).__init__()
        self.setupUi(self)
        self.radioButton_select_vedio.clicked.connect(self.ui_enable_judge)
        self.radioButton_select_img.clicked.connect(self.ui_enable_judge)
        # self.radioButton_select_SAR.clicked.connect()
        # self.radioButton_select_OPT.clicked.connect()
        self.task_type = 1 # 0是图像检测，1是视频检测
        self.img_type = 0 # 0是SAR，1是光学
        self.img_list = None
        self.vedio_path = None
        self.vedio_flag = 2 # 0是播放，1是暂停，2是结束（停止）
        self.vedio_playing = False
        self.pushButton_play.clicked.connect(self.vedio_play_flag)
        self.pushButton_pause.clicked.connect(self.vedio_pause_flag)
        self.pushButton_stop.clicked.connect(self.vedio_stop_flag)
        # self.weight_path = "model/model/yolov5/weights/8ship_v2.pt"
        self.weight_path = r"model\model\yolov5\weights\8ship_best_v1.pt"
        # self.weight_path = r"model\model\yolov5\weights\vl_best.pt"
        self.vedio_path_signal_receive.connect(self.recieve_vedio_path)
        self.detected_info_signal_receive.connect(self.show_txt)

        self.radioButton_select_img.setEnabled(False)

        self.thread_detect_init()

    def thread_detect_init(self):
        pass

    def recieve_vedio_path(self, path):
        self.vedio_path = path

    def ui_enable_judge(self):
        if self.radioButton_select_vedio.isChecked():
            flag = False
            self.task_type = 1
        else:
            self.task_type = 0
            flag = True
        self.radioButton_select_OPT.setEnabled(flag)
        self.radioButton_select_SAR.setEnabled(flag)
        self.pushButton_play.setEnabled(not flag)
        self.pushButton_pause.setEnabled(not flag)
        self.pushButton_start_img_detect.setEnabled(flag)
        self.pushButton_start_img_detect.setEnabled(not flag)

    def select_img_source(self):
        if self.radioButton_select_SAR.isChecked():
            self.img_type = 0
        else:
            self.img_type = 1

    def vedio_play_flag(self):
        if self.vedio_path != None:
            if not self.vedio_playing:
                self.textBrowser_show_state.setText("正在加载中......")
                self.textBrowser_show_state.setStyleSheet("color:red;")
                self.vedio_playing = True
                self.vedio_flag = 0
                # self.vedio_play()
                detect_thread = threading.Thread(target=self.vedio_play)
                self.textBrowser_show_state.setText("加载完成")
                self.textBrowser_show_state.setStyleSheet("color:black;")
                self.label_vedio_ctrl.setText("视频控制：正在播放")
                detect_thread.start()
            else:
                if self.vedio_flag == 1:
                    self.vedio_flag = 0
                    self.label_vedio_ctrl.setText("视频控制：正在播放")
        else:
            QMessageBox.about(self, "提示", "请选择视频文件")

    def vedio_pause_flag(self):
        if self.vedio_playing:
            self.label_vedio_ctrl.setText("视频控制：播放暂停")
            self.vedio_flag = 1
    def vedio_stop_flag(self):
        if self.vedio_playing:
            self.label_vedio_ctrl.setText("视频控制：播放停止")
            self.vedio_flag = 2
            self.vedio_playing = False
        # time.sleep(0.25)
        # self.textBrowser_show_state.setText("检测停止")

    def vedio_play(self):
        while True:
            if self.vedio_flag == 0:
                for out_img, labels in detect(self.vedio_path, self.weight_path):
                    out_img = Image.fromarray(cv2.cvtColor(out_img, cv2.COLOR_BGR2RGBA))  # 将BGR颜色空间转换为RGB颜色空间
                    self.detected_img_signal_send.emit(out_img, None)
                    # show_txt(labels)
                    self.detected_info_signal_send.emit(labels)
                    # self.textBrowser_show_state.setText(labels)
                    # self.show_txt(labels)
                    # print(lables)
                    if self.vedio_flag != 0:
                        if self.vedio_flag == 1:
                            while True:
                                time.sleep(0.25)
                                if self.vedio_flag != 1:
                                    break
                        if self.vedio_flag == 2:
                            break
            elif self.vedio_flag == 2:
                break
        self.vedio_playing = False

    def show_txt(self, txt):
        self.textBrowser_show_state.setText(txt)








