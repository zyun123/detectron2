import json
import shutil
import random
import glob
import os



def find_same_imgjson():
    #找出文件名相同的img和json
    src_dir = "/911G/data/temp/20221229新加手托脚托新数据/20230311_最新修改/middle_up_nei/中指指尖修正后标注数据/middle_up_nei_20230609"
    dst_dir = "/911G/data/temp/20221229新加手托脚托新数据/20230311_最新修改/middle_up_nei/中指指尖修正后标注数据/new_data"
    count = 0
    for file in os.listdir(src_dir):
        if file.endswith(".jpg"):
            img_path = os.path.join(src_dir,file)
            json_path = img_path.replace(".jpg",".json")
            if os.path.exists(json_path):
                dst_img_path = os.path.join(dst_dir,file)
                dst_json_path = dst_img_path.replace(".jpg",".json")
                shutil.copy(img_path,dst_img_path)
                shutil.copy(json_path,dst_json_path)
                count+=1

    print("count: " , count)


def split_dataset():
    #分配数据集  train test
    src_dir = "/911G/data/temp/20221229新加手托脚托新数据/20230311_最新修改/middle_up_nei/修改手指后数据"
    dst_train = src_dir+"/train"
    dst_test = src_dir+"/test"
    imgs =[file for file in os.listdir(src_dir) if file.endswith(".jpg")] 
    random.shuffle(imgs)
    split_index = int(len(imgs)*0.8)

    os.makedirs(dst_train,exist_ok=True)
    os.makedirs(dst_test,exist_ok=True)

    for i, file in enumerate(imgs):
        src_img_path = os.path.join(src_dir,file)
        src_js_path = src_img_path.replace("jpg","json")
        if i < split_index:
            dst_img_path = os.path.join(dst_train,file)
            
        else:
            dst_img_path = os.path.join(dst_test,file)
        dst_js_path = dst_img_path.replace("jpg","json")
        shutil.move(src_img_path,dst_img_path)
        shutil.move(src_js_path,dst_js_path)    


def del_filename_end():
    #去除文件名的一部分后缀
    root_dir = "/home/zy/vision/ultralytics/yolo_crop/left_down_wai_right_foot"
    dst_dir = "/home/zy/vision/ultralytics/yolo_crop/left_down_wai_right_foot_split"
    os.makedirs(dst_dir,exist_ok = True)
    count = 0
    for file in os.listdir(root_dir):
        new_file = file.replace(".jpg_crop.jpg",".jpg")
        dst_path = os.path.join(dst_dir,new_file)
        src_path = os.path.join(root_dir,file)
        shutil.move(src_path,dst_path)
        count += 1
        print(count)
        

def get_kanames():
    a = [f'R-sanjiao-{i}' for i in range(8,25)]
    print(a)



import numpy as np
import cv2

def canny_edge_detection(image, sigma=1.0, low_threshold=30, high_threshold=90):
    # 第一步：图像灰度化
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # 第二步：使用高斯滤波平滑图像
    smoothed_image = cv2.GaussianBlur(gray_image, (5, 5), sigma)
    
    # 第三步：计算图像中各点像素的梯度幅值和方向
    gradient_x = cv2.Sobel(smoothed_image, cv2.CV_64F, 1, 0, ksize=3)
    gradient_y = cv2.Sobel(smoothed_image, cv2.CV_64F, 0, 1, ksize=3)
    gradient_magnitude = np.sqrt(gradient_x**2 + gradient_y**2)
    gradient_angle = np.arctan2(gradient_y, gradient_x)
    
    # 第四步：对梯度幅值进行非极大值抑制
    edge_magnitude = non_max_suppression(gradient_magnitude, gradient_angle)
    
    # 第五步：使用双阈值检测策略，将边缘点进行连接
    edge_image = hysteresis_threshold(edge_magnitude, low_threshold, high_threshold)
    
    return edge_image

def non_max_suppression(gradient_magnitude, gradient_angle):
    # 获取图像的高度和宽度
    height, width = gradient_magnitude.shape
    
    # 初始化结果图像为全零图像
    edge_magnitude = np.zeros_like(gradient_magnitude)
    
    # 将角度转换到0~180度范围内，方便后续处理
    gradient_angle = gradient_angle * 180 / np.pi
    gradient_angle[gradient_angle < 0] += 180
    
    # 对图像的每个像素点进行遍历
    for y in range(1, height - 1):
        for x in range(1, width - 1):
            # 获取当前像素点的梯度幅值和方向
            mag = gradient_magnitude[y, x]
            angle = gradient_angle[y, x]
            
            # 进行非极大值抑制
            edge_magnitude[y, x] = mag
            if angle >= 0 and angle < 22.5 or angle >= 157.5 and angle <= 180:
                if mag < gradient_magnitude[y, x+1] or mag < gradient_magnitude[y, x-1]:
                    edge_magnitude[y, x] = 0
            elif angle >= 22.5 and angle < 67.5:
                if mag < gradient_magnitude[y+1, x-1] or mag < gradient_magnitude[y-1, x+1]:
                    edge_magnitude[y, x] = 0
            elif angle >= 67.5 and angle < 112.5:
                if mag < gradient_magnitude[y+1, x] or mag < gradient_magnitude[y-1, x]:
                    edge_magnitude[y, x] = 0
            else:  # angle >= 112.5 and angle < 157.5
                if mag < gradient_magnitude[y-1, x-1] or mag < gradient_magnitude[y+1, x+1]:
                    edge_magnitude[y, x] = 0
    
    return edge_magnitude

def hysteresis_threshold(edge_magnitude, low_threshold, high_threshold):
    # 获取图像的高度和宽度
    height, width = edge_magnitude.shape
    
    # 初始化结果图像为全零图像
    edge_image = np.zeros_like(edge_magnitude)
    
    # 将边缘幅值分为强边缘和弱边缘两类
    strong_edges = (edge_magnitude >= high_threshold)
    weak_edges = (edge_magnitude >= low_threshold) & (edge_magnitude < high_threshold)
    
    # 对强边缘进行标记
    edge_image[strong_edges] = 255
    
    # 对弱边缘进行连接
    for y in range(1, height - 1):
        for x in range(1, width - 1):
            if weak_edges[y, x]:
                # 判断该像素周围8个像素是否有强边缘
                if np.any(strong_edges[y-1:y+2, x-1:x+2]):
                    edge_image[y, x] = 255
    
    return edge_image











if __name__ == "__main__":
    del_filename_end()

