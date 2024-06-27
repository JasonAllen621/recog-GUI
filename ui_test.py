from PyQt5.QtWidgets import QApplication, QGraphicsView, QGraphicsScene, QWidget, QVBoxLayout
from PyQt5.QtGui import QImage, QPixmap, QWheelEvent, QPainter
from PyQt5.QtCore import Qt
from PIL import Image
from qt_material import list_themes

# 导入pprint接口，可以打印出更加漂亮的list列表数据
from pprint import pprint




class CustomGraphicsView(QGraphicsView):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setRenderHint(QPainter.Antialiasing)
        self.setDragMode(QGraphicsView.ScrollHandDrag)
        self.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)
        self.setResizeAnchor(QGraphicsView.AnchorUnderMouse)

    def wheelEvent(self, event: QWheelEvent):
        if event.modifiers() == Qt.ControlModifier:
            delta = event.angleDelta().y() / 120
            zoom_factor = 1.2 ** delta
            self.scale(zoom_factor, zoom_factor)
        else:
            super().wheelEvent(event)

'''
['dark_amber.xml',
 'dark_blue.xml',
 'dark_cyan.xml',
 'dark_lightgreen.xml',
 'dark_medical.xml',
 'dark_pink.xml',
 'dark_purple.xml',
 'dark_red.xml',
 'dark_teal.xml',
 'dark_yellow.xml',
 'light_amber.xml',
 'light_blue.xml',
 'light_blue_500.xml',
 'light_cyan.xml',
 'light_cyan_500.xml',
 'light_lightgreen.xml',
 'light_lightgreen_500.xml',
 'light_orange.xml',
 'light_pink.xml',
 'light_pink_500.xml',
 'light_purple.xml',
 'light_purple_500.xml',
 'light_red.xml',
 'light_red_500.xml',
 'light_teal.xml',
 'light_teal_500.xml',
 'light_yellow.xml']
'''
if __name__ == "__main__":
    # app = QApplication([])
    # scene = QGraphicsScene()
    #
    # # 添加图像到场景中
    # image = QImage("0000.png")
    # pixmap = QPixmap.fromImage(image)
    # scene.addPixmap(pixmap)
    #
    # view = CustomGraphicsView()
    # view.setScene(scene)
    #
    # widget = QWidget()
    # layout = QVBoxLayout(widget)
    # layout.addWidget(view)
    # widget.show()
    #
    # app.exec()
    image_path = "ui/logo.jpg"
    image = Image.open(image_path)

    # 将图像转换为 RGBA 模式
    image = image.convert("RGBA")

    # 获取图像的像素数据
    data = image.getdata()

    # 创建一个新的像素列表，将白色背景替换为透明
    new_data = []
    for item in data:
        # 判断像素是否为白色
        if item[:3] >= (235, 235, 235):
            new_data.append((255, 255, 255, 0))  # 替换为透明
        else:
            new_data.append(item)

    # 更新图像的像素数据
    image.putdata(new_data)

    # 保存处理后的图像
    image.save("ui/logo.png", format="PNG")



