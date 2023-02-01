import torch
from torch.utils.data import DataLoader

from network import *
from dataset import *

net = MyNetwork().cuda()
net.eval()

data = DriverDataset(False)
loader = DataLoader(data, batch_size=32, shuffle=True)
batch = iter(loader).__next__()

loaded_dict = torch.load('network.pth')
net.load_state_dict(loaded_dict)

output = net(batch[0].float().cuda())
target = torch.squeeze(output)

print('| Network Output | Target |')
for i in range(output.shape[0]):
    print('|{0}|{1}|'.format(output[i], target[i]))

print(batch[0].shape)
print(output[0].item())