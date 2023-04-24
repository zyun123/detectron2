"""
根据文本里的文件名，将图像和json文件挑选出来，存在一个文件夹里
"""

import json
import os
import shutil

def select_file(file_name,root_dir,dst_dir):
    src_file_path = os.path.join(root_dir,file_name)    
    dst_file_path = os.path.join(dst_dir,file_name)
    shutil.copyfile(src_file_path,dst_file_path)    


if __name__ == "__main__":
    root_dir = "/911G/data/cure_images/上位机第一次识别图像/小框28预测"
    dst_dir = "/911G/data/cure_images/上位机第一次识别图像/小框28预测_pick_false"
    os.makedirs(dst_dir,exist_ok=True)
    with open("/911G/data/cure_images/上位机第一次识别图像/false_point.txt","r") as f:
        files = f.readlines()
    for file in files:
        file = file.strip()
        file_name = os.path.basename(file)
        json_file_name = file_name.replace("jpg","json")
        select_file(file_name,root_dir,dst_dir)
        select_file(json_file_name,root_dir,dst_dir)
