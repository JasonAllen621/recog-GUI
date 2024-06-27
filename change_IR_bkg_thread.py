import os.path
import random
import cv2
from PIL import Image
import numpy as np
import pandas as pd
import contextlib
from PyQt5.QtCore import pyqtSignal, QObject

from utils.utils import process_sea, superimpose, process_sky, process_clutter, get_sea_level, get_random_value

class change_IR_bkg(QObject):
    processed_IR_imgs_signal_send = pyqtSignal(list)
    rand_set_signal_recieve = pyqtSignal(str, dict, str)
    custom_set_signal_recieve = pyqtSignal(str, dict, str)
    QMessage_signal_send = pyqtSignal(str)

    def __init__(self):
        super(change_IR_bkg, self).__init__()

        pass

    def add_sea(self, path, image, label, sea_level, intensity):
        mask = label[sea_level:, ...].copy()
        image_lower = image[sea_level:, ...]
        sea_image = Image.open(path).convert("RGB")
        sea_image = cv2.cvtColor(np.asarray(sea_image), cv2.COLOR_RGB2GRAY)
        sea_image = process_sea(
            sea_image,
            shape=image_lower.shape[0:2],
            average_intensity=int(np.mean(image_lower)),
            intensity_range=intensity
        )
        image[sea_level:, ...] = superimpose(image_lower, sea_image, mask)
        return image

    def add_sky(self, path, image, label, sea_level, intensity):
        mask = label[0: sea_level, ...].copy()  # Mask of foreground pixels to preserve
        image_top = image[0:sea_level, ...]  # Top half of image
        background_temp = int(np.mean(image_top))  # Average background temperature
        sky_image = Image.open(path).convert("RGB")
        sky_image = cv2.cvtColor(np.asarray(sky_image), cv2.COLOR_RGB2GRAY)
        clouds = process_sky(
            sky=sky_image,
            shape=image_top.shape[0:2],
            lower=background_temp,
            upper=background_temp + intensity
        )
        image[0:sea_level, ...] = superimpose(image_top, clouds, mask)
        return image

    def add_clustter(self, path, image, label, sea_level, intensity, clutter_height):
        orig_image = image.copy()
        clutter_image = Image.open(path).convert("RGB")
        clutter_image = cv2.cvtColor(np.asarray(clutter_image), cv2.COLOR_RGB2GRAY)
        clutter = process_clutter(clutter_image, image.shape, intensity, clutter_height)
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

    def rand_set_bkg(self, csv_path, cfg_dict, object_img_root_path):
        csv_content = pd.read_csv(csv_path)
        self.processed_img = []
        for i in range(cfg_dict["idx"][0] - 1, cfg_dict["idx"][1]):
            image_path = os.path.join(object_img_root_path, f"images/{csv_content.iloc[i].filename}")
            label_path = os.path.join(object_img_root_path, f"labels/{csv_content.iloc[i].labelname}")
            if os.path.exists(image_path) and os.path.exists(label_path):
                image = Image.open(image_path).convert("RGB")
                image = cv2.cvtColor(np.asarray(image), cv2.COLOR_RGB2GRAY)
                label = Image.open(label_path).convert("RGB")
                label = cv2.cvtColor(np.asarray(label), cv2.COLOR_RGB2GRAY)
                sea_level = get_sea_level(image) if csv_content.iloc[i].pitch == 0 else 0
                sea_intensity = np.random.randint(5, 30)
                sky_intensity = np.random.randint(2, 30)
                clutter_intensity_range = {
                    "ice": (0, 5),
                    "structure": (20, 70),
                    "landscape": (15, 60)
                }
                clustter_intensity = clutter_intensity_range
                for key, item in clutter_intensity_range.items():
                    with contextlib.suppress(TypeError):
                        clustter_intensity[key] = np.random.randint(*item)
                path = os.path.join(cfg_dict["path"], "sea/horizontal" if sea_level != 0 else "sea/elevated")
                sea_image = random.choice(os.listdir(path))
                image = self.add_sea(os.path.join(path, sea_image), image, label, sea_level, sea_intensity)
                if csv_content.iloc[i].pitch == 0:
                    path = os.path.join(cfg_dict["path"], "sky")
                    sky_image = random.choice(os.listdir(path))
                    image = self.add_sky(os.path.join(path, sky_image), image, label, sea_level, sky_intensity)

                    clutter_height_range = (0.2, 0.7)
                    clutter_height = get_random_value(*clutter_height_range)
                    clutter_height = max(10, int(clutter_height * sea_level))

                    path = os.path.join(cfg_dict["path"], "clutter")
                    clustter_type = random.choice(os.listdir(path))
                    clutter_image = random.choice(os.listdir(os.path.join(path, clustter_type)))
                    image = self.add_clustter(os.path.join(path, f"{clustter_type}/{clutter_image}"), image, label, sea_level, clustter_intensity[clustter_type], clutter_height)
                self.processed_img.append(Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB)))
            else:
                msg_str = ""
                if not os.path.exists(image_path):
                    msg_str = msg_str + f"{image_path} 文件不存在\n"
                if not os.path.exists(label_path):
                    msg_str = msg_str + f"{label_path} 文件不存在\n"
                self.QMessage_signal_send.emit(msg_str)
        if len(self.processed_img) == 0:
            self.QMessage_signal_send.emit("配置文件中图像均不存在")
        else:
            self.processed_IR_imgs_signal_send.emit(self.processed_img)

    def custom_set_bkg(self, csv_path, cfg_dict, object_img_root_path):
        csv_content = pd.read_csv(csv_path)
        self.processed_img = []
        for i in range(cfg_dict["idx"][0] - 1, cfg_dict["idx"][1]):
            image_path = os.path.join(object_img_root_path, f"images/{csv_content.iloc[i].filename}")
            label_path = os.path.join(object_img_root_path, f"labels/{csv_content.iloc[i].labelname}")
            if os.path.exists(image_path) and os.path.exists(label_path):
                image = Image.open(image_path).convert("RGB")
                image = cv2.cvtColor(np.asarray(image), cv2.COLOR_RGB2GRAY)
                label = Image.open(
                    os.path.join(object_img_root_path, f"labels/{csv_content.iloc[i].labelname}")).convert("RGB")
                label = cv2.cvtColor(np.asarray(label), cv2.COLOR_RGB2GRAY)
                sea_level = get_sea_level(image) if csv_content.iloc[i].pitch == 0 else 0
                image = self.add_sea(cfg_dict["sea"][0], image, label, sea_level, cfg_dict["sea"][1])
                if csv_content.iloc[i].pitch == 0:
                    image = self.add_sky(cfg_dict["sky"][0], image, label, sea_level, cfg_dict["sky"][1])
                    # clutter_height_range = (0.2, 0.7)
                    # clutter_height = get_random_value(*clutter_height_range)
                    # clutter_height = max(10, int(clutter_height * sea_level))
                    image = self.add_clustter(cfg_dict["clutter"][0], image, label, sea_level, cfg_dict["clutter"][1], 0.5 * sea_level)
                self.processed_img.append(Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB)))
            else:
                msg_str = ""
                if not os.path.exists(image_path):
                    msg_str = msg_str + f"{image_path} 文件不存在\n"
                if not os.path.exists(label_path):
                    msg_str = msg_str + f"{label_path} 文件不存在\n"
                self.QMessage_signal_send.emit(msg_str)
        if len(self.processed_img) == 0:
            self.QMessage_signal_send.emit("配置文件中图像均不存在")
        else:
            self.processed_IR_imgs_signal_send.emit(self.processed_img)