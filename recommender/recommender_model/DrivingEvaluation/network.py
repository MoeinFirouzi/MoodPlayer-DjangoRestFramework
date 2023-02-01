from torch import nn
import torch
from typing import List


class NetworkWithDropout(nn.Module):

    def __init__(self):
        super().__init__()
        # The list which contain Dropout layer, and value of s_i without v(t) (please look at Eq.3 in the paper)
        self.dropout_layer: List[List[nn.Dropout, float]] = list()


class SimpleNetwork(NetworkWithDropout):

    # In the paper the Axis Z is omitted. Also, you can omit this axis.
    def __init__(self):
        super().__init__()
        p = 1e-4
        self.dropout_layer = [
            [nn.Dropout(p), 9600 / 131072 * 1 / 7],
            [nn.Dropout(p), 51200 / 131072 * 2 / 7],
            [nn.Dropout(p), 51200 / 131072 * 3 / 7],
            [nn.Dropout(p), 622592 / 131072 * 4 / 7],
            [nn.Dropout(p), 131072 / 131072 * 5 / 7],
            [nn.Dropout(p), 4096 / 131072 * 6 / 7]
        ]
        self.feature = nn.Sequential(*[
            nn.Conv2d(1, 128, kernel_size=[200, 3], stride=[4, 1]),
            nn.ReLU(),
            self.dropout_layer[0][0],
            nn.Conv2d(128, 256, kernel_size=[100, 1], stride=[4, 1]),
            nn.ReLU(),
            self.dropout_layer[1][0],
            nn.Conv2d(256, 512, kernel_size=[25, 1], stride=[4, 1]),
            nn.ReLU(),
            self.dropout_layer[2][0],
        ])

        self.classifier = nn.Sequential(*[
            nn.Linear(2048, 512),
            nn.ReLU(),
            # self.dropout_layer[3][0],
            nn.Linear(512, 256),
            nn.ReLU(),
            # self.dropout_layer[4][0],
            nn.Linear(256, 16),
            nn.ReLU(),
            # self.dropout_layer[5][0],
            nn.Linear(16, 1),
        ])

    def forward(self, x: torch.Tensor):
        feature = self.feature(x)
        feature = feature.view(feature.size(0), -1)
        y = self.classifier(feature)
        return y


class MyNetwork(NetworkWithDropout):

    def __init__(self):
        super().__init__()
        p = 0.0
        self.dropout_layer = [
            [nn.Dropout(p), 28800 / 983040 * 1 / 7],
            [nn.Dropout(p), 409600 / 983040 * 2 / 7],
            [nn.Dropout(p), 983040 / 983040 * 3 / 7],
            [nn.Dropout(p), 65536 / 983040 * 4 / 7],
            [nn.Dropout(p), 4096 / 983040 * 5 / 7]
        ]
        self.conv1 = nn.Sequential(*[
            nn.Conv2d(1, 32, kernel_size=[120, 3]),
            self.dropout_layer[0][0],
            nn.BatchNorm2d(32),
            nn.ReLU(),
            #nn.MaxPool2d(kernel_size=[4, 1], stride=[4, 1])
        ])

        self.conv2 = nn.Sequential(*[
            nn.Conv2d(32, 128, kernel_size=[1, 1]),
            self.dropout_layer[1][0],
            nn.BatchNorm2d(128),
            nn.ReLU(),
            #nn.MaxPool2d(kernel_size=[4, 1], stride=[4, 1])
        ])

        self.conv3 = nn.Sequential(*[
            nn.Conv2d(128, 256, kernel_size=[1, 1]),
            self.dropout_layer[2][0],
            nn.BatchNorm2d(256),
            nn.ReLU(),
        ])

        self.linear = nn.Sequential(*[
            nn.Linear(256, 128),
            self.dropout_layer[3][0],
            nn.ReLU(),
            nn.Linear(128, 32),
            self.dropout_layer[4][0],
            nn.ReLU(),
            nn.Linear(32, 1),
        ])

    def forward(self, x):
        y = self.conv1(x)
        y = self.conv2(y)
        y = self.conv3(y)

        y = y.view(y.size(0), -1)
        y = self.linear(y)

        return y


class AuxiliaryNetwork(nn.Module):

    def __init__(self):
        super().__init__()
        self.r_weights = list()
        r_weight = list()
        self.conv1 = nn.Sequential(*[
            nn.Conv2d(1, 32, kernel_size=[300, 3]),
            nn.BatchNorm2d(32),
            nn.ReLU(),
            nn.MaxPool2d(kernel_size=[4, 1], stride=[4, 1])
        ])

        self.aux_1 = nn.Linear(7200, 1)
        r_weight.append(self.conv1[0].weight)
        r_weight.append(self.aux_1.weight)
        self.r_weights.append(r_weight)

        self.conv2 = nn.Sequential(*[
            nn.Conv2d(32, 128, kernel_size=[100, 1]),
            nn.BatchNorm2d(128),
            nn.ReLU(),
            nn.MaxPool2d(kernel_size=[4, 1], stride=[4, 1])
        ])

        self.aux_2 = nn.Linear(3968, 1)
        r_weight.append(self.conv2[0].weight)
        r_weight.append(self.aux_2.weight)
        self.r_weights.append(r_weight)

        self.conv3 = nn.Sequential(*[
            nn.Conv2d(128, 256, kernel_size=[30, 1]),
            nn.BatchNorm2d(256),
            nn.ReLU(),
        ])

        self.aux_3 = nn.Linear(512, 1)
        r_weight.append(self.conv3[0].weight)
        r_weight.append(self.aux_3.weight)
        self.r_weights.append(r_weight)

        self.linear1 = nn.Sequential(*[
            nn.Linear(512, 128),
            nn.ReLU()])

        self.aux_4 = nn.Linear(128, 1)
        r_weight.append(self.linear1[0].weight)
        r_weight.append(self.aux_4.weight)
        self.r_weights.append(r_weight)

        self.linear2 = nn.Sequential(*[
            nn.Linear(128, 32),
            nn.ReLU(),
            nn.Linear(32, 1)
        ])

    def forward(self, x):
        y = self.conv1(x)
        y1 = self.aux_1(y.view(y.size(0), -1))
        y = self.conv2(y)
        y2 = self.aux_2(y.view(y.size(0), -1))
        y = self.conv3(y)
        y3 = self.aux_3(y.view(y.size(0), -1))

        y = y.view(y.size(0), -1)
        y = self.linear1(y)
        y4 = self.aux_4(y)
        y = self.linear2(y)
        return [y4, y3, y2, y1, y]


class PlainNetwork(nn.Module):
    def __init__(self):
        super().__init__()
        self.conv = nn.Sequential(*[
            nn.Conv2d(1, 32, kernel_size=[300, 3]),
            nn.BatchNorm2d(32),
            nn.ReLU(),
            nn.MaxPool2d(kernel_size=[4, 1], stride=[4, 1]),
            nn.Conv2d(32, 128, kernel_size=[100, 1]),
            nn.BatchNorm2d(128),
            nn.ReLU(),
            nn.MaxPool2d(kernel_size=[4, 1], stride=[4, 1]),
            nn.Conv2d(128, 256, kernel_size=[30, 1]),
            nn.BatchNorm2d(256),
            nn.ReLU(),
        ])

        self.linear = nn.Sequential(*[
            nn.Linear(512, 128),
            nn.ReLU(),
            nn.Linear(128, 32),
            nn.ReLU(),
            nn.Linear(32, 1)
        ])

    def forward(self, x):
        y = self.conv(x)
        y = y.view(y.size(0), -1)
        y = self.linear(y)
        return y
