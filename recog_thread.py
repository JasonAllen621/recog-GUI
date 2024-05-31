import torch
from torchvision import transforms
from torch import nn, sort, unsqueeze
import os
from PyQt5.QtCore import pyqtSignal, QObject
from model.model import net_cllect, parent_path
import json



with open("./model/classes.json", "r") as f:
    classes_label_dict = json.load(f)

net_list = {
    "OPT": {
        "net": ["RESNEXT50", "DENSENET121", "REGNETY16GF"],
        # "path": [],
        "label": len(classes_label_dict["OPT"])
    },
    "SAR": {
        "net": ["RESNEXT50", "DENSENET121", "REGNETY16GF"],
        # "path": [],
        "label": len(classes_label_dict["SAR"])
    },
    "INFRAD": {
        "net": ["DENSENET121"],
        # "path": [],
        "label": len(classes_label_dict["INFRAD"])
    },
}

model_record_list = []

class object_recog(QObject):
    class_n_prob_signal_send = pyqtSignal(list)

    net_id_signal_recieve = pyqtSignal(str, int)
    recog_image_signal_receive = pyqtSignal(list)

    def __init__(self):
        super(object_recog, self).__init__()
        self.net = net_cllect("RESNEXT50", "test", net_list["OPT"]["label"])
        self.net_id = ["OPT", 0]

        self.transform = transforms.Compose([
        transforms.Resize((128, 128)),
        transforms.ToTensor(),
    ])

    def net_select(self, source, i):
        if self.net_id == [source, i]:
            pass
        else:
            self.net = net_cllect(net_list[source]["net"][i], "test", net_list[source]["label"])
            self.net_id = [source, i]
        # print(self.net_id)
            # self.net.load_state_dict(torch.load())

    def trans_pretreat(self, img_list):
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
                class_n_prob = [(classes_label_dict[self.net_id[0]][idx], percentage[idx].item()) for idx in indices[0][:2]]
                # print(class_n_prob)
            else:
                idx = indices[0][0]
                class_n_prob.append((classes_label_dict[self.net_id[0]][idx], percentage[idx].item()))
                # print(class_n_prob)

        # print(class_n_prob)

        self.class_n_prob_signal_send.emit(class_n_prob)

        # 原文链接：https: // blog.csdn.net / u013679159 / article / details / 104253030
        # return [(self.classes[idx], percentage[idx].item()) for idx in indices[0][:5]]









