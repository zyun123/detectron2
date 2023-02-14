import copy
import cv2
import json

import os
import numpy as np

person_kp_train2017_json = "/911G/data/coco-jl-middle_up(复件)/annotations/train.json"
new_json = "/911G/data/coco-jl-middle_up(复件)/annotations/train_rot90.json"
with open(person_kp_train2017_json,"r") as f:
    data_dict = json.load(f)

new_images = []
for img in data_dict["images"]:
    img["height"] = 1280
    img["width"] =720
    new_images.append(img)
data_dict["images"] = new_images


annotations = data_dict["annotations"]
new_annotations = []
for ann in annotations:
    bbox = (ann["bbox"])
    oldX = bbox[0]
    oldY = bbox[1]
    oldW = bbox[2]
    oldH = bbox[3]
    # new_bbox = [720-oldY-oldH,oldX,oldH,oldW]
    new_bbox = [oldY,1280-oldW-oldX,oldH,oldW]

    keypoints = ann["keypoints"]
    assert len(keypoints) == 3*ann["num_keypoints"], "numkeypoints is not same"
    for i in range(ann["num_keypoints"]):
        tmpx = copy.deepcopy(keypoints[i*3])

        # keypoints[i*3] = 720-keypoints[i*3+1]
        # keypoints[i*3+1] = tmpx

        keypoints[i*3] = keypoints[i*3+1]
        keypoints[i*3+1] = oldW - tmpx

    ann["bbox"] = new_bbox  
    new_annotations.append(ann)


data_dict["annotations"] = new_annotations
with open(new_json,"w") as f:
    json.dump(data_dict,f,indent=4)