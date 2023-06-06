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

def create_shapes(keypoints,box=None,kp_names=[],img_width=1280,h_flip=False):
    assert len(keypoints) >0, "keypoints is None"
    # assert len(box)>0, "box is None"
    if len(keypoints) == 2:
        keypoints = keypoints[0]
    assert len(keypoints) ==len(kp_names) , "keypoints must match kp_names length"
    shapes = []
    shape = {}
    shape["label"] = "leg"
    if h_flip:
        shape["points"] = [[img_width-box[2],box[1]],[img_width-box[0],box[3]]]
    else:
        if box:
            assert len(box)>0, "box is None"
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



def save_predictions_to_json(box_list,keypoints,kp_names,img_path,h_flip=False):
    """主程序

    Args:
        predictions (dict): predict 预测的结果 {"instance":Instance}  box = Instances.pred_boxes keypoints = Instances.pred_keypoints
        kp_names (list): 关键点的名字和顺序
    """
    
    if len(box_list) == 0:
        return
    box = box_list[0]
    # keypoints = predictions["instances"].pred_keypoints.squeeze().cpu().numpy().tolist()
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





def merge_pred_to_other_json(box,keypoints,kp_names,origin_json_path):
    """主程序

    Args:
        predictions (dict): predict 预测的结果 {"instance":Instance}  box = Instances.pred_boxes keypoints = Instances.pred_keypoints
        kp_names (list): 关键点的名字和顺序
        将预测的信息取出大肠经，小肠经，放到原来的标注好的json文件，标注好的json文件里有三焦经和膀胱经
    """
    # keypoints = predictions["instances"].pred_keypoints.squeeze().cpu().numpy().tolist()  #预测的关键点
    if len(keypoints) == 2:
        keypoints = keypoints[0]
    assert len(keypoints) == len(kp_names),"关键点个数要和穴位名字个数一样"
    # origin_dir = ""  #标注的json文件所在的文件夹
    # origin_json_path = os.path.join(origin_dir,os.path.basename(json_path))

    #需要挑出来的存在标注文件里的经络点  大肠经和小肠经
    # filter_kp_names = ['R-dachang-1','R-dachang-2', 'R-dachang-3','R-dachang-4','R-dachang-5','R-dachang-6','R-dachang-20','R-dachang-7','R-dachang-8','L-dachang-1','L-dachang-2','L-dachang-3','L-dachang-4','L-dachang-5','L-dachang-6','L-dachang-20','L-dachang-7','L-dachang-8','L-xiaochang-1', 'L-xiaochang-2','L-xiaochang-3','L-xiaochang-4','L-xiaochang-20','L-xiaochang-5','L-xiaochang-6','L-xiaochang-7','L-xiaochang-8','L-xiaochang-9','L-xiaochang-10','L-xiaochang-11', 'L-xiaochang-12','R-xiaochang-1', 'R-xiaochang-2','R-xiaochang-3','R-xiaochang-4','R-xiaochang-20','R-xiaochang-5','R-xiaochang-6','R-xiaochang-7','R-xiaochang-8','R-xiaochang-9','R-xiaochang-10','R-xiaochang-11', 'R-xiaochang-12']
    filter_kp_names = ['L-pi-1', 'L-pi-2', 'L-pi-3', 'L-pi-4','L-pi-5', 'L-pi-6', 'L-pi-7',
                            'R-pi-1', 'R-pi-2', 'R-pi-3', 'R-pi-4','R-pi-5', 'R-pi-6', 'R-pi-7',
                            'L-wei-24', 'L-wei-25', 'L-wei-26', 'L-wei-27', 'L-wei-28', 'L-wei-29', 'L-wei-30',
                            'R-wei-24', 'R-wei-25', 'R-wei-26', 'R-wei-27', 'R-wei-28', 'R-wei-29', 'R-wei-30']
    all_kpname_xy = {}
    for i, kp_name in enumerate(kp_names):
        all_kpname_xy[kp_name] = (keypoints[i][0], keypoints[i][1])

    filter_keypoints = []
    for f_kp in filter_kp_names:
        kp = [all_kpname_xy[f_kp][0], all_kpname_xy[f_kp][1]]
        filter_keypoints.append(kp)
    shapes = create_shapes(filter_keypoints,kp_names = filter_kp_names)


    with open(origin_json_path,"r") as f:
        data_dict = json.load(f)
    
    data_dict["shapes"].extend(shapes)  

    with open(origin_json_path, "w") as f:
        json.dump(data_dict,f,indent=4)
    