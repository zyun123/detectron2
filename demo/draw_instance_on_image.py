"""
将预标的json文件的数据画在图上
"""


import json
import os
import cv2
import numpy as np
import glob
import shutil

kpnames = ['L-pangguang-4','L-pangguang-5','L-pangguang-6','L-pangguang-40','R-pangguang-4','R-pangguang-5','R-pangguang-6','R-pangguang-40',
                'du-20','du-21','du-22']
connection_rules = [
    ('L-pangguang-4', 'L-pangguang-5', (0 ,255, 255)),
    ('L-pangguang-5', 'L-pangguang-6', (0 ,255, 255)),
    ('L-pangguang-6', 'L-pangguang-40', (0 ,255, 255)),
    ('R-pangguang-4', 'R-pangguang-5', (0 ,255, 255)),
    ('R-pangguang-5', 'R-pangguang-6', (0 ,255, 255)),
    ('R-pangguang-6', 'R-pangguang-40', (0 ,255, 255)),
    ('du-20', 'du-21', (255,255,0)),    
    ('du-21', 'du-22', (255,255,0)),   
]



root_dir = "/911G/data/new_all_jldata/test_images/global_pred"
new_draw_dir = os.path.join(os.path.dirname(root_dir),os.path.basename(root_dir)+"draw_on_image")
os.makedirs(new_draw_dir,exist_ok=True)
js_list = glob.glob(os.path.join(root_dir, "*.json"))
for js_file in js_list:
    img_file = js_file.replace("json","jpg")
    img  = cv2.imread(img_file)
    with open(js_file,"r") as f:
        data_dict = json.load(f)

    shapes = data_dict["shapes"]
    visible = {}
    for shape in shapes:
        if shape['label'] == "person" or shape['label'] =="leg":
            continue
        else:
            kp_x = int(shape['points'][0][0])
            kp_y = int(shape['points'][0][1])
            kp_name = shape['label']
            cv2.circle(img,(kp_x,kp_y),2,(0,0,255),2,8)
            visible[kp_name] = (kp_x, kp_y)
    for kp0,kp1,color in connection_rules:
        if kp0 in visible and kp1 in visible:
            x0, y0 = visible[kp0]
            x1, y1 = visible[kp1]
            # color = tuple(x / 255.0 for x in color)
            cv2.line(img,(x0,y0),(x1,y1),color,1,8)


    cv2.imwrite(os.path.join(new_draw_dir,os.path.basename(img_file)),img)

    # shutil.rmtree(js_file)