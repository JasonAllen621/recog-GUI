from PIL import Image, ImageOps
from PyQt5.QtCore import pyqtSignal, QObject
import math

class img_concat(QObject):
    imglist_path_signal_recieve = pyqtSignal(object)
    concatimg_signal_send = pyqtSignal(Image.Image, list)

    def __init__(self):
        super(img_concat, self).__init__()
        self.image_list = []

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

    def concat_images(self, image_names):
        list_len = len(image_names)
        COL = math.ceil(math.sqrt(list_len))
        ROW = round(list_len/COL)
        print(COL, ROW)
        if COL * ROW > 16:
            COL = 4
            ROW = 4
        # COL = 4  # 指定拼接图片的列数
        # ROW = 4  # 指定拼接图片的行数
        UNIT_HEIGHT_SIZE = 0  # 图片高度
        UNIT_WIDTH_SIZE = 0  # 图片宽度
        max_UNIT_HEIGHT_SIZE = 0
        max_UNIT_WIDTH_SIZE = 0
        self.image_list = []
        for index in range(len(image_names)):
            self.image_list.append(Image.open(image_names[index]).convert("RGB"))  # 读取所有用于拼接的图片
            UNIT_WIDTH_SIZE = self.image_list[index].width
            UNIT_HEIGHT_SIZE = self.image_list[index].height

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
                    pad_img = self.img_pad(self.image_list[COL * row + col])
                    concat_image.paste(pad_img, (0 + self.set_size * col, 0 + self.set_size * row))
                else:
                    break
        concat_image.thumbnail((500, 600), Image.ANTIALIAS)
        # return concat_image
        self.concatimg_signal_send.emit(concat_image, self.image_list)



