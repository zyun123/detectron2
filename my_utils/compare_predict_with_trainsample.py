"""
将训练的模型 用于预测训练样本， 比较两者差异
"""

import json
import numpy as np
import os
import matplotlib.pyplot as plt
import glob
# import torch
import pandas as pd
from demo.keypoints_names import *
# jl_names = MIDDLE_UP_WITHOUT_FEI
jl_names = ["L-xinbao-5","L-xinbao-6","L-xinbao-7","L-xinbao-8","L-xinbao-9",
"R-xinbao-5","R-xinbao-6","R-xinbao-7","R-xinbao-8","R-xinbao-9",
"L-wei-27", "L-wei-28", "L-wei-29", "L-wei-30","L-pi-1","L-pi-2","L-pi-3",
"R-wei-27", "R-wei-28", "R-wei-29", "R-wei-30","R-pi-1","R-pi-2","R-pi-3"]


def get_kp_with_instances(json_file,jl_names):
    """
    json_file: 单个json文件
    jl_names:长度和keypoints 长度相等
    """
    kps = []
    with open(json_file, 'r') as f:
        data = json.load(f)
    for accu_name in jl_names:
        for shape in data['shapes']:
            if shape['label'] == accu_name:
                kps.append(shape['points'][0])
    kps = np.array(kps)
    return kps


def compare_and_draw_diff(pred_kp, train_kp):
    """
    pred_kp:预测的关键点 array
    train_kp: 标注的关键点 array
    return :x,y,distance 差异
    """
    assert pred_kp.shape == train_kp.shape, "数组shape不一致"
    diff = pred_kp - train_kp 
    diff_x = diff[:,0]
    diff_y = diff[:,1]
    diff_dist = np.sqrt(np.sum(diff**2,axis = 1))
    return diff_x, diff_y , diff_dist

if __name__ == "__main__":
    pred_dir = "/911G/data/cure_images/上位机第一次识别图像/局部识别/局部图局部识别"
    train_dir = "/911G/data/cure_images/上位机第一次识别图像/局部识别/整体预测"
    save_dir = "/911G/data/cure_images/上位机第一次识别图像/局部识别/局部compare全局dist_diff"
    os.makedirs(save_dir,exist_ok=True)

    files = []
    diff_xs = []
    diff_ys = []
    diff_dists = []
    # files = []
    len_file = len(glob.glob(os.path.join(pred_dir,"*.json")))
    file_list = os.listdir(pred_dir)
    for file in file_list:
        if file.endswith("json"):
            # files.append(file)
            pred_js_file = os.path.join(pred_dir,file)
            train_js_file = os.path.join(train_dir,file)

            pred_kp = get_kp_with_instances(pred_js_file,jl_names)
            train_kp = get_kp_with_instances(train_js_file,jl_names)

            diff_x, diff_y , diff_dist = compare_and_draw_diff(pred_kp, train_kp)
            files.append(file)
            diff_xs.append(diff_x)
            diff_ys.append(diff_y)
            diff_dists.append(diff_dist)
    # diff_xs = np.abs(np.array(diff_xs))
    # diff_ys = np.abs(np.array(diff_ys))
    diff_xs = np.array(diff_xs)
    diff_ys = np.array(diff_ys)
    diff_dists = np.array(diff_dists).astype(int)

    comp_diff = (diff_dists>5).astype(int)
    sum1 = comp_diff.sum(axis = 1).reshape(-1,1)
    
    result = np.column_stack((comp_diff,sum1))

    sum2 = result.sum(axis = 0).reshape(1,-1)
    result = np.row_stack((result,sum2))
    files.append("max_sum")
    jl_names.append("max_sum")
    data = pd.DataFrame(result,index = files,columns =jl_names)
    with pd.ExcelWriter("compare_partial_global1.xlsx") as writer:
        data.to_excel(writer,sheet_name = "diff_dists",index= True)






    
    axis_x = range(0,len_file)
    base_line1 = [5]*len_file
    base_line2 = [-5]*len_file
    # plt.subplot()
    # plt.figure(figsize = (320,56),dpi = 60) #设置图形
    for i in range(diff_xs.shape[1]):
        plt.figure(figsize = (len_file,10),dpi = 80) #设置图形
        # plt.subplot(56,1,i+1)
        axis_y = diff_dists[:,i]
        # plt.plot(axis_x,(axis_y+i).tolist(),color=(np.random.randint(0,255),np.random.randint(0,255),np.random.randint(0,255)),label = jl_names[i],zorder = (i+1)*5)
        # plt.plot(axis_x,axis_y,label = jl_names[i])
        plt.plot(axis_x,axis_y)
        plt.plot(axis_x,base_line1)
        plt.plot(axis_x,base_line2)



        plt.title(f"keyponts dist_diff")
        plt.grid(alpha = 0.5)

        #xy刻度
        plt.yticks(np.linspace(-10,10,21))
        plt.xticks(np.linspace(0,len_file,len_file),files,rotation = 75,ha = "right")
        # plt.xticks(np.linspace(1,len_file,len_file))
        # plt.xticks(np.linspace(1,len_file,len_file))

        plt.legend([jl_names[i],"base_line:5"],"base_line:-5")
        # plt.show()
        plt.savefig(os.path.join(save_dir,f"{jl_names[i]}.jpg"))


    # plt.legend(jl_names)
    # plt.show()
    # plt.savefig(os.path.join(save_dir,"x_difff.jpg"))
    print("compare down")



