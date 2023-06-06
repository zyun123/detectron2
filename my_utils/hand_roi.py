import cv2
import numpy as np
import glob
import os
from demo.predictor import VisualizationDemo




# cfg = setup_cfg(args,kp_use_mean_std,kp_names_key)
# demo = VisualizationDemo(cfg,parallel = False)

root_dir = "/911G/data/cure_images/一楼拷贝数据/up_nei"
save_dir = "/911G/data/cure_images/一楼拷贝数据/up_nei_crop"
os.makedirs(save_dir,exist_ok = True)
roi_lt = [470,120]
roi_rb = [roi_lt[0]+200,roi_lt[1]+200]
roi_arr = np.array([roi_lt,roi_rb])
for file in os.listdir(root_dir):
    if file.startswith("m"):
        file_path = os.path.join(root_dir,file)
        img = cv2.imread(file_path)
        # cv2.rectangle(img,roi_lt,roi_rb,(255,0,255),1,8)
        # cv2.putText(img,"roi",roi_lt,cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,255),2,8)
        # cv2.imshow("img",img)
        roi_img = img[roi_lt[1]:roi_rb[1],roi_lt[0]:roi_rb[0],:]
        cv2.imshow("roi_img",roi_img)
        cv2.imwrite(os.path.join(save_dir,file),roi_img)
        key = cv2.waitKey(1)
        if key ==27 or key == ord("q"):   #esc or q
            break

cv2.destroyAllWindows()
