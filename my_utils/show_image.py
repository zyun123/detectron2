import cv2
import matplotlib.pyplot as plt




# #------------------------opencv-------
img1 = cv2.imread("/911G/data/new_all_jldata/20231226/middle_up_nei/test/m_up_nei_20231019150829170_0.jpg")
img2 = cv2.imread("/911G/data/new_all_jldata/20231226/middle_up_nei/test/m_up_nei_20231013140831877_0.jpg")
cv2.imshow("img1",img1)
cv2.imshow("img2",img2) 
cv2.waitKey(0)
cv2.destroyAllWindows()


#---------------------matplotlib----------------
# img1 = plt.imread("/911G/data/cure_images/dynamic_identfy/middle_up_nei_20230512105416017.jpg")
# img2 = plt.imread("/911G/data/cure_images/dynamic_identfy/middle_up_nei_20230512165407232.jpg")
# fig,axs = plt.subplots(2,1)
# axs[0].imshow(img1)
# axs[0].set_title("img1")    

# axs[1].imshow(img2)
# axs[1].set_title("img2")


# plt.tight_layout()
# plt.show()
# print("done...")


import glob 
import os

# root_dir = "/911G/data/cure_images/dynamic_up_nei/ori_img_01"
# dst_dir1 = "/911G/data/cure_images/dynamic_up_nei/ori_img_01/10cm"
# dst_dir2 = "/911G/data/cure_images/dynamic_up_nei/ori_img_01/20cm"
# dst_dir3 = "/911G/data/cure_images/dynamic_up_nei/ori_img_01/30cm"
# for file in os.listdir(root_dir):
#     if file.startswith("middle"):
#         img = cv2.imread(os.path.join(root_dir,file))
#         cv2.imshow("img",img)
#         key = cv2.waitKey(0)
#         if key == ord("a"):
#             cv2.imwrite(os.path.join(dst_dir1,file),img)
#         if key == ord("s"):
#             cv2.imwrite(os.path.join(dst_dir2,file),img)
#         if key == ord("d"):
#             cv2.imwrite(os.path.join(dst_dir3,file),img)
#         if key == 27:
#             break
# cv2.destroyAllWindows()




