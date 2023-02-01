from network import NetworkWithDropout, AuxiliaryNetwork
from torch.utils.tensorboard import SummaryWriter
from utils import *
from torch.optim import *
from typing import List
from torch import nn
from torch.utils.data import DataLoader
import torch
from numpy import linalg
import numpy as np


def compute_loss(net: nn.Module, loss: nn.Module, data_loader: DataLoader, multi_output=False):
    total = 0
    with torch.no_grad():
        for data in data_loader:
            batch_x = data[0].float().cpu()
            batch_y = data[1].cpu()
            if multi_output:
                output = net(batch_x)[0]
            else:
                output = net(batch_x)
            output = torch.squeeze(output)
            total += loss(output, batch_y.long())

    return total / len(data_loader)


class AdaptiveDropout:

    def __init__(self, net: NetworkWithDropout, beta: List[float], verbose=False):
        self.beta = beta
        self.net = net
        self.verbose = verbose
        for d in self.net.dropout_layer:
            d[0].p = 1e-3

    def update(self, train_loss, val_loss, M1, M2):
        v = val_loss / train_loss
        dropout_list = self.net.dropout_layer
        if v > M1:
            for i, d in enumerate(dropout_list):
                s = v * d[1]
                if 0 < s < 5:
                    d[0].p *= self.beta[0]
                elif 5 <= s < 10:
                    d[0].p *= self.beta[1]
                elif 10 <= s:
                    d[0].p *= self.beta[2]
                if d[0].p > 0.7:
                    d[0].p = 0.7
                if self.verbose:
                    print('Dropout value for layer {0} is {1}'.format(i, d[0].p))

        elif v < M2:
            for i, d in enumerate(dropout_list):
                s = v * d[1]
                if 0 < s < 5:
                    d[0].p /= self.beta[0]
                elif 5 <= s < 10:
                    d[0].p /= self.beta[1]
                elif 10 <= s:
                    d[0].p /= self.beta[2]
                if d[0].p < 1e-20:
                    d[0].p = 1e-20
                if self.verbose:
                    print('Dropout value for layer {0} is {1}'.format(i, d[0].p))


class AuxiliaryLossFunction(nn.Module):

    def __init__(self, aux_network: AuxiliaryNetwork):
        super().__init__()
        self.net = aux_network
        self.gamma = [0, 1, 2, 3]
        self.im = ImpactWave(self.gamma, 0.5, 2.)
        self.opt = Adamax(aux_network.parameters(), 1e-3)
        self.list_w_star = list()
        self.v = list()
        self.writer = SummaryWriter('./laliga')
        self.best_loss = 10000
        self.loss_function = nn.MSELoss()

        for r_param in self.net.r_weights:
            temp_list = list()
            for w in r_param:
                temp_list.append(w.detach().cpu().numpy())
            self.list_w_star.append(temp_list)

    def forward(self, x, y):
        outputs = self.net(x)
        alpha = torch.tensor(self.im.alpha, requires_grad=False).cuda()
        loss_val = alpha[-1] * self.loss_function(outputs[-1], y)
        for i, g in enumerate(self.gamma):
            aux_loss = alpha[i] * (self.loss_function(outputs[g], y) + 0.0001 * self.create_reg_term(g))
            loss_val += aux_loss
        return loss_val

    def approximation_svd_matrix(self, w) -> np.ndarray:
        u, s, v = linalg.svd(w)
        d = self.optimal_d(s)
        s = np.diag(s)
        wa = np.dot(u[:, :d], np.dot(s[:d, :d], v[:d, :]))
        return wa

    def approximate_svd_tensor(self, w: np.ndarray) -> np.ndarray:
        w_shape = w.shape
        n1 = w_shape[0]
        n2 = w_shape[1]
        ds = []
        if w_shape[2] == 1 or w_shape[3] == 1:
            return w
        u, s, v = linalg.svd(w)
        for i in range(n1):
            for j in range(n2):
                ds.append(self.optimal_d(s[i, j]))
        d = int(np.mean(ds))
        w = np.matmul(u[..., 0:d], s[..., 0:d, None] * v[..., 0:d, :])
        return w

    @staticmethod
    def optimal_d(s):
        variance = np.std(s)
        mean = np.average(s)
        for i in range(s.shape[0] - 1):
            if s[i] < mean + variance:
                return i
        return s.shape[0] - 1

    def create_reg_term(self, i):
        list_w = self.net.r_weights[i]
        list_w_star = self.list_w_star[i]
        sub_w = list()
        for w, w_star in zip(list_w, list_w_star):
            w_star_approx = w_star
            sub_w.append(torch.norm(w - torch.tensor(w_star_approx, requires_grad=False).cuda()))
        reg = sum(sub_w)
        return reg

    def update_w_star(self, current_loss):
        if current_loss < self.best_loss:
            print('The W*s are going to be updated...')
            self.best_loss = current_loss
            for i, g in enumerate(self.gamma):
                for i, w in enumerate(self.net.r_weights[g]):
                    wt = w.detach().cpu().numpy()
                    if len(wt.shape) == 4:
                        wt = self.approximate_svd_tensor(wt)
                    elif len(wt.shape) == 2 and np.prod(wt.shape) < 300000:
                        wt = self.approximation_svd_matrix(wt)
                    self.list_w_star[g][i] = wt

    def fit(self, train_data: DataLoader, test_data: DataLoader, epochs: int = 100):
        max_batch_len = len(train_data)
        for epoch in range(1, epochs + 1):
            for i, batch in enumerate(train_data):
                self.opt.zero_grad()
                loss_val = self(batch[0].cuda(), batch[1].cuda())
                loss_val.backward()
                self.opt.step()
                print_progress_bar(i, max_batch_len, epoch, metrics={
                    'Loss Value': loss_val.detach().cpu().numpy()
                })

            test_loss_val = compute_loss(self.net, self.loss_function, test_data, multi_output=True)
            train_loss_val = compute_loss(self.net, self.loss_function, train_data, multi_output=True)

            self.writer.add_scalar('loss/train', train_loss_val)
            self.writer.add_scalar('loss/test', test_loss_val)

            self.v.append(test_loss_val / train_loss_val)
            self.im.update_wave_and_get_alpha(self.v, gaussian_wav)
            self.update_w_star(test_loss_val)
            print(test_loss_val)
            print('The ImpactWave change alpha values to ' + str(self.im.alpha))
        self.writer.close()
