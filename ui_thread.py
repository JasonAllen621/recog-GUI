import time

from ui.main_widght import Ui_main_widget
from ui.IR_releated_subwidget_instance import IR_related_subwidget_class
from ui.recog_subwidget_instance import recog_subwidget_class
from ui.detect_subwidget_indtance import detect_subwidget_class
from PyQt5.QtWidgets import QWidget, QFileDialog, QGraphicsScene, QGraphicsView, QStackedLayout
from PyQt5.QtGui import QPixmap, QImage, QPainter
from PyQt5.QtCore import Qt
from img_concat_thread import img_concat
import os
import re


class InitForm(QWidget):

    def __init__(self):
        super(InitForm, self).__init__()
        self.ui = Ui_main_widget()
        self.ui.setupUi(self)
        self.setWindowTitle("目标识别Demo")

        # print("主线程id:", current_thread().ident)
        self.thread_concat_img_init()
        self.param_init()
        # 主窗口初始化
        self.graphic_view_init()
        self.set_logo_init()
        self.stacked_ui_init()# 包括了子窗口的实例化

        self.setFixedSize(self.width(), self.height())
        self.setWindowFlag(Qt.WindowMinimizeButtonHint)
        self.setWindowFlag(Qt.WindowCloseButtonHint)
        self.ui.pushButton_select_file.clicked.connect(self.select_file_path)
        # self.ui.pushButton_change_func.clicked.connect(self.change_func)


    # 参数初始化
    def param_init(self):
        self.func_id = 0
        self.ui.comboBox_select_func.addItems(["图像识别", "改变背景", "图像（流）检测"])
        self.ui.comboBox_select_func.currentIndexChanged[int].connect(self.change_func)
        # self.ui.frame.setStyleSheet('''QWidget{background-color:#EAEAEF;}''')
        # self.ui.frame.setLineWidth(3)
        # self.ui.frame.setMidLineWidth(2)

    # 初始化线程
    def thread_concat_img_init(self):
        # self.concat_img_thread = QThread()
        self.concat_img = img_concat()
        self.concat_img.setParent(self)
        # self.concat_img.moveToThread(self.concat_img_thread)
        # self.concat_img_thread.start()
        self.concat_img.concatimg_signal_send.connect(self.loadImage)
        self.concat_img.recog_imglist_path_signal_recieve.connect(self.concat_img.recog_concat_images)
        self.concat_img.IR_imglist_path_signal_recieve.connect(self.concat_img.IR_imgpath_process)


    # ui初始化
    # 主窗口相关内容初始化
    def stacked_ui_init(self):
        self.recog_subwidget = recog_subwidget_class()
        # self.recog_subwidget.setParent(self)
        self.IR_related_subwidget = IR_related_subwidget_class()
        self.IR_related_subwidget.process_func.processed_IR_imgs_signal_send.connect(
            self.concat_img.processed_IR_imgs_concat_images)
        self.detect_subwidget = detect_subwidget_class()
        self.detect_subwidget.detected_img_signal_send.connect(self.loadImage)
        self.detect_subwidget.detected_info_signal_send.connect(self.detect_info_process)
        # self.detect_subwidget.vedio_path_signal_receive.connect(self)
        # self.recog_subwidget.setParent(self)

        self.func_list = [self.recog_subwidget, self.IR_related_subwidget, self.detect_subwidget]
        self.frame = QStackedLayout(self.ui.frame)
        # self.frame.addWidget(self.recog_subwidget)
        # self.frame.addWidget(self.IR_related_subwidget)
        for i in self.func_list:
            self.frame.addWidget(i)
        self.frame.setCurrentIndex(self.func_id)

    def graphic_view_init(self):
        self.graphicview_scale_factor = 1
        self.ui.graphicsView.setViewportUpdateMode(QGraphicsView.FullViewportUpdate)  # 设置刷新模式为自动刷新

        self.ui.graphicsView.show()
        self.ui.graphicsView.setRenderHint(QPainter.Antialiasing)  # 可选，抗锯齿渲染
        self.ui.graphicsView.setDragMode(QGraphicsView.ScrollHandDrag)
        self.ui.graphicsView.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)  # 在鼠标位置缩放
        self.ui.graphicsView.setResizeAnchor(QGraphicsView.AnchorUnderMouse)  # 在鼠标位置缩放
        # self.ui.graphicsView.setWheelModifiers(Qt.ControlModifier)  # 使用 Ctrl + 鼠标滚轮进行缩放
        self.ui.graphicsView.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.ui.graphicsView.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.ui.graphicsView.wheelEvent = self.graphicview_wheel_Event
        self.ui.graphicsView.mouseDoubleClickEvent = self.mouseDoubleClickEvent
        # self.ui.graphicsView 大小500*600

    def set_logo_init(self):
        logo = QPixmap("./ui/logo.png")
        proportion = logo.height() / self.ui.logo_show.height()
        logo.setDevicePixelRatio(proportion)
        self.ui.logo_show.setPixmap(logo)

    def mouseDoubleClickEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.graphicview_back2_ori_size()

    def graphicview_back2_ori_size(self):
        self.ui.graphicsView.scale(1 / self.graphicview_scale_factor, 1 / self.graphicview_scale_factor)
        self.graphicview_scale_factor = 1

    def graphicview_wheel_Event(self, event):
        # https://blog.csdn.net/qq_60947873/article/details/126321522
        if event.modifiers() == Qt.ControlModifier:
            delta = event.angleDelta().y() / 120
            zoom_factor = 1.2 ** delta
            self.graphicview_scale_factor = self.graphicview_scale_factor * zoom_factor
            self.ui.graphicsView.scale(zoom_factor, zoom_factor)
        else:
            super().wheelEvent(event)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Plus:  # 按 "+" 键放大图像
            self.ui.graphicsView.scale(1.2, 1.2)
            self.graphicview_scale_factor = self.graphicview_scale_factor * 1.2
        elif event.key() == Qt.Key_Minus:  # 按 "-" 键缩小图像
            self.ui.graphicsView.scale(0.8, 0.8)
            self.graphicview_scale_factor = self.graphicview_scale_factor * 0.8

    # 改变子窗口功能
    def change_func(self, idx):
        self.graphicview_back2_ori_size()
        if self.func_id == 2:
            self.detect_subwidget.vedio_flag = 2
        self.func_id = idx
        # self.func_id = self.func_id + 1
        # if self.func_id > 1:
        #     self.func_id = 0
        self.frame.setCurrentIndex(idx)
        # self.ui.label_func_state.setText(f"当前功能：{self.func_name_list[self.func_id]}")
        # self.ui.la

    # 选择文件并显示
    def select_imgs_path(self, options):
        imgName_list, imgtype = QFileDialog.getOpenFileNames(self,
                                                             "选择文件", "./",
                                                             "图像(*.jpg *.jpeg *.png *.bmp *.tif *.tiff)",
                                                             options=options)

        list_len = len(imgName_list)

        if list_len < 1:
            self.ui.label_show_path.setText("未选中文件")
            self.ui.label_show_path.setStyleSheet("color:red;")
        else:
            if list_len > 1:
                self.ui.label_show_path.setText(imgName_list[0] + "等{}个文件".format(len(imgName_list)))
            else:
                self.ui.label_show_path.setText(imgName_list[0])
            self.ui.label_show_path.setStyleSheet("color:black;")
            self.concat_img.recog_imglist_path_signal_recieve.emit(imgName_list)

    def select_file_path(self):
        # chatgpt
        # 点击选择文件的按钮之后，弹出选择路径窗口，选择文件
        options = QFileDialog.Options()
        if self.func_id == 0:
            self.select_imgs_path(options)
        elif self.func_id == 1:
            default_path = r"F:\1A研究生\研究方向\remote_ship\IR\IRship\irships/"
            if not os.path.exists:
                default_path = "./"
            directory = QFileDialog.getExistingDirectory(None, "选取文件夹", default_path, options=options)  # 起始路径
            if len(directory) > 0:
                sub_dirs = os.listdir(directory)
                sub_dirs = [i.lower() for i in sub_dirs]
                judge_list = [i in sub_dirs for i in ['images', 'labels']]
                judge = True
                for i in judge_list:
                    judge = judge and i
                if judge:
                    self.ui.label_show_path.setText(directory)
                    self.ui.label_show_path.setStyleSheet("color:black;")
                    self.IR_related_subwidget.img_read_root_path = directory
                    self.concat_img.IR_imglist_path_signal_recieve.emit(directory)
                    self.IR_related_subwidget.object_img_root_path_signal_recieve.emit(directory)
                else:
                    self.ui.label_show_path.setText("选中文件夹格式不符合格式：\n"
                                                         "根文件夹中需要包含以下文件夹：images、labels")
                    self.ui.label_show_path.setStyleSheet("color:red;")
            else:
                self.ui.label_show_path.setText("未选中文件夹")
                self.ui.label_show_path.setStyleSheet("color:red;")
        elif self.func_id == 2:
            # print(self.detect_subwidget.task_type)
            if self.detect_subwidget.task_type == 0:
                self.select_imgs_path(options)
            else:
                if not self.detect_subwidget.vedio_playing:
                    vedioName, _ = QFileDialog.getOpenFileName(self, "选择文件", "./",
                                                                "视频(*.mp4 *.avi)",
                                                                options=options)

                    # def contain_chinese(check_str):
                    #     for ch in check_str:
                    #         if '\u4e00' <= ch <= '\u9fa5':
                    #             return True
                    #     return False
                    # if contain_chinese(vedioName):
                    #     self.ui.label_show_path.setText("选择的路径不能包含中文")
                    #     self.ui.label_show_path.setStyleSheet("color:red;")
                    # else:
                    self.detect_subwidget.vedio_path = vedioName
                    self.ui.label_show_path.setText(vedioName)
                    self.ui.label_show_path.setStyleSheet("color:black;")
                    self.detect_subwidget.vedio_path_signal_receive.emit(vedioName)
                else:
                    self.ui.label_show_path.setText("视频正在播放，等待播放完毕或停止后选择文件")
                    self.ui.label_show_path.setStyleSheet("color:red;")



    def loadImage(self, showimg, img_list=None):
        if self.func_id != 2:
            self.func_list[self.func_id].img_list = img_list
        image = self.convertPilToPixmap(showimg)
        scene = QGraphicsScene()  # 创建画布
        self.ui.graphicsView.setScene(scene)  # 把画布添加到窗口
        scene.clear()
        scene.addPixmap(image)

    # 功能性函数
    def convertPilToPixmap(self, image):
        image = image.convert("RGBA")
        data = image.tobytes("raw", "RGBA")
        qimage = QPixmap.fromImage(QImage(data, image.size[0], image.size[1], QImage.Format_RGBA8888))
        pixmap = QPixmap(qimage)
        return pixmap

    def detect_info_process(self, txt_list):
        content = ''
        for i in txt_list:
            content = content + i + "\n"
        self.detect_subwidget.detected_info_signal_receive.emit(content)

    def closeEvent(self, event):
        # pass
        # self.concat_img_thread.quit()
        self.detect_subwidget.vedio_flag = 2
        time.sleep(0.5)
        self.recog_subwidget.recog_thread.quit()
        self.IR_related_subwidget.process_thread.quit()
        # print("窗体关闭")