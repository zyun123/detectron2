"""
将图片旋转90度，同时将标注文件的内容，box和keypoint，line 都跟着旋转
"""
import copy
import cv2
import json

import os
import numpy as np

img_dir = "/911G/mergeData/middle_down_wai（736套）更新/middle_down_wai"
new_img_dir = "/911G/mergeData/middle_down_wai（736套）更新/middle_down_wai_trainrot90"
# os.makedirs(new_img_dir,exist_ok=True)

def rot90_img(img,clockwise = True):
    """
    clockwise:为True时是顺时针旋转  False的时候是逆时针旋转
    """
    if clockwise:
        img = np.rot90(img,-1)
    else:
        img = np.rot90(img,1)
    return img
        

def chage_90_json(data_dict,clockwise = True):
    """
    clockwise: 为True时，图像顺时针旋转，对应的box和keypoint也要跟着旋转
    """
    img_height = data_dict['imageHeight']
    img_width = data_dict['imageWidth']
    for shape in data_dict['shapes']:
        # if shape['label'] == 'person':
        if False:
            tlx = shape['points'][0][0] #左上角x
            tly = shape['points'][0][1] #左上角y
            brx = shape['points'][1][0] #右下角x
            bry = shape['points'][1][1] #左上角y
            if clockwise:
                new_tlx = img_height - bry
                new_tly = tlx
                new_brx = img_height - tly
                new_bry = brx
                # pass
            else:
                new_tlx = tly
                new_tly = img_width - brx
                new_brx = bry
                new_bry = img_width - tlx
                # pass
            shape['points'] = [[new_tlx,new_tly],[new_brx,new_bry]]
        else:
            #这里不管是关键点 还是线段  都通用
            new_points = []
            for point in shape['points']:
                cx = point[0]
                cy = point[1]
                if clockwise:
                    new_cx = img_height - cy
                    new_cy = cx
                    # pass
                else:
                    new_cx = cy
                    new_cy = img_width - cx
                    # pass
                point = [new_cx,new_cy]
                new_points.append(point)
            
            shape['points'] = new_points
    return data_dict




if __name__ == "__main__":
    img_dir = "/911G/mergeData/middle_down_wai（736套）更新/middle_down_wai"
    new_img_dir = "/911G/mergeData/middle_down_wai（736套）更新/middle_down_wai_trainrot90"

    #设定旋转方向
    clockwise = True  #True表示顺时针

    os.makedirs(new_img_dir,exist_ok=True)
    for img in os.listdir(img_dir):
        if img.endswith("json"):
            continue
        img_path = os.path.join(img_dir,img) #图片路径
        json_path = img_path.replace("jpg","json") #对应的json路径

        image = cv2.imread(img_path)
        new_image = rot90_img(image,clockwise = clockwise)

        with open(json_path,"r") as f:
            data_dict = json.load(f)

        new_data_dict = chage_90_json(data_dict,clockwise = clockwise)

        new_image_path = os.path.join(new_img_dir,img) #新的路径
        new_json_path = new_image_path.replace("jpg","json")

        with open(new_json_path,"w") as f:
            json.dump(new_data_dict,f,indent=4)

        cv2.imshow("img",new_image)
        cv2.waitKey(1)
        cv2.imwrite(new_image_path,new_image)
    cv2.destroyAllWindows()
