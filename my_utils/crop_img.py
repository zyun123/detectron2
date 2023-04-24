"""
裁剪人体图像，并保存
"""
import os
import json
import cv2
import numpy as np
import glob

def get_dataDict(json_path):
        '''得到json'内容'''
        with open(json_path, 'r') as f:
            dataDict = json.load(f)
            return dataDict

def get_new_image(img,start_x,start_y,end_x,end_y):
    """
    img:原图像
    start_x:左上角坐标
    start_y:左上角坐标
    end_x:右下角坐标
    end_y:右下角坐标
    """
    new_image = img[start_y:end_y,start_x:end_x,:]
    return new_image

def crop_image(root_dir,new_dir):
    
    for jsfile in glob.glob(os.path.join(root_dir,"*.json")):
        imgfile = jsfile.replace(".json",".jpg")
        img = cv2.imread(imgfile)
        data_dict = get_dataDict(jsfile)
        shapes = data_dict["shapes"]
        new_shapes = []
        for shape in shapes:
            if shape['label'] == "person":
                person_points = shape['points'] #[[x,y],[x,y]]
                points = [int(person_points[0][0]),int(person_points[0][1]),
                        int(person_points[1][0]),int(person_points[1][1])]
                new_image = get_new_image(img,*points)
                new_image_h,new_image_w = new_image.shape[:2]
                new_image_path = os.path.join(new_dir,os.path.basename(imgfile))
                cv2.imwrite(new_image_path,new_image)
        for shape in shapes:
            if len(shape['label'].split('-')) == 3:
                kpx,kpy = shape['points'][0]
                new_points = [[kpx - points[0],kpy - points[1]]]
                shape['points'] = new_points
                new_shapes.append(shape)
        
        data_dict['shapes'] = new_shapes
        data_dict['imageHeight'] = new_image_h
        data_dict['imageWidth'] = new_image_w

        new_js_path = os.path.join(new_dir,os.path.basename(jsfile))
        with open(new_js_path,"w") as f:
            json.dump(data_dict,f,indent=4)


if __name__ == "__main__":
    root_dir = "/911G/data/temp/20221229新加手托脚托新数据/精确标注494套middle_up_nei_changerec/origin_whole_label_image"
    new_dir = "/911G/data/temp/20221229新加手托脚托新数据/精确标注494套middle_up_nei_changerec/hrnet_data"
    os.makedirs(new_dir,exist_ok=True)
    crop_image(root_dir,new_dir)


