from PIL import Image
import matplotlib.pyplot as plt
import numpy as np
import cv2


img = Image.open(r'S:\code\python\educateWork\images\000001.jpg').convert('RGB')
img = np.uint8(img)

imgr = img[:,:,0]
imgg = img[:,:,1]
imgb = img[:,:,2]

claher = cv2.createCLAHE(clipLimit=5, tileGridSize=(8,8))  # 创建CLAHE算法对象
claheg = cv2.createCLAHE(clipLimit=5, tileGridSize=(8,8))
claheb = cv2.createCLAHE(clipLimit=5, tileGridSize=(8,8))
cllr = claher.apply(imgr)  # 对图像进行CLAHE处理
cllg = claheg.apply(imgg)
cllb = claheb.apply(imgb)

rgb_img = np.dstack((cllr,cllg,cllb))

plt.subplot(1,2,1),plt.imshow(img)
plt.title('Input Image'),plt.axis('off')
plt.subplot(1,2,2),plt.imshow(rgb_img)
plt.title('CLAHE Image'),plt.axis('off')
plt.show()

# 显示原始图像和CLAHE处理后的图像
cv2.imshow('Input Image', img)
cv2.imshow('CLAHE Image', rgb_img)
cv2.waitKey(0)
cv2.destroyAllWindows()