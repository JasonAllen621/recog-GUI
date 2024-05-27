from ui.IR_bkg_set import Ui_IR_set_bkg_widget
from PyQt5.QtWidgets import QWidget, QFileDialog, QMessageBox
from PIL import Image
import os
import time
import cv2
from PyQt5.QtCore import pyqtSignal
import numpy as np

value_range_record = {
    "sea": [5, 30],
    "sky": [2, 30],
    "ice": [1, 5],
    "land": [15, 60],
    "building": [20, 70],
    "img_idx": [1, 97200]
}

class IR_bkg_set_class(QWidget, Ui_IR_set_bkg_widget):
    cfg_info_signal_send = pyqtSignal(dict)
    def __init__(self):
        super(IR_bkg_set_class, self).__init__()
        self.setupUi(self)
        self.param_init()
        self.signal_slot_init()

    def param_init(self):
        self.sea_path = None
        self.sky_path = None
        self.clutter_path = None
        self.rand_mode_path = None

    def signal_slot_init(self):
        self.lineEdit_start_idx.editingFinished.connect(self.set_img_start_idx)
        self.lineEdit_end_idx.editingFinished.connect(self.set_img_end_idx)

        self.radioButton_rand_set.pressed.connect(self.rand_mode)
        self.radioButton_custom_set.pressed.connect(self.custom_mode)

        self.pushButton_select_sea.clicked.connect(self.select_sea)
        self.pushButton_select_sky.clicked.connect(self.select_sky)
        self.pushButton_select_clutter.clicked.connect(self.select_clutter)

        self.radioButton_set_ice.clicked.connect(self.clutter_set_mode)
        self.radioButton_set_land.clicked.connect(self.clutter_set_mode)
        self.radioButton_set_buiding.clicked.connect(self.clutter_set_mode)

        self.horizontalSlider_sea_intensity.valueChanged.connect(self.read_sea_intensity_value)
        self.horizontalSlider_sky_intensity.valueChanged.connect(self.read_sky_intensity_value)

        self.horizontalSlider_ice_intensity.valueChanged.connect(self.read_ice_intensity_value)
        self.horizontalSlider_land_intensity.valueChanged.connect(self.read_land_intensity_value)
        self.horizontalSlider_building_intensity.valueChanged.connect(self.read_building_intensity_value)

        self.lineEdit_sea_intensity.editingFinished.connect(self.set_sea_slider_value)
        self.lineEdit_sky_intensity.editingFinished.connect(self.set_sky_slider_value)
        self.lineEdit_ice_intensity.editingFinished.connect(self.set_ice_slider_value)
        self.lineEdit_land_intensity.editingFinished.connect(self.set_land_slider_value)
        self.lineEdit_building_intensity.editingFinished.connect(self.set_building_slider_value)

        self.pushButton_save_cfg.clicked.connect(self.save_cfg)

    def save_cfg(self):
        if self.radioButton_rand_set.isChecked():
            if self.rand_mode_path != None:
                # mode = 0
                cfg_dict = {
                    "mode": 0,
                    "idx": [int(self.lineEdit_start_idx.text()), int(self.lineEdit_end_idx.text())],
                    "path": self.rand_mode_path
                }
                self.cfg_info_signal_send.emit(cfg_dict)
                time.sleep(0.5)
                self.close()
            else:
                QMessageBox.about(self, "提示", "未选中随机背景下图像路径")
        else:
            # mode = 1
            if self.sea_path != None  and self.sky_path != None and self.clutter_path != None:
                cfg_dict = {
                    "mode": 1,
                    "idx": [int(self.lineEdit_start_idx.text()), int(self.lineEdit_end_idx.text())],
                    "sea": [self.sea_path, int(self.lineEdit_sea_intensity.text())],
                    "sky": [self.sky_path, int(self.lineEdit_sky_intensity.text())],
                    "clutter": [self.clutter_path]
                }
                if self.radioButton_set_ice.isChecked():
                    cfg_dict["clutter"].append(int(self.lineEdit_ice_intensity.text()))
                elif self.radioButton_set_land.isChecked():
                    cfg_dict["clutter"].append(int(self.lineEdit_land_intensity.text()))
                else:
                    cfg_dict["clutter"].append(int(self.lineEdit_building_intensity.text()))

                self.cfg_info_signal_send.emit(cfg_dict)
                time.sleep(0.5)
                self.close()
            else:
                msg_str = ""
                if self.sea_path == None:
                    msg_str = msg_str + "海 "
                if self.sky_path == None:
                    msg_str = msg_str + "天 "
                if self.clutter_path == None:
                    msg_str = msg_str + "其它 "
                msg_str = msg_str + "背景未选择"
                QMessageBox.about(self, "提示", msg_str)

    def rand_mode(self):
        self.radioButton_rand_set.setChecked(True)
        self.widgets_state_change(False)
        options = QFileDialog.Options()
        directory = QFileDialog.getExistingDirectory(None, "选取文件夹",
                                                     r"F:\1A研究生\研究方向\remote_ship\IR\IRship\irships/augment/",
                                                     options=options)  # 起始路径
        if len(directory) > 0:
            sub_dirs = os.listdir(directory)
            sub_dirs = [i.lower() for i in sub_dirs]
            certain_dirs = ["clutter", "sea", "sky"]
            judge_list = [i in sub_dirs for i in certain_dirs]
            judge = True
            for i in judge_list:
                judge = judge and i
            if judge:
                self.rand_mode_path = directory
                self.lineEdit_rand_mode_path.setText(directory)
                self.lineEdit_rand_mode_path.setStyleSheet("color:black;")
            else:
                self.lineEdit_rand_mode_path.setText("选中文件夹格式不符合格式：\n"
                                                     "根文件夹中需要包含：sea（horizontal，elevated）"
                                                     "\nsky\nclutter（ice，landscape，structure）")
                self.lineEdit_rand_mode_path.setStyleSheet("color:red;")
        else:
            self.lineEdit_rand_mode_path.setText("未选中文件夹")
            self.lineEdit_rand_mode_path.setStyleSheet("color:red;")


    def custom_mode(self):
        self.radioButton_custom_set.setChecked(True)
        self.widgets_state_change(True)

    def clutter_set_mode(self):
        self.clutter_widgets_state_change([self.radioButton_set_ice.isChecked(),
                                           self.radioButton_set_land.isChecked(),
                                           self.radioButton_set_buiding.isChecked()])

    def widgets_state_change(self, state):
        self.lineEdit_rand_mode_path.setEnabled(not state)
        self.pushButton_select_sea.setEnabled(state)
        self.pushButton_select_sky.setEnabled(state)
        self.pushButton_select_clutter.setEnabled(state)

        self.horizontalSlider_sea_intensity.setEnabled(state)
        self.lineEdit_sea_intensity.setEnabled(state)
        self.horizontalSlider_sky_intensity.setEnabled(state)
        self.lineEdit_sky_intensity.setEnabled(state)

        self.radioButton_set_ice.setEnabled(state)
        self.radioButton_set_land.setEnabled(state)
        self.radioButton_set_buiding.setEnabled(state)
        self.clutter_widgets_state_change([self.radioButton_set_ice.isChecked(),
                                           self.radioButton_set_land.isChecked(),
                                           self.radioButton_set_buiding.isChecked()])

    def clutter_widgets_state_change(self, state):
        self.horizontalSlider_ice_intensity.setEnabled(state[0])
        self.lineEdit_ice_intensity.setEnabled(state[0])
        self.horizontalSlider_land_intensity.setEnabled(state[1])
        self.lineEdit_land_intensity.setEnabled(state[1])
        self.horizontalSlider_building_intensity.setEnabled(state[2])
        self.lineEdit_building_intensity.setEnabled(state[2])


    def select_file(self):
        options = QFileDialog.Options()
        imgName_list, _ = QFileDialog.getOpenFileNames(self, "选择文件",
                                                                  r"F:\1A研究生\研究方向\remote_ship\IR\IRship\irships/augment/",
                                                                  "背景图像(*.png)",
                                                                  options=options)
        if len(imgName_list) == 1:
            path = imgName_list[0]
            return path
        else:
            QMessageBox.about(self, "提示", "只能选取单张图像/未选中图像")
            return False

    def select_sea(self):
        self.sea_path = self.select_file()
        if self.sea_path:
            img = Image.open(self.sea_path)
            cv2.imshow("海", cv2.cvtColor(np.asarray(img), cv2.COLOR_RGB2BGR))
            cv2.waitKey()

    def select_sky(self):
        self.sky_path = self.select_file()
        if self.sky_path:
            img = Image.open(self.sky_path)
            cv2.imshow("天", cv2.cvtColor(np.asarray(img), cv2.COLOR_RGB2BGR))
            cv2.waitKey()

    def select_clutter(self):
        self.clutter_path = self.select_file()
        if self.clutter_path:
            img = Image.open(self.clutter_path)
            cv2.imshow("其它", cv2.cvtColor(np.asarray(img), cv2.COLOR_RGB2BGR))
            cv2.waitKey()

    def read_sea_intensity_value(self):
        self.lineEdit_sea_intensity.setText(f"{self.horizontalSlider_sea_intensity.value()}")

    def read_sky_intensity_value(self):
        self.lineEdit_sky_intensity.setText(f"{self.horizontalSlider_sky_intensity.value()}")

    def read_ice_intensity_value(self):
        self.lineEdit_ice_intensity.setText(f"{self.horizontalSlider_ice_intensity.value()}")

    def read_land_intensity_value(self):
        self.lineEdit_land_intensity.setText(f"{self.horizontalSlider_land_intensity.value()}")

    def read_building_intensity_value(self):
        self.lineEdit_building_intensity.setText(f"{self.horizontalSlider_building_intensity.value()}")

    def str_2_int(self, source: str, string):
        try:
            number = int(string)
            min_bound = value_range_record[source][0]
            max_bound = value_range_record[source][1]
            if number < min_bound:
                return min_bound
            elif number > max_bound:
                return max_bound
            else:
                return number
        except ValueError:
            QMessageBox.about(self, "提示", "只能输入数字（小数会转为整数）")
            return False

    def set_img_start_idx(self):
        value = self.lineEdit_start_idx.text()
        value = self.str_2_int("img_idx", value)
        if value:
            if value > int(self.lineEdit_end_idx.text()):
                value = int(self.lineEdit_end_idx.text())
            self.lineEdit_start_idx.setText(str(value))

    def set_img_end_idx(self):
        value = self.lineEdit_end_idx.text()
        value = self.str_2_int("img_idx", value)
        if value:
            if value < int(self.lineEdit_start_idx.text()):
                value = int(self.lineEdit_start_idx.text())
            self.lineEdit_end_idx.setText(str(value))

    def set_sea_slider_value(self):
        value = self.lineEdit_sea_intensity.text()
        value = self.str_2_int("sea", value)
        if value:
            self.lineEdit_sea_intensity.setText(str(value))
            self.horizontalSlider_sea_intensity.setValue(value)

    def set_sky_slider_value(self):
        value = self.lineEdit_sky_intensity.text()
        value = self.str_2_int("sky", value)
        if value:
            self.lineEdit_sky_intensity.setText(str(value))
            self.horizontalSlider_sky_intensity.setValue(value)

    def set_ice_slider_value(self):
        value = self.lineEdit_ice_intensity.text()
        value = self.str_2_int("ice", value)
        if value:
            self.lineEdit_ice_intensity.setText(str(value))
            self.horizontalSlider_ice_intensity.setValue(value)

    def set_land_slider_value(self):
        value = self.lineEdit_land_intensity.text()
        value = self.str_2_int("land", value)
        if value:
            self.lineEdit_land_intensity.setText(str(value))
            self.horizontalSlider_land_intensity.setValue(value)

    def set_building_slider_value(self):
        value = self.lineEdit_building_intensity.text()
        value = self.str_2_int("building", value)
        if value:
            self.lineEdit_building_intensity.setText(str(value))
            self.horizontalSlider_building_intensity.setValue(value)












