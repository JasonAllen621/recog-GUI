from ui.main_widght import Ui_main_widget
from ui.IR_releated_subwidget import Ui_IR_related_subwidget
from ui.recog_subwidget import Ui_recog_subwidget
from PyQt5.QtWidgets import QWidget, QFileDialog, QGraphicsScene, QButtonGroup, QGraphicsPixmapItem, QTextEdit, QGraphicsView, QStackedLayout
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import QThread

from recog_thread import object_recog
from img_concat_thread import img_concat

class IR_related_subwidget(QWidget, Ui_IR_related_subwidget):
    def __init__(self):
        super(IR_related_subwidget, self).__init__()
        self.setupUi(self)

class recog_subwidget(QWidget, Ui_recog_subwidget):
    def __init__(self):
        super(recog_subwidget, self).__init__()
        self.setupUi(self)

class InitForm(QWidget):

    def __init__(self):
        super(InitForm, self).__init__()
        self.ui = Ui_main_widget()
        self.ui.setupUi(self)
        self.setWindowTitle("目标识别Demo")

        # print("主线程id:", current_thread().ident)
        self.thread_recog_init()
        self.thread_concat_img_init()

        self.param_init()

        # 主窗口初始化
        self.graphic_view_init()
        self.set_logo_init()
        self.stacked_ui_init()# 包括了子窗口的实例化

        # 子窗口初始化
        self.recog_subwidget_init()

        self.ui.pushButton_select_file.clicked.connect(self.select_file_path)
        self.ui.pushButton_change_func.clicked.connect(self.change_func)

    # 参数初始化
    def param_init(self):
        self.net_id = 0  # 默认网络为0号网络
        self.func_id = 0
        self.img_list = [[[0]]]

        # 如果点击了选择文件按钮，并且选择文件的函数运行完毕后则改变为1，
        # 在识别完毕后转为0
        self.recog_flag = False

        self.func_list = ["图像识别", "改变背景"]

        # self.ui.frame.setStyleSheet('''QWidget{background-color:#EAEAEF;}''')
        # self.ui.frame.setLineWidth(3)
        # self.ui.frame.setMidLineWidth(2)

    # 初始化线程
    def thread_recog_init(self):
        self.recog_thread = QThread()
        self.recog = object_recog()
        self.recog.moveToThread(self.recog_thread)
        self.recog.recog_image_signal_receive.connect(self.recog.recog)
        self.recog.class_n_prob_signal_send.connect(self.get_class_n_prob)
        self.recog.net_id_signal_recieve.connect(self.recog.net_select)

    def thread_concat_img_init(self):
        self.concat_img_thread = QThread()
        self.concat_img = img_concat()
        self.concat_img.moveToThread(self.concat_img_thread)
        self.concat_img_thread.start()
        self.concat_img.concatimg_signal_send.connect(self.loadImage)
        self.concat_img.imglist_path_signal_recieve.connect(self.concat_img.concat_images)

    # ui初始化
    # 主窗口相关内容初始化

    def stacked_ui_init(self):
        self.recog_subwidget = recog_subwidget()
        self.IR_related_subwidget = IR_related_subwidget()
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

    # 子窗口相关内容初始化

    def recog_subwidget_init(self):
        self.recog_subwidget.textBrowser_class.setLineWrapMode(QTextEdit.NoWrap)
        self.recog_subwidget.textBrowser_class_prob.setLineWrapMode(QTextEdit.NoWrap)

        self.recog_subwidget.comboBox.addItems(["RESNEXT50", "DENSENET121", "REGNETY16GF"])
        self.recog_subwidget.comboBox.currentIndexChanged[int].connect(self.net_architecture)  # 条目发生改变，发射信号，传递条目内容
        self.recog_subwidget.pushButton_start_recog.clicked.connect(self.start_recog)

    # 修改各种状态量
    def net_architecture(self, i):
        self.net_id = i

    # 改变子窗口功能
    def change_func(self):
        self.func_id = self.func_id + 1
        if self.func_id > 1:
            self.func_id = 0
        self.frame.setCurrentIndex(self.func_id)
        self.ui.label_func_state.setText(f"当前功能：{self.func_list[self.func_id]}")


    # 选择文件并显示
    def select_file_path(self):
        # chatgpt
        # 点击选择文件的按钮之后，弹出选择路径窗口，选择文件
        options = QFileDialog.Options()
        # options |= QFileDialog.DontUseNativeDialog
        self.imgName_list, imgtype = QFileDialog.getOpenFileNames(self,
                                                                  "选择文件", "", "Image(*.jpg *.jpeg *.png *.bmp)",
                                                                  options=options)
        list_len = len(self.imgName_list)

        if list_len < 1:
            self.ui.label_show_path.setText("未选中文件")
            self.ui.label_show_path.setStyleSheet("color:red;")
            self.recog_flag = False
        else:
            if list_len > 1:
                self.ui.label_show_path.setText(self.imgName_list[0] + "等{}个文件".format(len(self.imgName_list)))
            else:
                self.ui.label_show_path.setText(self.imgName_list[0])
            # self.concat_img_thread.start()
            self.ui.label_show_path.setStyleSheet("color:black;")
            self.concat_img.imglist_path_signal_recieve.emit(self.imgName_list, (self.ui.graphicsView.height(), self.ui.graphicsView.width()))
            self.recog_flag = True


    def loadImage(self, concatimg, img_list):
        self.img_list = img_list
        image = self.convertPilToPixmap(concatimg)
        self.scene.clear()
        self.scene.addPixmap(image)

    # 识别过程（开线程，发送图像，识别，显示目标及概率）
    def start_recog(self):
        if self.recog_flag:
            self.recog_thread.start()
            self.recog.net_id_signal_recieve.emit(self.net_id)
            self.recog.recog_image_signal_receive.emit(self.img_list)
            self.recog_subwidget.pushButton_start_recog.setEnabled(False)
            self.ui.pushButton_select_file.setEnabled(False)
            self.recog_subwidget.label_recog_state.setText("识别中……")
            self.recog_subwidget.label_recog_state.setStyleSheet("color:black;")
        else:
            self.recog_subwidget.label_recog_state.setText("未选中文件，无法识别")
            self.recog_subwidget.label_recog_state.setStyleSheet("color:red;")

    def get_class_n_prob(self, msg):
        # print("show txt")
        class_text, prob_text = self.class_prob2text(msg)
        self.recog_subwidget.textBrowser_class.setText(class_text)
        self.recog_subwidget.textBrowser_class_prob.setText(prob_text)

        self.recog_subwidget.label_recog_state.setText("识别结束")
        self.recog_subwidget.pushButton_start_recog.setEnabled(True)
        self.ui.pushButton_select_file.setEnabled(True)
        self.recog_thread.quit()

    # 功能性函数
    def class_prob2text(self, class_n_prob):
        class_text = ''
        prob_text = ''
        count = 0
        for i in class_n_prob:
            count = count + 1
            count_txt = "{}. ".format(count)
            class_text = (class_text + count_txt + i[0]) + '\n'
            prob_text = (prob_text + count_txt + f'{i[1]:.4f}') + '\n'

        return class_text, prob_text

    def convertPilToPixmap(self, image):
        image = image.convert("RGBA")
        data = image.tobytes("raw", "RGBA")
        qimage = QPixmap.fromImage(QImage(data, image.size[0], image.size[1], QImage.Format_RGBA8888))
        pixmap = QPixmap(qimage)
        return pixmap

    def closeEvent(self, event):
        self.concat_img_thread.quit()
        self.recog_thread.quit()
        # print("窗体关闭")