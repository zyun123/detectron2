"""
修改person rec
"""
import cv2
import os
import json
import glob
import numpy as np

def change_rec(root_dir):
    for jsfile in glob.glob(os.path.join(root_dir,"*.json")):
        with open(jsfile,"r") as f:
            data_dict = json.load(f)
        for shape in data_dict['shapes']:
            if shape['label'] == "person":
                points = shape['points']
                print("origin points:",points)
                shape['points'] = [[103,175],[1038,561]]
                print("new points:",shape['points'])
                break
        
        with open(jsfile,"w") as f:
            json.dump(data_dict,f,indent=4)


if __name__ == "__main__":
    root_dir = "/911G/data/temp/20221229新加手托脚托新数据/20230311_最新修改/middle_up_nei/test"
    change_rec(root_dir)