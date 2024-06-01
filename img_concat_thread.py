import os.path
from PIL import Image, ImageOps
from PyQt5.QtCore import pyqtSignal, QObject
import math

class img_concat(QObject):
    recog_imglist_path_signal_recieve = pyqtSignal(object)
    concatimg_signal_send = pyqtSignal(Image.Image, list)
    IR_imglist_path_signal_recieve = pyqtSignal(str)

    def __init__(self):
        super(img_concat, self).__init__()
        pass

    def img_pad(self, img):
        (width, height) = img.size
        delta_width = self.set_size - width
        delta_height = self.set_size - height
        left = delta_width // 2
        top = delta_height // 2
        right = delta_width - left
        bottom = delta_height - top

        padded_image = ImageOps.expand(img, border=(left, top, right, bottom), fill='white')
        return padded_image

    def IR_imgpath_process(self, root_path):
        img_path = os.path.join(root_path, "images")
        # mask_path = os.path.join(root_path, "labels")
        img_path_select_list = os.listdir(img_path)[-1004:-1000]
        img_path_select_list = [os.path.join(img_path, i) for i in img_path_select_list]
        # mask_path_select_list = os.listdir(mask_path)[-1002:-1000]
        # mask_path_select_list = [os.path.join(mask_path, i) for i in mask_path_select_list]
        image_list = [Image.open(path).convert("RGB") for path in img_path_select_list]
        self.concat_images(image_list)

    def processed_IR_imgs_concat_images(self, image_list):
        self.concat_images(image_list)

    def recog_concat_images(self, images_names):
        images = [Image.open(path).convert("RGB") for path in images_names]
        self.concat_images(images)

    def concat_images(self, image_list):
        list_len = len(image_list)
        COL = math.ceil(math.sqrt(list_len))
        ROW = math.ceil(list_len/COL)
        if COL * ROW > 16:
            COL = 4
            ROW = 4
        # COL = 4  # 指定拼接图片的列数
        # ROW = 4  # 指定拼接图片的行数
        UNIT_HEIGHT_SIZE = 0  # 图片高度
        UNIT_WIDTH_SIZE = 0  # 图片宽度
        max_UNIT_HEIGHT_SIZE = 0
        max_UNIT_WIDTH_SIZE = 0
        # self.image_list = []
        for index in range(len(image_list)):
            # self.image_list.append(Image.open(image_names[index]).convert("RGB"))  # 读取所有用于拼接的图片
            # self.image_list.append(Image.open(image_names[index]))  # 读取所有用于拼接的图片
            UNIT_WIDTH_SIZE = image_list[index].width
            UNIT_HEIGHT_SIZE = image_list[index].height

            if UNIT_WIDTH_SIZE > max_UNIT_WIDTH_SIZE:
                max_UNIT_WIDTH_SIZE = UNIT_WIDTH_SIZE
            if UNIT_HEIGHT_SIZE > max_UNIT_HEIGHT_SIZE:
                max_UNIT_HEIGHT_SIZE = UNIT_HEIGHT_SIZE

        self.set_size = max(max_UNIT_WIDTH_SIZE, max_UNIT_HEIGHT_SIZE)

        concat_image = Image.new('RGB', (self.set_size * COL, self.set_size * ROW), color=(255, 255, 255))  # 创建成品图的画布
        # 第一个参数RGB表示创建RGB彩色图，第二个参数传入元组指定图片大小，第三个参数可指定颜色，默认为黑色
        count = 0
        for row in range(ROW):
            for col in range(COL):
                # 对图片进行逐行拼接
                # paste方法第一个参数指定需要拼接的图片，第二个参数为二元元组（指定复制位置的左上角坐标）
                # 或四元元组（指定复制位置的左上角和右下角坐标）
                count = COL * row + col
                if count <= list_len - 1:
                    pad_img = self.img_pad(image_list[COL * row + col])
                    concat_image.paste(pad_img, (0 + self.set_size * col, 0 + self.set_size * row))
                else:
                    break
        concat_image.thumbnail((self.parent().ui.graphicsView.height(), self.parent().ui.graphicsView.width()), Image.ANTIALIAS)
        # return concat_image
        self.concatimg_signal_send.emit(concat_image, image_list)



