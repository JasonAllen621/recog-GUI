import os.path
import random
import cv2
import numpy as np
from PIL import Image
import numpy
from PyQt5.QtCore import pyqtSignal, QObject

from utils.utils import process_sea, superimpose, process_sky, process_clutter, get_sea_level

class change_IR_bkg(QObject):
    imglist_path_signal_recieve = pyqtSignal(object)
    changed_img_signal_send = pyqtSignal(list)

    def __init__(self):
        super(change_IR_bkg, self).__init__()
        self.label = []
        self.image = []
        self.sealevel = []
        # 可能有多个（其顺序一定是按照[sea, sky, clutter]赋值的）
        self.itensity = []
        self.bkg_image = []
    pass

    def add_sea(self):
        mask = label[sea_level:, ...].copy()
        image_lower = image[sea_level:, ...]
        # path = os.path.join("../irships/augment/sea", "horizontal" if sea_level != 0 else "elevated")
        # sea_image = random.choice(os.listdir(path))
        # sea_image = cv2.imread(os.path.join(path, sea_image), cv2.IMREAD_GRAYSCALE)
        sea_image = process_sea(
            sea_image,
            shape=image_lower.shape[0:2],
            average_intensity=int(np.mean(image_lower)),
            intensity_range=intensity
        )
        image[sea_level:, ...] = superimpose(image_lower, sea_image, mask)
        return image

    def add_sky(self, image, label, sea_level, intensity):
        mask = label[0: sea_level, ...].copy()  # Mask of foreground pixels to preserve
        image_top = image[0:sea_level, ...]  # Top half of image
        background_temp = int(np.mean(image_top))  # Average background temperature
        clouds = process_sky(
            sky=sky_image,
            shape=image_top.shape[0:2],
            lower=background_temp,
            upper=background_temp + intensity
        )
        image[0:sea_level, ...] = superimpose(image_top, clouds, mask)
        return image

    def add_clustter(self, image, label, sea_level, intensity, clutter_height):
        orig_image = image.copy()
        clutter = process_clutter(clutter_image, image.shape, intensity[clustter_type], clutter_height)
        y0 = sea_level - clutter.shape[0]
        # Make ship and clutter masks
        ship_mask = label[y0: sea_level:, ...].copy()
        clutter_mask = clutter.copy()
        clutter_mask[clutter > 0] = 1
        clutter_mask = 1 - clutter_mask
        # Superimpose clutter and ship
        image[y0: sea_level, ...] = superimpose(image[y0: sea_level, ...], clutter, clutter_mask)
        image[y0: sea_level, ...] = superimpose(orig_image[y0: sea_level, ...], clutter, ship_mask)
        return image