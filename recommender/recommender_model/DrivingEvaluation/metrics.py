import torch
from torch import nn
from torch.utils.data import DataLoader
from torch.utils.tensorboard import SummaryWriter
from typing import List

import torch
from torch import nn
from torch.utils.data import DataLoader


def compute_accuracy(net: nn.Module, data_loader: DataLoader, dataset_tag: str, multi_output=False,
                     writer: SummaryWriter = None):
    correct = 0
    total = 0
    with torch.no_grad():
        for data in data_loader:
            train_x = data[0].cuda()
            train_y = data[1].cuda()
            if multi_output:
                outputs = net(train_x)
                for o in outputs:
                    outputs[-1] += o
                outputs = outputs[-1]
            else:
                outputs = net(train_x)
            _, predicted = torch.max(outputs.data, 1)
            if len(train_y.shape) > 1:
                _, target = torch.max(train_y.data, 1)
            else:
                target = train_y
            total += train_y.size(0)
            correct += (predicted == target).sum().item()
    acc = 100. * correct / total
    print('\nAccuracy of the network on the %s data is: %f %%' % (dataset_tag,
                                                                  acc))
    if writer is not None:
        writer.add_scalar("Main Accuracy", acc)

    return 100. * correct / total


def compute_accuracy_with_aux(net: nn.Module, data_loader: DataLoader, dataset_tag: str, gamma, alpha):
    correct = 0
    total = 0
    with torch.no_grad():
        for data in data_loader:
            train_x = data[0].cuda()
            train_y = data[1].cuda()
            outputs = net(train_x)
            output_gamma = list()
            for g in gamma:
                output_gamma.append(outputs[g])
            output = outputs[-1]
            for i, o in enumerate(output_gamma):
                output += alpha[i] * o
            _, predicted = torch.max(output.data, 1)
            if len(train_y.shape) > 1:
                _, target = torch.max(train_y.data, 1)
            else:
                target = train_y
            total += train_y.size(0)
            correct += (predicted == target).sum().item()

    print('\nAccuracy of the network on the %s data is: %f %%' % (dataset_tag,
                                                                  100. * correct / total))

    return 100. * correct / total


def compute_accuracy_batch(net: nn.Module, input_data, target_data, multi_output=False):
    with torch.no_grad():
        train_x = input_data
        train_y = target_data
        outputs = net(train_x)
        if multi_output:
            for o in outputs:
                outputs[-1] += o
            outputs = outputs[-1]
        _, predicted = torch.max(outputs.data, 1)
        if len(train_y.shape) > 1:
            _, target = torch.max(train_y.data, 1)
        else:
            target = train_y
        total = train_y.size(0)
        correct = (predicted == target).sum().item()

    return 100 * correct / total


def compute_loss_on_batch(net: nn.Module, loss: nn.Module, batch_x: torch.Tensor, batch_y: torch.Tensor,
                          multi_output=False):
    with torch.no_grad():
        outputs = net(batch_x)
        if multi_output:
            return loss(outputs[-1], batch_y).detach().cpu().numpy()
        return loss(outputs, batch_y).detach().cpu().numpy()


def compute_loss(net: nn.Module, loss: nn.Module, data_loader: DataLoader, dataset_tag, multi_output):
    total_loss = 0
    counter = 0
    with torch.no_grad():
        for data in data_loader:
            train_x = data[0].cuda()
            train_y = data[1].cuda()
            if multi_output:
                outputs = net(train_x)[-1]
            else:
                outputs = net(train_x)
            outputs = torch.squeeze(outputs)
            total_loss += loss(outputs, train_y)
            counter += 1

    print('\nLoss of the network on the %s data is: %f' % (dataset_tag,
                                                           total_loss / counter))

    return total_loss / counter


def compute_sub_accuracy(net: nn.Module, data_loader: DataLoader, gamma, dataset_tag='Test',
                         writers: List[SummaryWriter] = None):
    accuracies = []
    correct = 0
    total = 0
    with torch.no_grad():
        for g in gamma:
            for data in data_loader:
                train_x = data[0].cuda()
                train_y = data[1].cuda()
                outputs = net(train_x)
                _, predicted = torch.max(outputs[g].data, 1)
                if len(train_y.shape) > 1:
                    _, target = torch.max(train_y.data, 1)
                else:
                    target = train_y
                total += train_y.size(0)
                correct += (predicted == target).sum().item()
            accuracies.append(100. * correct / total)
            total = 0
            correct = 0

    if writers is not None:
        for i in range(len(accuracies)):
            writers[i].add_scalar('AccuracySubNetwork', accuracies[i])
    for a in accuracies:
        print('\nAccuracy of the network on the %s data is: %f %%' % (dataset_tag, a))
