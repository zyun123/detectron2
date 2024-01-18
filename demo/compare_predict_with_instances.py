"""
将训练的局部图局部模型 用于预测验证集，统计两者欧氏距离
"""

import json
import numpy as np
import os
import matplotlib.pyplot as plt
import glob
# import torch
# import pandas as pd
from keypoints_names import *
# jl_names = MIDDLE_UP_WITHOUT_FEI
#ALLJL_DOWN_RIGHT_FOOT+ALLJL_UP_LEFT_HAND+ALLJL_UP_RIGHT_HAND+ALLJL_DOWN_LEFT_HAND+ALLJL_DOWN_RIGHT_HAND+ALLJL_DOWN_RIGHT_HEAD+ALLJL_UP_LEFT_FOOT+ALLJL_UP_FACE+ALLJL_TOP_HEAD


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


def plt_diff(files,jl_names,save_dir,diff_xs,diff_dists):
    len_file = len(files)
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


def cal_mean_diff_dists(diff_dists):
    files_length , kp_nums = diff_dists.shape
    kp_mean = np.mean(diff_dists,axis = 0)


if __name__ == "__main__":
    #ALLJL_DOWN_RIGHT_FOOT   11kp
    # ALLJL_UP_LEFT_HAND
    # ALLJL_UP_RIGHT_HAND
    # ALLJL_DOWN_LEFT_HAND
    # ALLJL_DOWN_RIGHT_HAND
    # ALLJL_DOWN_RIGHT_HEAD
    # ALLJL_UP_LEFT_FOOT
    # ALLJL_UP_FACE
    # ALLJL_TOP_HEAD

    # #middle up nei left hand
    jl_names = ALLJL_UP_LEFT_HAND
    pred_dir = "/911G/data/new_all_jldata/20231226/middle_up_nei/test_crop/left_hand(复件)"
    test_dir = "/911G/data/new_all_jldata/20231226/middle_up_nei/test_crop/left_hand"

    # #middle up nei right hand
    # jl_names = ALLJL_UP_RIGHT_HAND
    # pred_dir = "/911G/data/new_all_jldata/20231226/middle_up_nei/test_crop/right_hand(复件)"
    # test_dir = "/911G/data/new_all_jldata/20231226/middle_up_nei/test_crop/right_hand"

    # #middle down wai left hand
    # jl_names = ALLJL_DOWN_LEFT_HAND
    # pred_dir = "/911G/data/new_all_jldata/20230410/middle_down_wai/test_crop/left_hand(复件)"
    # test_dir = "/911G/data/new_all_jldata/20230410/middle_down_wai/test_crop/left_hand"

    # #middle down wai right hand
    # jl_names = ALLJL_DOWN_RIGHT_HAND
    # pred_dir = "/911G/data/new_all_jldata/20230410/middle_down_wai/test_crop/right_hand(复件)"
    # test_dir = "/911G/data/new_all_jldata/20230410/middle_down_wai/test_crop/right_hand"

    # #left down wai right foot
    # jl_names = ALLJL_DOWN_RIGHT_FOOT
    # pred_dir = "/911G/data/new_all_jldata/20230410/left_down_wai/test_crop/right_foot(复件)"
    # test_dir = "/911G/data/new_all_jldata/20230410/left_down_wai/test_crop/right_foot"

    ## left down wai right head
    # jl_names = ALLJL_DOWN_RIGHT_HEAD
    # pred_dir = "/911G/data/new_all_jldata/20230410/left_down_wai/test_crop/right_head"
    # test_dir = "/911G/data/new_all_jldata/20230410/left_down_wai/test_crop/right_head(复件)"


    # #middle up nei face
    # jl_names = ALLJL_UP_FACE
    # pred_dir = "/911G/data/new_all_jldata/20230804/middle_up_nei/test_crop/face(复件)"
    # test_dir = "/911G/data/new_all_jldata/20230804/middle_up_nei/test_crop/face"

    # #left up nei left foot
    # jl_names = ALLJL_UP_LEFT_FOOT
    # pred_dir = "/911G/data/new_all_jldata/20230410/left_up_nei/test_crop/left_foot(复件)"
    # test_dir = "/911G/data/new_all_jldata/20230410/left_up_nei/test_crop/left_foot"

    #head down wai top head 
    # jl_names = ALLJL_TOP_HEAD
    # pred_dir = "/911G/data/new_all_jldata/head_down_all/test_crop/top_head(复件)"
    # test_dir = "/911G/data/new_all_jldata/head_down_all/test_crop/top_head"



    # save_dir = "/911G/data/new_all_jldata/20230410/middle_up_nei/test_crop/left_hand_compdiff"
    # os.makedirs(save_dir,exist_ok=True)

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
            test_js_file = os.path.join(test_dir,file)

            pred_kp = get_kp_with_instances(pred_js_file,jl_names)
            test_kp = get_kp_with_instances(test_js_file,jl_names)

            diff_x, diff_y , diff_dist = compare_and_draw_diff(pred_kp, test_kp)
            files.append(file)
            diff_xs.append(diff_x)
            diff_ys.append(diff_y)
            diff_dists.append(diff_dist)
    # diff_xs = np.abs(np.array(diff_xs))
    # diff_ys = np.abs(np.array(diff_ys))
    diff_xs = np.array(diff_xs)
    diff_ys = np.array(diff_ys)
    diff_dists = np.array(diff_dists).astype(int)

    # plt_diff(files,jl_names,save_dir,diff_xs,diff_dists)  ##plt diff results

    # print(diff_dists)
    print("diff_dists.shape: ",diff_dists.shape)
    print(">1pix nums: ",np.where(diff_dists > 1)[0].shape)
    print(">2pix nums: ",np.where(diff_dists > 2)[0].shape)
    print(">3pix nums: ",np.where(diff_dists > 3)[0].shape)
    # cal_mean_diff_dists(diff_dists)

    



