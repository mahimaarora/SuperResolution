#!/usr/bin/env python
# coding: utf-8

# In[1]:


import torch
import torch.nn as nn
import math
from torch.utils.data import Dataset, DataLoader
import os
from fastai.conv_learner import *
import matplotlib.pyplot as plt


# In[2]:


def conv(ni, no, kernal_size=3, actn=False):
    layers = [nn.Conv2d(ni, no, kernal_size, padding=kernal_size//2)]
    if actn:
        layers += [nn.ReLU(True)]
    return nn.Sequential(*layers)


# In[3]:


class ResSequential(nn.Module):
    def __init__(self, layers, scale=1.0):
        super().__init__()
        self.res_scale = scale
        self.m = nn.Sequential(*layers)
    def forward(self, x):
        return x + self.m(x) * self.res_scale


# In[4]:


def res_block_build(no):
    return ResSequential([conv(no, no, actn=True), conv(no, no)], 0.1)


# In[5]:


def upsample_sub_conv(ni, nf, scale):
    layers = []
    for i in range(int(math.log(scale, 2))):
        layers += [conv(ni, nf * 4, actn=False), nn.PixelShuffle(2)]
    return nn.Sequential(*layers)


# In[6]:


class SRNet(nn.Module):
    def __init__(self, scale):
        super().__init__()
        layers = [conv(3, 64)]
        for i in range(4):
            layers.append(res_block_build(64))
        layers += [conv(64, 64), upsample_sub_conv(64, 64, scale), nn.BatchNorm2d(64), conv(64, 3)]
        self.features = nn.Sequential(*layers)
    def forward(self, x):
        return self.features(x)


# In[7]:


class ImageData(Dataset):
    def __init__(self):
        self.paths = os.listdir('test_data/data')
        print(self.paths[:10])
    def __getitem__(self, index):
        #print(self.paths[index])
        return np.rollaxis(np.array(cv2.cvtColor(cv2.imread('test_data/data/' + self.paths[index]), cv2.COLOR_BGR2RGB)), 2, 0)
    def __len__(self):
        return len(self.paths)


# In[9]:


def process():
    paths = os.listdir('./data/')
    #ds = ImageData()
    #dl = DataLoader(ds, shuffle=False)
    model = SRNet(4).cuda()
    model.eval()
    model.load_state_dict(torch.load('data/imagenet/models/sr01.h5', map_location=lambda storage, loc: storage))
    for path in paths:
        img = cv2.imread('data'+path)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img = np.rollaxis(np.array(img), 2, 0)
        img = torch.unsqueeze(torch.Tensor(img), dim=0)
        img = img.cuda()
        op = model(img)
        op = np.rollaxis(op.cpu().detach().numpy(), 1, 4)
        op = op.squeeze()
        op = op.astype(np.int32)
        op = op/255
        plt.imsave('./data'+path, np.clip(op, 0, 1))
        print('saved')


# In[10]:





# In[ ]:
