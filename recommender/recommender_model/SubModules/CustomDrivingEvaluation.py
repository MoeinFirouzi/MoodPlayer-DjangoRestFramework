from torch.utils.data import Dataset
from torchvision.transforms import ToTensor
import scipy.io as spio
import numpy as np
import pandas as pd

import torch
from torch.utils.data import DataLoader

from DrivingEvaluation.network import *

class Evaluator():





    def evaluate(dataframe=None, data_path=None):
        #device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
        
        net = MyNetwork()
        net.eval()
        
        if(dataframe is None and data_path is None):
            return
        elif(data_path is not None and dataframe is None):
            df = pd.read_csv(data_path)
        elif(dataframe is not None and data_path is None):
            df = dataframe
        else:
            df = dataframe

        data = Data(df)

        loader = DataLoader(data, batch_size=len(data), shuffle=False)
        batch = iter(loader).__next__()
        
        loaded_dict = torch.load('./DrivingEvaluation/network_120_cpu_0.16.pth')
        net.load_state_dict(loaded_dict)

        output = net(batch.float())
        target = torch.squeeze(output)

        if (target.size() == torch.Size([])):
            return target.item()
        else:
            avg = 0
            counter = 0
            for i in range(target.size()[0]):
                avg += target[i].item()
                counter += 1
            avg = avg / counter
            return avg


def reshape_to_batch(normal_array,size):

    reshape_batch_input = []

    rows_input = []

    for i in range(normal_array.shape[0]):
        if(len(rows_input) < size):
            rows_input.append(normal_array[i])
        else:
                
            reshape_batch_input.append(np.array(rows_input, dtype=float))

            rows_input = []

    reshape_batch_input_array = np.array(reshape_batch_input, dtype=float)

    return reshape_batch_input_array

class Data():



    def __init__(self,dataframe):

        data = np.array([dataframe['acceleration_x'].values,dataframe['acceleration_y'].values,dataframe['acceleration_z'].values]).transpose()
            
        self.input_data = data
        self.input_data = self.input_data * 10
        self.input_data = reshape_to_batch(self.input_data,120)
        #print(len(self.input_data))

    def __len__(self):
        return self.input_data.shape[0]

    def __getitem__(self, idx):
            
        sample_input = np.squeeze(self.input_data[idx])
            
        sample_input = np.reshape(sample_input, [120,3])
        #print(sample_input.shape)
        #print(torch.from_numpy(sample_input).shape)
        sample_input = np.expand_dims(sample_input, axis=0)
        #print(torch.from_numpy(sample_input).shape) 
        return torch.from_numpy(sample_input)

