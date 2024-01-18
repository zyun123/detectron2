import glob
import os
import json
import cv2
import numpy as np
import random
left_hand_dir = "/911G/data/temp/20221229新加手托脚托新数据/20230311_最新修改/middle_up_nei/修改手指后数据/middle_up_nei/test_crop/right_hand"
robot_path = "/911G/data/cure_images/二次识别机械臂图像/Up_Robot.png"

rb_img = cv2.imread(robot_path,cv2.IMREAD_UNCHANGED)
print(rb_img.shape)
# cv2.imshow("b",rb_img[...,0])
# cv2.imshow("g",rb_img[...,1])
# cv2.imshow("r",rb_img[...,2])
# cv2.imshow("bgr",rb_img[...,:3])
# cv2.imshow("a",rb_img[...,3])


cv2.imshow("rb_img",rb_img)

new_rb_img  = cv2.resize(rb_img,(256,256),interpolation = cv2.INTER_LINEAR)
cv2.imshow("new_rb img",new_rb_img)

mask = new_rb_img[...,3]    
robot_color = new_rb_img[...,:3]


robot_color[mask==0] = 0
# cv2.imshow("mask2img",robot_color)

# cv2.waitKey(0)


img_pathes = glob.glob(os.path.join(left_hand_dir,"*.jpg"))
random.shuffle(img_pathes)
split_index = int(len(img_pathes)* 0.5)



for img_path in img_pathes[:split_index]:
    img = cv2.imread(img_path)
    img = cv2.resize(img,(256,256),interpolation = cv2.INTER_LINEAR)
    cv2.imshow("img",img) 
    img[mask > 0] =0
    new_img = img + robot_color
    cv2.imshow("mask2img",new_img)
    # cv2.imwrite(img_path,new_img)
    key = cv2.waitKey(0)
    if key == 27 or key == ord("q"):
        break

cv2.destroyAllWindows()