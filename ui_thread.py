from ui.ui_object_recog_demo import Ui_object_recog_demo
from PyQt5.QtWidgets import QWidget, QFileDialog, QGraphicsScene, QButtonGroup, QGraphicsPixmapItem, QTextEdit, QGraphicsView
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import QThread

from torch import version, cuda

from recog_thread import object_recog
from img_concat_thread import img_concat

class InitForm(QWidget):

    def __init__(self):
        super().__init__()
        self.ui = Ui_object_recog_demo()
        self.ui.setupUi(self)
        self.setWindowTitle("目标识别Demo")

        self.net_id = 0  # 默认网络为0号网络
        self.img_list = [[[0]]]
        self.cuda_version = None
        self.gpu_cal_available = False
        self.cuda_available = cuda.is_available()

        # 如果点击了选择文件按钮，并且选择文件的函数运行完毕后则改变为1，
        # 在识别完毕后转为0
        self.recog_flag = False
        self.cuda_flag = False

        # print("主线程id:", current_thread().ident)
        self.thread_recog_init()
        self.thread_concat_img_init()
        self.gpu_available_judge()

        self.button_group = QButtonGroup(self)
        self.button_group.addButton(self.ui.radioButton_cpu)
        self.button_group.addButton(self.ui.radioButton_cuda)
        self.ui.radioButton_cpu.setChecked(True)  # 设置默认选项

        self.ui.graphicsView.setViewportUpdateMode(QGraphicsView.FullViewportUpdate)  # 设置刷新模式为自动刷新
        self.scene = QGraphicsScene()  # 创建画布
        self.ui.graphicsView.setScene(self.scene)  # 把画布添加到窗口
        self.ui.graphicsView.show()
        # self.ui.graphicsView 大小549*374

        self.ui.textBrowser_class.setLineWrapMode(QTextEdit.NoWrap)
        self.ui.textBrowser_class_prob.setLineWrapMode(QTextEdit.NoWrap)

        self.ui.comboBox.addItems(["RESNEXT50", "DENSENET121", "REGNETY16GF"])
        self.ui.comboBox.currentIndexChanged[int].connect(self.net_architecture)  # 条目发生改变，发射信号，传递条目内容

        self.ui.radioButton_cuda.clicked.connect(self.handle_cuda_button_clicked)
        self.ui.radioButton_cpu.clicked.connect(self.handle_cuda_button_clicked)
        self.ui.pushButton_select_file.clicked.connect(self.select_file_path)
        self.ui.pushButton_start_recog.clicked.connect(self.start_recog)

    # 初始化线程
    def thread_recog_init(self):
        self.recog_thread = QThread()
        self.recog = object_recog()
        self.recog.moveToThread(self.recog_thread)
        self.recog.device_n_image_signal_receive.connect(self.recog.recog)
        self.recog.class_n_prob_signal_send.connect(self.get_class_n_prob)
        self.recog.net_model_signal_recieve.connect(self.recog.net_select)

    def thread_concat_img_init(self):
        self.concat_img_thread = QThread()
        self.concat_img = img_concat()
        self.concat_img.moveToThread(self.concat_img_thread)
        self.concat_img_thread.start()
        self.concat_img.concatimg_signal_send.connect(self.loadImage)
        self.concat_img.imglist_path_signal_recieve.connect(self.concat_img.concat_images)

    def gpu_available_judge(self):
        if self.cuda_available:
            self.cuda_version = version.cuda
            if self.cuda_version == "11.8":
                self.ui.label_cuda_available_version.setText(
                    "已安装CUDA，版本为11.8，GPU运算可用"
                )
                self.ui.radioButton_cuda.setEnabled(True)
                self.ui.label_cuda_available_version.setStyleSheet("color: green;")
                self.gpu_cal_available = True
            else:
                self.ui.label_cuda_available_version.setText(
                    "已安装CUDA，版本为{}，指定CUDA版本11.8，GPU运算不可用".format(self.cuda_version)
                )
                self.ui.label_cuda_available_version.setStyleSheet("color: yellow;")
                self.ui.radioButton_cuda.setEnabled(False)
        else:
            self.ui.label_cuda_available_version.setText(
                "未安装CUDA，不可使用GPU运算"
            )
            self.ui.label_cuda_available_version.setStyleSheet("color: red;")
            self.ui.radioButton_cuda.setEnabled(False)

    # 修改各种状态量
    def net_architecture(self, i):
        self.net_id = i

    def handle_cuda_button_clicked(self):
        if self.ui.radioButton_cuda.isChecked() & self.gpu_cal_available:
            self.cuda_flag = True
        else:
            self.cuda_flag = False

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
            self.concat_img.imglist_path_signal_recieve.emit(self.imgName_list)
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
            self.recog.net_model_signal_recieve.emit(self.net_id)
            self.recog.device_n_image_signal_receive.emit(self.img_list, self.cuda_flag)
            self.ui.pushButton_start_recog.setEnabled(False)
            self.ui.pushButton_select_file.setEnabled(False)
            self.ui.label_recog_state.setText("识别中……")
            self.ui.label_recog_state.setStyleSheet("color:black;")
        else:
            self.ui.label_recog_state.setText("未选中文件，无法识别")
            self.ui.label_recog_state.setStyleSheet("color:red;")

    def get_class_n_prob(self, msg):
        # print("show txt")
        class_text, prob_text = self.class_prob2text(msg)
        self.ui.textBrowser_class.setText(class_text)
        self.ui.textBrowser_class_prob.setText(prob_text)

        self.ui.label_recog_state.setText("识别结束")
        self.ui.pushButton_start_recog.setEnabled(True)
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