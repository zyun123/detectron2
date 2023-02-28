import numpy as np
import os
import json

annotation_file = "/911G/data/temp/20221229新加手托脚托新数据/精确标注494套middle_up_nei_changerec_yolo/annotations/train.json"

with open(annotation_file, 'r') as f:
    data = json.load(f)
    annotations = data['annotations']

image_size = (720,1280)

# sigmas = np.zeros(36)

def get_keypoints_sigmas(annotations,image_size,sigmas):
    for ann in annotations:
        num_kps = ann['num_keypoints']
        kpts = ann['keypoints']
        bbox = ann['bbox']
        coords = np.array(kpts).reshape(-1,3)
        # coords = [(kpts[i],kpts[i+1],kpts[i+2]) for i in range(0,len(kpts),3)]
        distances = np.sqrt((coords[:,0] - bbox[0])**2 + (coords[:,1] - bbox[1])**2)
        sigmas += distances

    sigmas /= len(annotations)
    sigmas *= 3
    sigmas /=max(image_size)
    return sigmas


if __name__ == '__main__':
    sigmas = np.zeros(36)
    sigmas = get_keypoints_sigmas(annotations,image_size,sigmas)
    sigmas = np.round(sigmas,2).tolist()
    print(sigmas)
    print(len(sigmas))
    