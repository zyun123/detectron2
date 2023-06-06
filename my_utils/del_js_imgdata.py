"""
将每个json数据里的imgae data清除掉
"""
import json
import os
import numpy as np
import glob


def del_image_data(root_dir):
    """
    刪除所有json文件里的imagedata
    """
    for jsfile in glob.glob(os.path.join(root_dir,"*.json")):
        with open(jsfile,"r") as f:
            data_dict = json.load(f)
        data_dict["imageData"] = None
        # data_dict['imageHeight'] = 720
        # data_dict['imageWidth'] = 1280
        print(data_dict["imagePath"])

        with open(jsfile,"w") as f:
            json.dump(data_dict,f,indent=4)

def del_shape_with_jl_names(root_dir,filter_names):
    """
    根据filter_names里的穴位点名，删除json文件里的对应的shape
    filter_names:需要删除的穴位点
    """
    n = 1
    for jsfile in glob.glob(os.path.join(root_dir,"*.json")):
        n+=1
        print(n)
        with open(jsfile,"r") as f:
            data_dict = json.load(f)
        
        # for i,shape in enumerate(data_dict['shapes']):
        for i in range(len(data_dict['shapes'])-1,-1,-1):
            if data_dict['shapes'][i]['label'] in filter_names:
                del data_dict['shapes'][i]


        with open(jsfile,"w") as f:
            json.dump(data_dict,f,indent=4)
    
def create_rec_with_kp(root_dir):
    """
    主要用于创建脚和手局部框
    """
    for jsfile in glob.glob(os.path.join(root_dir,"*.json")):
        
        xyxy = {}
        rec_xy = []
        with open(jsfile,"r") as f:
            data_dict = json.load(f)
        for shape in data_dict['shapes']:
            xyxy[shape['label']] = shape['points'][0]
        
        leg_rec = [[xyxy['R-pi-1'][0]-20,
                    xyxy['R-wei-30'][1]-20],
                    [xyxy['L-pi-7'][0]+20,
                    xyxy['L-wei-30'][1]+20]]

        r_hand_rec = [[xyxy['R-xinbao-7'][0]-15,
                    xyxy['R-fei-8'][1]-15],
                    [xyxy['R-fei-6'][0]+15,
                    xyxy['R-xinbao-9'][1]+25]]

        l_hand_rec = [[xyxy['L-xinbao-7'][0]-15,
                    xyxy['L-xinbao-9'][1]-25],
                    [xyxy['L-fei-6'][0]+15,
                    xyxy['L-fei-8'][1]+15]]

        leg_shape = {"label": "leg",
                        "points":leg_rec,
                        "group_id": None,
                        "shape_type":"rectangle",
                        "flags":{}}
        r_hand_shape = {"label": "hand",
                        "points":r_hand_rec,
                        "group_id": None,
                        "shape_type":"rectangle",
                        "flags":{}}
        l_hand_shape = {"label": "hand",
                        "points":l_hand_rec,
                        "group_id": None,
                        "shape_type":"rectangle",
                        "flags":{}}

        # print(data_dict["imagePath"])
        data_dict['shapes'].append(leg_shape)
        data_dict['shapes'].append(r_hand_shape)
        data_dict['shapes'].append(l_hand_shape)
        with open(jsfile,"w") as f:
            json.dump(data_dict,f,indent=4)


def change_person_rectangle(root_dir):
    """
    将人体框扩大一点
    """
    for jsfile in glob.glob(os.path.join(root_dir,"*.json")):
        with open(jsfile,"r") as f:
            data_dict = json.load(f)
        for shape in data_dict['shapes']:
            if shape['label'] == "person":
                points = shape['points']
                print("origin points:",points)
                shape['points'] = [[points[0][0],points[0][1]],
                                    [points[1][0]-20,points[1][1]]]
                print("new points:",shape['points'])
                break
        with open(jsfile,"w") as f:
            json.dump(data_dict,f,indent=4)

def delete_keypoint(root_dir):
    for jsfile in glob.glob(os.path.join(root_dir,"*.json")):
        with open(jsfile,"r") as f:
            data_dict = json.load(f)
        new_shape = []
        for shape in data_dict['shapes']:
            if shape["shape_type"] == "rectangle":
                new_shape.append(shape)
        data_dict['shapes'] = new_shape
        with open(jsfile,"w") as f:
            json.dump(data_dict,f,indent=4)



        



if __name__ == "__main__":
    # root_dir = "/911G/mergeData/0301经修改middle_down_wai/middle_down_wai"
    # root_dir = "/911G/data/temp/20221229新加手托脚托新数据/精确标注494套middle_up_nei_multi_kp/train"
    root_dir = "/911G/data/cure_images/一楼拷贝数据/up_nei/middle_up_nei"

    # filter_names = ['person']
    # del_shape_with_jl_names(root_dir,filter_names = filter_names)
    # create_rec_with_kp(root_dir)
    # del_image_data(root_dir) #删除图像数据
    # change_person_rectangle(root_dir)
    delete_keypoint(root_dir)