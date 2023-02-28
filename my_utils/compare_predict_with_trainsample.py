"""
将训练的模型 用于预测训练样本， 比较两者差异
"""

import json
import numpy as np
import os
import matplotlib.pyplot as plt



from demo.keypoints_names import *
jl_names = COCO_PERSON_KEYPOINT_NAMES_DOWN+COCO_PERSON_KEYPOINT_NAMES_HEAD_MIDDLE_DOWN
# jl_names = ['L-sanjiao-1', 'L-sanjiao-2', 'L-sanjiao-3', 'L-sanjiao-4', 'L-sanjiao-5',
                # 'L-sanjiao-6', 'L-sanjiao-7', 'L-sanjiao-8', 'L-sanjiao-9']


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
    pred_dir = "/911G/data/temp/20221229新加手托脚托新数据/精确标注320套middle_down_wai_change_rec/train"
    train_dir = "/911G/data/temp/20221229新加手托脚托新数据/精确标注320套middle_down_wai_change_rec/train_predict_new"

    files = []
    diff_xs = []
    diff_ys = []
    diff_dists = []

    for file in os.listdir(pred_dir):
        if file.endswith("json"):
            pred_js_file = os.path.join(pred_dir,file)
            train_js_file = os.path.join(train_dir,file)

            pred_kp = get_kp_with_instances(pred_js_file,jl_names)
            train_kp = get_kp_with_instances(train_js_file,jl_names)

            diff_x, diff_y , diff_dist = compare_and_draw_diff(pred_kp, train_kp)
            files.append(file)
            diff_xs.append(diff_x)
            diff_ys.append(diff_y)
            diff_dists.append(diff_dist)
    diff_xs = np.abs(np.array(diff_xs))
    diff_ys = np.abs(np.array(diff_ys))
    diff_dists = np.array(diff_dists)

    
    axis_x = range(0,320)
    base_line = [5]*320
    # plt.subplot()
    plt.figure(figsize = (320,56),dpi = 60) #设置图形
    for i in range(diff_xs.shape[1]):
        # plt.figure(figsize = (320,10),dpi = 80) #设置图形
        # plt.subplot(56,1,i+1)
        axis_y = diff_xs[:,i]
        # plt.plot(axis_x,(axis_y+i).tolist(),color=(np.random.randint(0,255),np.random.randint(0,255),np.random.randint(0,255)),label = jl_names[i],zorder = (i+1)*5)
        # plt.plot(axis_x,axis_y,label = jl_names[i])
        plt.plot(axis_x,axis_y)
        plt.plot(axis_x,base_line)



        plt.title(f"keyponts x_diff")
        plt.grid(alpha = 0.5)
        plt.yticks(np.linspace(1,10,10))
        # plt.xticks(np.linspace(1,320,320),files,rotation = 30)
        plt.xticks(np.linspace(1,320,320))
    plt.legend(jl_names)
    plt.show()
    save_dir = "/911G/data/temp/20221229新加手托脚托新数据/精确标注320套middle_down_wai_change_rec/plt_images"
    # plt.savefig(os.path.join(save_dir,f"{jl_names[i]}.jpg"))
    plt.savefig(os.path.join(save_dir,"x_difff.jpg"))
    print("compare down")



