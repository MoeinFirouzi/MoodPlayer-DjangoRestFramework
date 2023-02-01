from torch.utils.data import Dataset
import torchvision.transforms as T
import scipy.io as spio
import numpy as np


class DriverDataset(Dataset):

    def __init__(self, train=True):
        # data = spio.loadmat('dataSetAcc1200Normal.mat')
        data = spio.loadmat('python_dataset_120.mat')
        if train:
            tag = 'train'
        else:
            tag = 'test'

        self.input_data = data['{0}_input'.format(tag)]
        self.target_data = self.input_data[:, :2, :]
        self.target_data = np.array(np.squeeze(data['{0}_target'.format(tag)]), dtype=np.float32)

    def __len__(self):
        return self.input_data.shape[0]

    def __getitem__(self, idx):
        sample_input = np.squeeze(self.input_data[idx])
        sample_input = np.reshape(sample_input, [120, 3])

        sample_target = self.target_data[idx]
        sample_input = np.expand_dims(sample_input, axis=0)
        return sample_input, sample_target
