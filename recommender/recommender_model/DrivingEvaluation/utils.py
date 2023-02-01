import torch
from typing import List, Callable
import numpy as np
from torch import nn
from torch.utils.data import DataLoader


class ImpactWave:

    def __init__(self, gamma, lb, hb):
        self.alpha = np.zeros(shape=[len(gamma) + 1, ], dtype=np.float)
        self.mu = len(gamma) + 1
        self.num_layer = len(gamma) + 1
        self.alpha[:] = 0.01
        self.alpha[-1] = 1.
        self.hist_mu = [self.mu]
        self.lb, self.hb = lb, hb

    def update_wave_and_get_alpha(self, v: List[float], wave_func: Callable) -> np.ndarray:
        if len(v) < 3:
            return self.alpha

        if (v[-1] - v[-2]) * (v[-2] - v[-3]) > 0.0:
            x = np.arange(1.0, self.num_layer + 1, 1)
            if v[-1] - v[-2] < 0:
                print('Alphas are increased')
                self.mu = min(self.num_layer - 1, self.mu + 1)
                y = wave_func(x, self.mu, self.hb, self.lb, 1.)
            else:
                print('Alphas are decreased')
                self.mu = max(2, self.mu - 1)
                y = wave_func(x, self.mu, self.hb, 1., self.lb)
            self.alpha = y * self.alpha
            self.hist_mu.append(self.mu)
            self.alpha[:-1] = np.clip(self.alpha[:-1], 0.001, 1.)
            self.alpha[-1] = 1.0
            return self.alpha

        return self.alpha


def vectorize_list_of_tensor(l: List[torch.Tensor]) -> torch.Tensor:
    vectors_list = list()
    for t in l:
        vectors_list.append(t.view(-1))
    v = torch.cat(vectors_list, dim=0)
    return v


def vectorize_list_of_numpy(l: List[np.ndarray]) -> np.ndarray:
    vectors_list = list()
    for n in l:
        vectors_list.append(np.reshape(n, [-1]))
    return np.concatenate(vectors_list, axis=0)


def vectorize_list_gradient_tensor(l: List[torch.Tensor]) -> torch.Tensor:
    vectors_list = list()
    for t in l:
        vectors_list.append(t.grad.view(-1))
    v = torch.cat(vectors_list, dim=0)
    return v


def norm_of_the_outer_product(x: np.ndarray, y: np.ndarray):
    if x.shape[0] != y.shape[0]:
        raise Exception()
    xy = np.outer(x, y)
    return np.linalg.norm(xy)


def compute_C(net: nn.Module) -> List:
    c_weights = net.c_weights
    c_list = list()
    for c_weight in c_weights:
        sum = 0
        for w in c_weight:
            sum += np.prod(w.shape)
        c_list.append(sum)
    return c_list


def compute_grad_list(grad_list: List[torch.Tensor]) -> List[np.ndarray]:
    result = list()
    for t in grad_list:
        result.append(t.grad.detach().cpu().numpy())
    return result


def compute_Omega(pax, data_loader: DataLoader) -> List[float]:
    grad_list = list()
    data_loader_iter = iter(data_loader)
    d = data_loader_iter.__next__()
    x, y = d[0].cuda(), d[1].cuda()
    losses = pax(x, y)
    net = pax.net
    for i in range(len(losses)):
        l_val = losses[i]
        l_val.backward(retain_graph=True)
        if i < len(losses) - 1:
            grad_list.append(compute_grad_list(net.o_weights[i]))
        else:
            grad_list.append(compute_grad_list(net.o_weights[-1]))

    v = vectorize_list_of_numpy(grad_list[-1])
    result = list()
    for i in range(len(losses) - 1):
        v1 = vectorize_list_of_numpy(grad_list[i])
        vp = v[:v1.shape[0]]
        result.append(np.linalg.norm(v1 - vp))

    return result


import sys


def print_progress_bar(iteration, total, epoch, metrics=dict(), prefix='', suffix='', decimals=1, length=50, fill='█'):
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filled_length = int(length * iteration // total)
    bar = fill * filled_length + '▒' * (length - filled_length)
    format_str = '\r%s |%s| %s%% %s ( Epoch %i|'
    illustrate_tuple = (prefix, bar, percent, suffix, epoch)
    for m in metrics:
        format_str += ' ' + m + ' %02f|'
        illustrate_tuple = illustrate_tuple + (metrics[m],)
    format_str = format_str[:-1]
    format_str += ')'
    sys.stdout.write(format_str % illustrate_tuple)
    sys.stdout.flush()
    if iteration == total:
        print()


def normalize(x):
    max_x = np.max(x)
    min_x = np.min(x)
    x = (x - min_x) / (max_x - min_x)
    return x


def linear_wav(x, mu, hb, a, b):
    y1 = (hb - a) / (mu - 1) * (x[:mu] - 1) + a
    y2 = (hb - b) / (mu - x[-1]) * (x[mu:] - x[-1]) + b
    y = np.concatenate([y1, y2], axis=0)
    return y


def exponential_wav(x, mu, hb, a, b):
    y1 = np.exp(x[:mu])
    y2 = np.exp(mu - x[mu:])

    y1 = normalize(y1)
    y2 = normalize(y2)

    y1 = (hb - a) * y1 + a
    y1 = (hb - b) * y1 + b

    y = np.concatenate([y1, y2], axis=0)
    return y


def gaussian_wav(x, mu, hb, a, b):
    y1 = 1 / np.sqrt(2 * np.pi) * np.exp(-(x[:mu] - mu) ** 2)
    y2 = 1 / np.sqrt(2 * np.pi) * np.exp(-(x[mu:] - mu) ** 2)

    y1 = normalize(y1)
    y2 = normalize(y2)

    y1 = (hb - a) * y1 + a
    y1 = (hb - b) * y1 + b

    y = np.concatenate([y1, y2], axis=0)
    return y
