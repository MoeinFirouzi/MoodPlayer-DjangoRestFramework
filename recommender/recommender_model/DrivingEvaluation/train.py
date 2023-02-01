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

net = MyNetwork().cpu()
w = list(net.parameters())[0]
loss = nn.MSELoss()
opt = Adamax(net.parameters(), 1e-3, weight_decay=5e-4)
ad = AdaptiveDropout(net, [1.0, 1.0, 0.8], verbose=True)
writer = SummaryWriter('./weight-decay')


# writer = SummaryWriter('./adaptive-dropout')
# writer = SummaryWriter('./dropout')
# writer = SummaryWriter('./laliga')


def weights_init(m):
    if isinstance(m, nn.Conv2d) or isinstance(m, nn.Linear):
        m.weight.data = xavier_normal_(m.weight.data)


net.apply(weights_init)

train_data = DriverDataset()
test_data = DriverDataset(False)

train_loader = DataLoader(train_data, batch_size=120)
test_loader = DataLoader(test_data, batch_size=120)

max_epoch = 100
for epoch in range(max_epoch):
    pbar = tqdm(enumerate(train_loader), total=len(train_loader), ncols=100, position=0, leave=True)
    train_loss = 0.
    for i, batch in pbar:
        opt.zero_grad()
        output = net(batch[0].float().cpu())
        output = torch.squeeze(output)
        loss_batch = loss(output, batch[1].cpu())
        loss_batch.backward()
        opt.step()
        train_loss += loss_batch
        pbar.set_description("[%i/%i] Train Loss is %f" % ((epoch + 1), max_epoch, train_loss / (i + 1)))

    test_loss = compute_loss(net, loss, test_loader)
    train_loss /= len(train_loader)
    ad.update(train_loss, test_loss, 2, 1.1)
    writer.add_scalar('loss/train', train_loss)
    writer.add_scalar('loss/test', test_loss)
    print('Test Loss is {0}'.format(test_loss))
    #sleep(0.1)

writer.close()
torch.save(net.state_dict(), 'network_120_cpu.pth')
