'''
将预测的关键点保存为json文件，以便于labelme软件打开进行修改标注
input: predictions(box,classes,keypoints)
        keypoints_names
output:jsonfile
'''

import json
import os
import cv2
import numpy as np


class MyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        elif isinstance(obj, bytes):
            return str(obj, encoding='utf-8')
        return json.JSONEncoder.default(self, obj)

def create_shapes(keypoints,box,kp_names,img_width,h_flip=False):
    assert len(keypoints) >0, "keypoints is None"
    assert len(box)>0, "box is None"
    assert len(keypoints) ==len(kp_names) , "keypoints must match kp_names length"
    shapes = []
    shape = {}
    shape["label"] = "person"
    if h_flip:
        shape["points"] = [[img_width-box[2],box[1]],[img_width-box[0],box[3]]]
    else:
        shape["points"] = [[box[0],box[1]],[box[2],box[3]]]
    shape["group_id"] = None
    shape["shape_type"] = "rectangle"
    shape["flags"] = {}
    shapes.append(shape)
    
    for i,kp in enumerate(keypoints):
        tmp_shape = {}
        tmp_shape["label"] = kp_names[i]
        if h_flip:
            tmp_shape["points"] = [[img_width-kp[0],kp[1]]]
        else:
            tmp_shape["points"] = [[kp[0],kp[1]]]
        tmp_shape["group_id"] = None
        tmp_shape["shape_type"] = "point"
        tmp_shape["flags"] = {}
        shapes.append(tmp_shape)
    return shapes



def save_predictions_to_json(predictions,kp_names,img_path,h_flip=False):
    """主程序

    Args:
        predictions (dict): predict 预测的结果 {"instance":Instance}  box = Instances.pred_boxes keypoints = Instances.pred_keypoints
        kp_names (list): 关键点的名字和顺序
    """
    box_list = predictions["instances"].pred_boxes.tensor.cpu().numpy().tolist()
    if len(box_list) == 0:
        return
    box = box_list[0]
    keypoints = predictions["instances"].pred_keypoints.squeeze().cpu().numpy().tolist()
    js_path = img_path.replace("jpg","json") #json file save path
    imagePath = os.path.basename(img_path)
    
    dataDict = {}
    dataDict["version"] = "4.5.6"
    dataDict["flages"] = {}
    dataDict["imagePath"] = imagePath
    dataDict["imageData"] = None
    dataDict["imageHeight"] = 720
    dataDict["imageWidth"] = 1280

    img_width = dataDict["imageWidth"]
    shapes = create_shapes(keypoints,box,kp_names,img_width,h_flip)
    dataDict["shapes"] = shapes

    with open(js_path,"w") as f:
        json.dump(dataDict,f,indent=4,cls = MyEncoder)
    print(js_path,"save done!")



def replace_jsfile_box(predictions,js_file):
    """
    用现有的模型预测 ， 只取出box，来替换原有的对应的json文件上的框
    """
    box_list = predictions["instances"].pred_boxes.tensor.cpu().numpy().tolist()
    box = box_list[0]

    with open(js_file,"r") as f:
        dataDict = json.load(f)


    shapes = dataDict["shapes"]
    img_width = dataDict["imageWidth"]
    for shape in shapes:
        if shape["label"] == "person":
            shape["points"] = [[box[0],box[1]],[box[2],box[3]]]

    with open(js_file,"w") as f:
        json.dump(dataDict,f,indent=4,cls = MyEncoder)
