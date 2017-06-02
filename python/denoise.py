#coding=utf-8  

# 去噪點演算法 測試用 不大好用

import numpy as np
import cv2
import os
from matplotlib import pyplot as plt

folder = 'OB'
pwd = os.path.split(os.path.realpath(__file__))[0]

img = cv2.imread(os.path.join(pwd, 'img\\' + folder + '\\' + '0' + '.bmp'))
print(img.dtype)
dst = cv2.fastNlMeansDenoisingColored(img,None,10,10,7,21)

plt.subplot(121),plt.imshow(img)
plt.subplot(122),plt.imshow(dst)
plt.show()