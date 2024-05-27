from PyQt5.QtWidgets import QApplication, QGraphicsView, QGraphicsScene, QWidget, QVBoxLayout
from PyQt5.QtGui import QImage, QPixmap, QWheelEvent, QPainter
from PyQt5.QtCore import Qt
from PIL import Image


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


if __name__ == "__main__":
    app = QApplication([])
    scene = QGraphicsScene()

    # 添加图像到场景中
    image = QImage("0000.png")
    pixmap = QPixmap.fromImage(image)
    scene.addPixmap(pixmap)

    view = CustomGraphicsView()
    view.setScene(scene)

    widget = QWidget()
    layout = QVBoxLayout(widget)
    layout.addWidget(view)
    widget.show()

    app.exec()


