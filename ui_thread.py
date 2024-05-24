from ui.main_widght import Ui_main_widget
from ui.IR_releated_subwidget_instance import IR_related_subwidget_class
from ui.recog_subwidget_instance import recog_subwidget_class
from PyQt5.QtWidgets import QWidget, QFileDialog, QGraphicsScene, QButtonGroup, QGraphicsPixmapItem, QTextEdit, QGraphicsView, QStackedLayout
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import QThread
from img_concat_thread import img_concat


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

        # 子窗口初始化
        self.ui.pushButton_select_file.clicked.connect(self.select_file_path)
        self.ui.pushButton_change_func.clicked.connect(self.change_func)

    # 参数初始化
    def param_init(self):
        self.func_id = 0
        self.func_name_list = ["图像识别", "改变背景"]
        # self.ui.frame.setStyleSheet('''QWidget{background-color:#EAEAEF;}''')
        # self.ui.frame.setLineWidth(3)
        # self.ui.frame.setMidLineWidth(2)

    # 初始化线程
    def thread_concat_img_init(self):
        self.concat_img_thread = QThread()
        self.concat_img = img_concat()
        self.concat_img.moveToThread(self.concat_img_thread)
        self.concat_img_thread.start()
        self.concat_img.concatimg_signal_send.connect(self.loadImage)
        self.concat_img.recog_imglist_path_signal_recieve.connect(self.concat_img.concat_images)
        self.concat_img.IR_imglist_path_signal_recieve.connect(self.concat_img.IR_imgpath_process)

    # ui初始化
    # 主窗口相关内容初始化
    def stacked_ui_init(self):
        self.recog_subwidget = recog_subwidget_class()
        self.IR_related_subwidget = IR_related_subwidget_class()
        self.func_list = [self.recog_subwidget, self.IR_related_subwidget]
        self.frame = QStackedLayout(self.ui.frame)
        self.frame.addWidget(self.recog_subwidget)
        self.frame.addWidget(self.IR_related_subwidget)
        self.frame.setCurrentIndex(self.func_id)

    def graphic_view_init(self):
        self.ui.graphicsView.setViewportUpdateMode(QGraphicsView.FullViewportUpdate)  # 设置刷新模式为自动刷新
        self.scene = QGraphicsScene()  # 创建画布
        self.ui.graphicsView.setScene(self.scene)  # 把画布添加到窗口
        self.ui.graphicsView.show()
        # self.ui.graphicsView 大小500*600

    def set_logo_init(self):
        logo = QPixmap("./ui/logo_gray.jpeg")
        proportion = logo.height() / self.ui.logo_show.height()
        logo.setDevicePixelRatio(proportion)
        self.ui.logo_show.setPixmap(logo)

    # 改变子窗口功能
    def change_func(self):
        self.func_id = self.func_id + 1
        if self.func_id > 1:
            self.func_id = 0
        self.frame.setCurrentIndex(self.func_id)
        self.ui.label_func_state.setText(f"当前功能：{self.func_name_list[self.func_id]}")

    # 选择文件并显示
    def select_file_path(self):
        # chatgpt
        # 点击选择文件的按钮之后，弹出选择路径窗口，选择文件
        options = QFileDialog.Options()
        if self.func_id == 0:
            imgName_list, imgtype = QFileDialog.getOpenFileNames(self,
                                                                      "选择文件", "", "图像(*.jpg *.jpeg *.png *.bmp)",
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
                self.concat_img.recog_imglist_path_signal_recieve.emit(imgName_list, (self.ui.graphicsView.height(), self.ui.graphicsView.width()))
        elif self.func_id == 1:
            directory = QFileDialog.getExistingDirectory(None, "选取文件夹", r"F:\1A研究生\研究方向\remote_ship\IR\IRship\irships/", options=options)  # 起始路径
            if len(directory) > 0:
                self.ui.label_show_path.setText(directory)
                self.ui.label_show_path.setStyleSheet("color:black;")
                self.IR_related_subwidget.img_read_root_path = directory
                self.concat_img.IR_imglist_path_signal_recieve.emit(directory, (self.ui.graphicsView.height(), self.ui.graphicsView.width()))
            else:
                self.ui.label_show_path.setText("未选中文件夹")
                self.ui.label_show_path.setStyleSheet("color:red;")


    def loadImage(self, concatimg, img_list):
        self.func_list[self.func_id].img_list = img_list
        image = self.convertPilToPixmap(concatimg)
        self.scene.clear()
        self.scene.addPixmap(image)

    # 功能性函数
    def convertPilToPixmap(self, image):
        image = image.convert("RGBA")
        data = image.tobytes("raw", "RGBA")
        qimage = QPixmap.fromImage(QImage(data, image.size[0], image.size[1], QImage.Format_RGBA8888))
        pixmap = QPixmap(qimage)
        return pixmap

    def closeEvent(self, event):
        # pass
        self.concat_img_thread.quit()
        self.recog_subwidget.recog_thread.quit()
        # print("窗体关闭")