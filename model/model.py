from torchvision import models
from torch import nn, load
import os

cur_path = os.path.abspath(__file__)
parent_path = os.path.abspath(os.path.dirname(cur_path) + os.path.sep + '.')
net_select = {
    "VGG11": models.vgg11_bn(),
    "RESNET50": models.resnet50(),
    "CONVNEXTsmall": models.convnext_small(),
    "RESNEXT50": models.resnext50_32x4d(),
    "DENSENET121": models.densenet121(),
    "EFFECIENETm": models.efficientnet_v2_m(),
    "REGNETY16GF": models.regnet_y_16gf()
}

class net_cllect(nn.Module):
    def __init__(self, net_type, class_num):
        super(net_cllect, self).__init__()

        self.net = nn.Sequential(
            net_select[net_type],
            nn.ReLU(),
            nn.Linear(1000, class_num),
            nn.Softmax(dim=-1)
        )

    def forward(self, x):
        return self.net(x)

def net_load(net_type, net_path, class_num):
    a = net_cllect(net_type, class_num).eval()
    a.load_state_dict(load(
        net_path
    ))
    return a

