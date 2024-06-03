import torch
from torchvision import transforms
from torch import nn, sort, unsqueeze
from PyQt5.QtCore import pyqtSignal, QObject
from utils.model import net_load
import json


class object_recog(QObject):
    class_n_prob_signal_send = pyqtSignal(list)

    net_id_signal_recieve = pyqtSignal(str, int)
    recog_image_signal_receive = pyqtSignal(list)

    def __init__(self):
        super(object_recog, self).__init__()

        with open("model/classes.json", "r") as f:
            self.classes_label_dict = json.load(f)

        self.net_list = {
            "OPT": {
                "net": ["RESNEXT50", "DENSENET121", "REGNETY16GF"],
                "path": [r"model/model/OPT/RESNEXT50/model_epoch71_ACC0.9796_LOSS2.3478.pth",
                         r"model/model/OPT/DENSENET121/model_epoch172_ACC0.9732_LOSS2.3807.pth",
                         r"model/model/OPT/REGNETY16GF/model_epoch147_ACC0.9647_LOSS2.3621.pth"],
                "label": len(self.classes_label_dict["OPT"])
            },
            "SAR": {
                "net": ["RESNEXT50", "DENSENET121", "REGNETY16GF"],
                "path": [r"model/model/SAR/RESNEXT50/model_epoch42_ACC0.6960_LOSS2.0931.pth",
                         r"model/model/SAR/DENSENET121/model_epoch90_ACC0.8259_LOSS1.9448.pth",
                         r"model/model/SAR/REGNETY16GF/model_epoch69_ACC0.8935_LOSS1.9001.pth"],
                "label": len(self.classes_label_dict["SAR"])
            },
            "INFRAD": {
                "net": ["DENSENET121"],
                "path": [r"model/model/INFRAD/DENSENET121/model_epoch26_ACC0.9882_LOSS0.7570.pth"],
                "label": len(self.classes_label_dict["INFRAD"])
            },
        }

        self.net = net_load("RESNEXT50", self.net_list["OPT"]["path"][0], self.net_list["OPT"]["label"])
        self.net_id = ["OPT", 0]
        self.trans_dict = {
            "OPT": transforms.Compose([transforms.Resize((128, 128)),
                                       transforms.ToTensor()]),
            "SAR": [transforms.Compose([transforms.CenterCrop(300),
                                        transforms.Resize((128, 128)),
                                        transforms.ToTensor()]),
                    transforms.Compose([transforms.Resize((128, 128)),
                                        transforms.ToTensor()])],
            "INFRAD": transforms.Compose([transforms.CenterCrop(512),
                                          transforms.Resize((128, 128)),
                                          transforms.ToTensor()]),
        }

        self.transform = self.trans_dict["OPT"]

    def net_select(self, source, i):
        if self.net_id == [source, i]:
            pass
        else:
            self.net = net_load(self.net_list[source]["net"][i], self.net_list[source]["path"][i], self.net_list[source]["label"])
            self.net_id = [source, i]
            self.transform = self.trans_dict[source]
        # print(self.net_id)
            # self.net.load_state_dict(torch.load())

    def trans_pretreat(self, img_list):
        if self.net_id[0] == "SAR":
            if img_list[0].size[0] > 300:
                tensor_list = unsqueeze(self.transform[0](img_list[0]), 0)
            else:
                tensor_list = unsqueeze(self.transform[1](img_list[0]), 0)

            for idx in range(1, len(img_list)):
                if img_list[idx].size[0] > 300:
                    tensor_temporal = unsqueeze(self.transform[0](img_list[idx]), 0)
                else:
                    tensor_temporal = unsqueeze(self.transform[1](img_list[idx]), 0)
                tensor_list = torch.concat((tensor_list, tensor_temporal), dim=0)
        else:
            tensor_list = unsqueeze(self.transform(img_list[0]), 0)
            for idx in range(1, len(img_list)):
                tensor_list = torch.concat((tensor_list, unsqueeze(self.transform(img_list[idx]), 0)), dim=0)
        return tensor_list

    def recog(self, img):
        # print(cuda)
        img = self.trans_pretreat(img)
        # print(img.shape)
        with torch.no_grad():
            # print("cpu")
            self.net = self.net.cpu()
            a = self.net(img)

        label = a.cpu()
        class_n_prob = []
        for i in label:
            i = unsqueeze(i, 0)
            _, indices = sort(i, descending=True)
            percentage = nn.functional.softmax(i, dim=1)[0] * 100

            if a.shape[0] == 1:
                class_n_prob = [(self.classes_label_dict[self.net_id[0]][idx], percentage[idx].item()) for idx in indices[0][:2]]
                # print(class_n_prob)
            else:
                idx = indices[0][0]
                class_n_prob.append((self.classes_label_dict[self.net_id[0]][idx], percentage[idx].item()))
                # print(class_n_prob)

        # print(class_n_prob)

        self.class_n_prob_signal_send.emit(class_n_prob)

        # 原文链接：https: // blog.csdn.net / u013679159 / article / details / 104253030
        # return [(self.classes[idx], percentage[idx].item()) for idx in indices[0][:5]]









