#coding=utf-8  
from PIL import Image, ImageTk, ImageEnhance
import numpy as np
import cv2
import os

folder = 'railway'

pwd = os.path.split(os.path.realpath(__file__))[0]
#處理驗證碼
def Captcha():
    #循環處理
    for t in range(0,100):
        path = os.path.join(pwd, 'img\\' + folder + '\\' + str(t))
        #讀圖檔
        im = cv2.imread(path + '.bmp', flags=cv2.IMREAD_GRAYSCALE)
        retval, im = cv2.threshold(im, 115, 255, cv2.THRESH_BINARY_INV)
        print('讀取' + path + '.bmp...')

        for i in range(len(im)):
            for j in range(len(im[i])):
                if im[i][j] == 255:
                    count = 0 
                    for k in range(-2, 3):
                        for l in range(-2, 3):
                            try:
                                if im[i + k][j + l] == 255:
                                    count += 1
                            except IndexError:
                                pass
                    # 這裡 threshold 設 4，當周遭小於 4 個點的話視為雜點
                    if count <= 4:
                        im[i][j] = 0

        im = cv2.dilate(im, (2, 2), iterations=1)
        cv2.imwrite(path + '_result.bmp', im)


if __name__ == "__main__":
    Captcha()