import torch
from torch import nn
from torch.optim import *
from torch.nn.init import xavier_normal_
from torch.utils.tensorboard import SummaryWriter
from tqdm import tqdm
from time import sleep

from model import *
from network import *
from dataset import *

net = AuxiliaryNetwork().cuda()


# writer = SummaryWriter('./adaptive-dropout')
# writer = SummaryWriter('./dropout')
# writer = SummaryWriter('./laliga')


def weights_init(m):
    if isinstance(m, nn.Conv2d) or isinstance(m, nn.Linear):
        m.weight.data = xavier_normal_(m.weight.data)


net.apply(weights_init)

train_data = DriverDataset()
test_data = DriverDataset(False)

train_loader = DataLoader(train_data, batch_size=256)
test_loader = DataLoader(test_data, batch_size=256)

mdl = AuxiliaryLossFunction(net)
mdl.fit(train_loader, test_loader)
