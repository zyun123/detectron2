import numpy as np
import cv2
import torch
from scipy.signal import convolve2d
import torch.functional as F
# ######################################
a = np.array([[1,2,1],
              [2,1,2],
              [2,1,1]]) 

w = np.array([[1,1],
              [1,2]])

out1 = convolve2d(a,w,mode = 'valid')   
print(out1)


#############################################################
import cv2
import numpy as np
import torch
import torch.nn.functional as F

# 输入图像和卷积核
input_image = np.array([[1, 2, 3],
                        [4, 5, 6],
                        [7, 8, 9]])

kernel = np.array([[0, 1, 0],
                   [1, -4, 1],
                   [0, 1, 0]])

# 使用OpenCV进行卷积
# opencv_result = cv2.filter2D(input_image, -1, kernel)

# 使用NumPy进行卷积
numpy_result = np.convolve(input_image.flatten(), kernel.flatten(), mode='same')
numpy_result = numpy_result.reshape(input_image.shape)

# 使用PyTorch进行卷积
input_tensor = torch.tensor(input_image, dtype=torch.float32).unsqueeze(0).unsqueeze(0)
kernel_tensor = torch.tensor(kernel, dtype=torch.float32).unsqueeze(0).unsqueeze(0)
pytorch_result = F.conv2d(input_tensor, kernel_tensor, padding=1)

# 打印结果
# print("OpenCV Result:")
# print(opencv_result)

print("NumPy Result:")
print(numpy_result)

print("PyTorch Result:")
print(pytorch_result.squeeze().numpy())
