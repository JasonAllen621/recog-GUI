from ui.recog_subwidget import Ui_recog_subwidget
from recog_thread import object_recog
from PyQt5.QtCore import QThread
from PyQt5.QtWidgets import QWidget, QTextEdit

source_list = ["OPT", "SAR"]
class recog_subwidget_class(QWidget, Ui_recog_subwidget):
    def __init__(self):
        super(recog_subwidget_class, self).__init__()
        self.setupUi(self)
        self.net_id = 0
        # 如果点击了选择文件按钮，并且选择文件的函数运行完毕后则改变为1（True），
        # 在识别完毕后转为0(False)
        self.img_list = None
        self.thread_recog_init()
        self.recog_subwidget_init()

    def thread_recog_init(self):
        self.recog_thread = QThread()
        self.recog = object_recog()
        self.recog.moveToThread(self.recog_thread)
        self.recog_thread.start()
        self.recog.recog_image_signal_receive.connect(self.recog.recog)
        self.recog.class_n_prob_signal_send.connect(self.get_class_n_prob)
        self.recog.net_id_signal_recieve.connect(self.recog.net_select)

    def recog_subwidget_init(self):
        self.textBrowser_class.setLineWrapMode(QTextEdit.NoWrap)
        self.textBrowser_class_prob.setLineWrapMode(QTextEdit.NoWrap)

        self.comboBox.addItems(["RESNEXT50", "DENSENET121", "REGNETY16GF"])
        self.comboBox.currentIndexChanged[int].connect(self.net_architecture)  # 条目发生改变，发射信号，传递条目内容
        self.pushButton_start_recog.clicked.connect(self.start_recog)

    # 修改各种状态量
    def net_architecture(self, i):
        self.net_id = i

    # 识别过程（开线程，发送图像，识别，显示目标及概率）
    def start_recog(self):
        # print(type(self.buttonGroup_specify_source.checkedId()))
        if self.img_list != None:
            self.recog.net_id_signal_recieve.emit(
                source_list[-1 * (self.buttonGroup_specify_source.checkedId() + 2)],
                self.net_id)
            self.recog.recog_image_signal_receive.emit(self.img_list)
            self.pushButton_start_recog.setEnabled(False)
            # self.pushButton_select_file.setEnabled(False)
            self.label_recog_state.setText("识别中……")
            self.label_recog_state.setStyleSheet("color:black;")
        else:
            self.label_recog_state.setText("未选中文件，无法识别")
            self.label_recog_state.setStyleSheet("color:red;")

    def get_class_n_prob(self, msg):
        # print("show txt")
        class_text, prob_text = self.class_prob2text(msg)
        self.textBrowser_class.setText(class_text)
        self.textBrowser_class_prob.setText(prob_text)

        self.label_recog_state.setText("识别结束")
        self.pushButton_start_recog.setEnabled(True)
        # self.pushButton_select_file.setEnabled(True)

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