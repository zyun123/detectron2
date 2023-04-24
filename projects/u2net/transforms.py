import random
from typing import List, Union
from torchvision.transforms import functional as F
from torchvision.transforms import transforms as T

class Compose(object):
    def __init__(self,transforms):
        self.transforms = transforms

    def __call__(self,image,target = None):
        for t in self.transforms:
            image,target = t(image,target)
        
        return image,target
    
class ToTensor(object):
    def __call__(self,image,target):
        image = F.to_tensor(image)
        target = F.to_tensor(target)
        return image,target

