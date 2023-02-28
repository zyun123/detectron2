"""
分析模型里的参数
"""
import torch
import numpy as np
import json
import os


model_path = "output/2023-02-14-vis01/model_0000099.pth"
m_dict = torch.load(model_path,map_location="cpu")
print(m_dict.keys())