"""
统计一下数据集里所有图像的最大shape
"""

import json
import cv2
import numpy as np
import glob
import os

def cal_shape(root_dir):
    max_w,max_h = 0,0
    for imgfile in glob.glob(os.path.join(root_dir,"*.jpg")):
        img =cv2.imread(imgfile)
        
        h,w = img.shape[:2]
        max_w= max(max_w,w)
        max_h = max(max_h,h)

    print("max_h = {}, max_w = {}".format(max_h,max_w))



if __name__ == "__main__":
    root_dir = "/911G/data/temp/20221229新加手托脚托新数据/精确标注494套middle_up_nei_changerec/hrnet_data"
    cal_shape(root_dir)