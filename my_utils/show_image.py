import cv2


img_path = "/911G/data/temp/20221229新加手托脚托新数据/20230311_最新修改/middle_up_nei/test/m_up_nei_20221228151547322.jpg"
img = cv2.imread(img_path)
cv2.imshow("img",img)
cv2.waitKey(0)
cv2.destroyAllWindows()

