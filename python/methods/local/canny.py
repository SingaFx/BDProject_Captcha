#coding=utf-8  

# canny detection演算法 先去除噪點再進行邊緣偵測

import cv2  
import numpy as np    
import os

folder = 'railway'
# 讀檔
pwd = os.path.split(os.path.realpath(__file__))[0]
for t in range(0,100):
    img = cv2.imread(os.path.join(pwd, 'img\\' + folder + '\\' + str(t) + '.bmp'))
    if img is not None:
        height, width = img.shape[:2]
        #去除噪點
        count = 0
        for i in range(width):
            for j in range(height):
                # if img[i,j][0] == 0 and img[i,j][1] == 0 and img[i,j][2] == 0:
                count = 0 
                for k in range(1, -2, -1):
                    for l in range(1, -2, -1):
                        try:
                            if i + k >= 0 and i + k < width and j + l >= 0 and j + l < height:
                                if img[i+k,j+l][0] == 255 and img[i+k,j+l][1] == 255 and img[i+k,j+l][2] == 255:
                                    count += 1
                        except TypeError:
                            pass
                        except IndexError:
                            pass
                if count >= 7:
                    img[i,j] = (255 , 255 , 255)   



        img = cv2.GaussianBlur(img,(3,3),0)  
        canny = cv2.Canny(img, 300, 150)  
        
        # cv2.imshow('Canny', canny)  
        cv2.imwrite(os.path.join(pwd, 'img\\' + folder + '\\' + str(t) + '_canny.bmp'), canny)
        cv2.waitKey(0)  
        cv2.destroyAllWindows()  
    else:
        print('找不到' + os.path.join(pwd, 'img\\' + folder + '\\' + str(t) + '.bmp'))