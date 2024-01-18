


"""
#运动模糊
import cv2
import numpy as np
# 读取图像
image = cv2.imread('/911G/data/new_all_jldata/床体移动采集图像/down_wai/h/0cm_crop/h_down_wai_20231010141644453_-0.4.jpg')

# 创建一个15x15的运动核
kernel_size = 15
angle = 45  # 运动模糊的方向（以度为单位）

# 生成运动核
motion_kernel = np.zeros((kernel_size, kernel_size))
center = kernel_size // 2

# 计算运动核的方向
angle_rad = np.deg2rad(angle)
cosine = np.cos(angle_rad)
sine = np.sin(angle_rad)

# 设置运动核的中心线
for i in range(kernel_size):
    motion_kernel[i, int(center + sine * (i - center))] = 1

# 归一化运动核
motion_kernel /= kernel_size

# 应用运动模糊
motion_blur = cv2.filter2D(image, -1, motion_kernel)

# 保存运动模糊后的图像
# cv2.imwrite('motion_blur.jpg', motion_blur)
cv2.imshow("motion_blur",motion_blur)
cv2.waitKey(0)
cv2.destroyAllWindows()


"""

#高斯模糊
import cv2
import numpy as np

# 读取图像
image = cv2.imread('/911G/data/new_all_jldata/床体移动采集图像/down_wai/h/0cm_crop/h_down_wai_20231010141644453_-0.4.jpg')

# 指定高斯核的大小（奇数）
kernel_size = (15, 15)

# 指定高斯核的标准差
sigma = 0

# 应用高斯模糊
gaussian_blur = cv2.GaussianBlur(image, kernel_size, sigma)

# 保存高斯模糊后的图像
# cv2.imwrite('gaussian_blur.jpg', gaussian_blur)

cv2.imshow("gaussian_blur",gaussian_blur)
cv2.waitKey(0)
cv2.destroyAllWindows()
