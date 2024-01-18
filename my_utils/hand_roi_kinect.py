import cv2
import numpy as np
import glob
import os
# from demo.predictor import VisualizationDemo
import json


def get_new_json(root_dir,jsfile,dst_dir,roi_lt,roi_rb):
    jspath = os.path.join(root_dir,jsfile)
    with open(jspath,"r") as f:
        data = json.load(f)
    new_shapes = []
    for shape in data['shapes']:
        if shape['label'] == "person":
            shape['points'] = [[1,1],[roi_rb[0]-roi_lt[0]-1,roi_rb[1]-roi_lt[1]-1]]
            new_shapes.append(shape)
        else:
            point = shape['points'][0]
            if point[0] > roi_lt[0] and point[0] < roi_rb[0] and point[1] > roi_lt[1] and point[1] < roi_rb[1]:
                shape['points'] = [[point[0] - roi_lt[0],point[1]-roi_lt[1]]]
                new_shapes.append(shape)
            
    data['imageHeight'] = roi_rb[1] - roi_lt[1]
    data['imageWidth'] = roi_rb[0] - roi_lt[0]
    data['shapes'] = new_shapes
    data['imageData'] = None
    new_jspath = os.path.join(dst_dir,jsfile)    
    with open(new_jspath, 'w') as f:
        json.dump(data,f,indent = 4)



# cfg = setup_cfg(args,kp_use_mean_std,kp_names_key)
# demo = VisualizationDemo(cfg,parallel = False)
root_dir = "/911G/data/new_all_jldata/20231226/middle_up_nei/test"

save_dir = "/911G/data/new_all_jldata/20231226/middle_up_nei/test_crop/right_hand"
os.makedirs(save_dir,exist_ok = True)

# roi_lt = [470,120]    #middle_up_nei  right_hand    200
# roi_lt = [470,410]   #middle_up_nei  left_hand    200

# roi_lt = [470,410]    #middle_down_wai  right_hand   200
# roi_lt = [470,120]   #middle_down_wai  left_hand     200

# roi_lt = [60,180]   #left_down_wai foot    320
# roi_lt = [725,185]   #left_down_wai head   320
# roi_lt = [50,200]   #left_up_nei foot    320

# roi_lt = [760,240]   #middle_up_nei  face   256
# roi_lt = [790,200]   #middle_up_nei  face   256  kinect 0位置  每移动500 roi框x +- 21pix
  
# roi_lt = [380,240]      #head_down_wai  head  320
# roi_lt = [410,200]      #head_down_wai  head  320
# roi_lt = [520,180]      #head_down_wai  head  320  h,w(416,416)
# roi_lt = [520,180]      #head_down_wai  head  320  h,w(416,416)

  
# roi_rb = [roi_lt[0]+200,roi_lt[1]+200]   #apply middle_up_nei hand

# roi_rb = [roi_lt[0]+200,roi_lt[1]+200]   #apply middle_up_nei hand
# roi_rb = [roi_lt[0]+300,roi_lt[1]+300]   #apply middle_up_nei hand


 
for file in os.listdir(root_dir):
    # if file.startswith("l_up_nei"):  #apply middle_up_nei hand
    if file.endswith(".jpg"):  #apply middle_up_nei hand
    # if file.endswith(".jpg") and file.startswith("left_up_nei"):  #apply middle_up_nei hand
        file_path = os.path.join(root_dir,file)
        img = cv2.imread(file_path)
        # roi_lt = [790,200]   #middle_up_nei  face   256  kinect 0位置  每移动500 roi框x +- 21pix
        # roi_lt = [470,360]    #middle_up_nei  left_hand    200
        # roi_lt = [470,77]    #middle_up_nei  right_hand    200
        roi_lt = [470,77]    #middle_down_wai  left_hand    200
        # roi_lt = [470,360]    #middle_down_wai  right_hand    200
        wh = 200 #矩形框边长
        bed_move_dist = round(int(file.split("_")[-1][:-4]) / 500) * 21     #转换成移动了多少像素值
        print(f"{file} move dist: {bed_move_dist}")
        print("roi_lt: " , roi_lt)
        roi_lt = (roi_lt[0] - bed_move_dist,roi_lt[1])
        print("roi_lt: " , roi_lt)
        roi_rb = (roi_lt[0] + wh , roi_lt[1] + wh)
        # cv2.rectangle(img,roi_lt,roi_rb,(255,0,255),1,8)
        # cv2.putText(img,"roi",roi_lt,cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,255),2,8)
        # cv2.imshow("img",img)


        roi_img = img[roi_lt[1]:roi_rb[1],roi_lt[0]:roi_rb[0],:]
        cv2.imshow("roi_img",roi_img)
        cv2.imwrite(os.path.join(save_dir,file),roi_img)

        jsfile = file.replace("jpg","json")
        get_new_json(root_dir,jsfile,save_dir,roi_lt,roi_rb)
        key = cv2.waitKey(1)
        if key ==27 or key == ord("q"):   #esc or q
            break

cv2.destroyAllWindows()
