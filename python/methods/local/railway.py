#coding=utf-8  
# 針對台鐵驗證碼的演算法

from PIL import Image, ImageTk, ImageEnhance
import numpy as np
import cv2
import os

folder = '9x9'

pwd = os.path.split(os.path.realpath(__file__))[0]
#處理驗證碼
def Captcha():
    #循環處理
    for t in range(0,100):
        path = os.path.join(pwd, '..\..\img\\' + folder + '\\' + str(t))
        print(path)
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
        cv2.imwrite(path + '_result.png', im)
        _, contours, _ = cv2.findContours(im.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        cnts = sorted([(c, cv2.boundingRect(c)[0]) for c in contours], key=lambda x:x[1])

        arr = []

        for index, (c, _) in enumerate(cnts):
            (x, y, w, h) = cv2.boundingRect(c)

            try:
                # 只將寬高大於 8 視為數字留存
                if w > 8 and h > 8:
                    add = True
                    for i in range(0, len(arr)):
                        # 這邊是要防止如 0、9 等，可能會偵測出兩個點，當兩點過於接近需忽略
                        if abs(cnts[index][1] - arr[i][0]) <= 3:
                            add = False
                            break
                    if add:
                        arr.append((x, y, w, h))
            except IndexError:
                pass

        for index, (x, y, w, h) in enumerate(arr):
            roi = im[y: y + h, x: x + w]
            thresh = roi.copy() 
            
            angle = 0
            smallest = 999
            row, col = thresh.shape

            for ang in range(-60, 61):
                M = cv2.getRotationMatrix2D((col / 2, row / 2), ang, 1)
                t = cv2.warpAffine(thresh.copy(), M, (col, row))

                r, c = t.shape
                right = 0
                left = 999

                for i in range(r):
                    for j in range(c):
                        if t[i][j] == 255 and left > j:
                            left = j
                        if t[i][j] == 255 and right < j:
                            right = j

                if abs(right - left) <= smallest:
                    smallest = abs(right - left)
                    angle = ang

            M = cv2.getRotationMatrix2D((col / 2, row / 2), angle, 1)
            thresh = cv2.warpAffine(thresh, M, (col, row))
            # resize 成相同大小以利後續辨識
            thresh = cv2.resize(thresh, (50, 50))

            cv2.imwrite(path + '_' + str(index) + '.png', thresh)

if __name__ == "__main__":
    Captcha()