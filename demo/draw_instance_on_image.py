"""
将预标的json文件的数据画在图上
"""


import json
import os
import cv2
import numpy as np
import glob
import shutil
root_dir = "/911G/data/temp/20221229新加手托脚托新数据/middle_down_wai新增采样300套数据"
new_draw_dir = os.path.join(os.path.dirname(root_dir),os.path.basename(root_dir)+"draw_on_image")
os.makedirs(new_draw_dir,exist_ok=True)
js_list = glob.glob(os.path.join(root_dir, "*.json"))
for js_file in js_list:
    img_file = js_file.replace("json","jpg")
    img  = cv2.imread(img_file)
    with open(js_file,"r") as f:
        data_dict = json.load(f)

    shapes = data_dict["shapes"]
    for shape in shapes:
        if shape['label'] == "person":
            continue
        else:
            kp_x = int(shape['points'][0][0])
            kp_y = int(shape['points'][0][1])

            cv2.circle(img,(kp_x,kp_y),1,(0,0,255),2,8)
    cv2.imwrite(os.path.join(new_draw_dir,os.path.basename(img_file)),img)

    # shutil.rmtree(js_file)