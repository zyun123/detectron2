"""
numpy矩阵乘法
"""


import time
import numpy as np

"""



#a[3,4]  b[4,1]   a*b --> [3,1]
a = np.arange(12).reshape(3,4)
print(a)
b = np.array([1,2,3,4]).reshape(4,1)
res1 = np.dot(a,b)
print(res1)


#  b:[4,1] --> [4,3] 广播
c = np.tile(b,3)
print(c)
#a[3,4]    c*a--> [4,3]
res2 = np.dot(c,a)
print(res2)


res2_pad = np.expand_dims(res2,axis = 0)

# print(res2_pad.shape)
# 

res2_pad2 = np.zeros_like(res2_pad)
res2_pad3 = np.zeros_like(res2_pad)

# res_stack = np.stack([res2,res2_pad2,res2_pad3],axis = 0)
res_cat = np.concatenate([res2_pad,res2_pad2,res2_pad3],axis = 0)

print(res_cat.shape)
t1 = time.time()
trans_res = np.ascontiguousarray(res_cat.transpose(1,2,0))
print(time.time() - t1)
print(trans_res.shape)

# a = np.array([1,2,3,4]).reshape(4,1)
# b = np.zeros((4,3))
# c = a + b
# print(c)

print(trans_res[0,0])

# res_cat.permute(1,2,0).contigious()



"""



###################svd 奇异值分解##################333

#A = np.array([[1,2,3], [4,5,6],[7,8,9]])
#U,S,Vt = np.linalg.svd(A)
#print("A: \n",A)
#print("U: \n",U)
#print("Vt: \n",Vt)
#print("sigma: \n",np.diag(S))

import numpy as np

# 创建一个超定矩阵 A 和一个列向量 B
A = np.array([[1, 2],
              [3, 4],
              [5, 6]])

B = np.array([7, 8, 9])

# 使用 SVD 分解 A
U, S, Vt = np.linalg.svd(A)

print("svd mul: \n",np.dot(U,np.dot(S,Vt)))


# 计算最小二乘解
x_lstsq = np.linalg.lstsq(A, B, rcond=None)[0]

# 使用 SVD 的伪逆计算最小二乘解
s_pseudo_inv = np.diag(1/S)
a_pseudo_inv  = Vt.T @ s_pseudo_inv.T @ U.T
x_svd = a_pseudo_inv @ B

# 打印结果
print("SVD Solution:", x_svd)
print("numpy.linalg.lstsq Solution:", x_lstsq)



