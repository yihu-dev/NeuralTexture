import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.utils.data import Dataset

import numpy as np
import os
from PIL import Image

from util import augment


class UVDataset(Dataset):

    def __init__(self, dir, idx_list, H, W):
        self.idx_list = idx_list
        self.dir = dir
        self.crop_size = (H, W)

    def __len__(self):
        return len(self.idx_list)

    def __getitem__(self, idx):
        img = Image.open(os.path.join(self.dir, self.idx_list[idx]+'.ppm'), 'r')
        uv_map = np.load(os.path.join(self.dir, 'uv_'+self.idx_list[idx]+'.npy'))
        # if np.any(np.isnan(uv_map)):
        #    print('uv_map is nan', self.idx_list[idx])
        img, uv_map, mask = augment(img, uv_map, self.crop_size)
        return img, uv_map, mask


def collect_fn(data):
    images, uv_maps, masks = zip(*data)
    images = torch.cat(images, dim=0)
    uv_maps = torch.cat(uv_maps, dim=0)
    masks = torch.cat(masks, dim=0)
    return images, uv_maps, masks
