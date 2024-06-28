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
import os
import json

file_type_dict = {
    "source": [".ui", '.png', '.jpg', '.jpeg', '.pt', '.pth', '.ico', '.pyc'],
    "file": ['.py']
}

def traverse_folder(folder_path, extension, exclude_folders=[]):
    file_paths = []

    for root, dirs, files in os.walk(folder_path):
        # 排除指定的文件夹
        dirs[:] = [d for d in dirs if d not in exclude_folders]

        for file in files:
            if file.endswith(extension):
                file_paths.append(os.path.join(root, file))

    return file_paths



# 示例用法
folder_path = r'F:\1A研究生\实验\for_graduation_pyqt'  # 指定要遍历的文件夹路径
exclude_folders = ['dist', 'build', 'pic4detect']  # 指定要排除的文件夹列表

file_record_dict = {
    "source": [],
    "file": []
}
for i in ["source", "file"]:
    for extension in file_type_dict[i]:

        print(extension)
        # extension = '.pt'  # 指定文件后缀名
        file_paths = traverse_folder(folder_path, extension, exclude_folders)

        if i == "source":
            for file_path in file_paths:
                a = (file_path, file_path.replace("\\" + file_path.split("\\")[-1], '').replace("F:\\1A研究生\\实验\\for_graduation_pyqt\\", ''))
                # print(a)
                file_record_dict[i].append(a)
        else:
            for file_path in file_paths:
                file_record_dict[i].append(file_path)
# print(file_record_dict)

with open("./utils/file_path_record.json", "w+", encoding='utf-8') as f:
    f.write(json.dumps(file_record_dict, indent=4, ensure_ascii=False))

for i in file_record_dict["source"]:
    print(i,',')

