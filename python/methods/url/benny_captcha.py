#coding=utf-8  
import numpy as np
import cv2
import os
import copy
import sys
import requests
sys.path.append('../../')
from util.convertImage import convertImage

class benny_captcha:
    def __init__(self):
        self.converter = convertImage()
        self.threshold = 3

    def run(self, url, rand):
        im = self.converter.cv_url_to_image(url)
        if im is not None:
            im = self.Binarization(im)
            im = self.NoiseReduce_eight(im, self.threshold)
            im = self.NoiseReduce_Burst(im, self.threshold)

            
            cv2.imwrite('img/' + rand + '/3_test.png', im)
            r = requests.post('http://140.138.152.207/house/BDProject/receiver.php', files={'3_test': open('img/' + rand + '/3_test.png', 'rb')}, data={'path':rand})
            print (r.text)
            return rand + '/3_test.png'
        return ''

    def Binarization(self, im):
        #Convert image file to gray map
        #OpenCv Get Image Channels
        #灰度化 ---> 加權變化 g[i,j] = 0.3*r[i,j] + 0.59*g[i,j] + 0.11*b[i,j] ----> 利用opencv內建cvtColor
        channels = len(im.shape)
        if channels == 3:
            #Give image width to width and image height to height 
            width, height = im.shape[:2]
            img = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
        else:
            print('The image file is not a RGB file.')
        #二值化 ----> 去除圖片上沒用的信息 ----> 採用自適應閥值
        #決定自適應閥值方法說明(採用K均值方法):
        #先取中間值當作閥值，計算[(大於中間閥值所有像素平均值) + (小於中間閥值所有像素平均值)]/2
        #暫存閥值
        ucThre = 0
        #自適應閥值
        ucThre_new = 127
        #尋找自適應閥值
        while(ucThre != ucThre_new):
            nBack_sum = nData_sum = 0
            nBack_count = nData_count = 0
            for i in range(len(img)):
                for j in range(len(img[i])):
                    nValue = img[i,j]
                    if nValue > ucThre_new:
                        nBack_sum += nValue
                        nBack_count += 1
                    else:
                        nData_sum += nValue
                        nData_count += 1
            nBack_sum = nBack_sum/nBack_count
            nData_sum = nData_sum/nData_count
            ucThre = ucThre_new
            ucThre_new = int((nBack_sum + nData_sum)/2)
        threshold = ucThre_new
        
        nWidth, nHeight = img.shape[:2]
        nBlack = 0
        nWhite = 0
        for i in range(len(img)):
            for j in range(len(img[i])):
                nValue = img[i,j]
                if nValue > threshold:
                    img[i,j] = 255
                    nWhite += 1
                else:
                    img[i,j] = 0
                    nBlack += 1
        #Background is black, swap black and white
        if nBlack > nWhite:
            for i in range(len(img)):
                for j in range(len(img[i])):
                    nValue = img[i,j]
                    if not nValue:
                        img[i,j] = 255
                    else:
                        img[i,j] = 0
        
        return img

    #8鄰域降噪
    def NoiseReduce_eight(self, img, threshold):
        #8鄰域降噪
        h, w = img.shape[:2]
        for i in range(w):
            img[0,i] = 255
            img[h-1,i] = 255
        for i in range(h):
            img[i,0] = 255
            img[i,w-1] = 255
        #if the neightbor of a point is white but it is black, delete it
        for i in range(len(img)):
            for j in range(len(img[i])):
                nValue = img[i,j]
                if not nValue:
                    nCount = 0
                    #以img[i,j]為中心點，計算其鄰近的8個pixel
                    for m in range(i-1, i+2):
                        for n in range(j-1, j+2):
                            if not img[m,n]:
                                nCount += 1
                    if nCount <= threshold:
                        img[i,j] = 255
                else:
                    nCount = 0
                    #以img[i,j]為中心點，計算其鄰近的8個pixel
                    for m in range(i-1, i+1):
                        for n in range(j-1, j+1):
                            if not img[m,n]:
                                nCount += 1
                    if nCount >= 7:
                        img[i,j] = 0
        #img.show()
        return img

    #連通域降噪
    def NoiseReduce_Burst(self, image, threshold):
        #floodFill
        img_height, img_width = image.shape[:2]
        color = 1
        mask = np.zeros((img_height + 2, img_width + 2), np.uint8)
        for i in range(img_width):
            for j in range(img_height):
                if not image[j,i]:
                    #Mask初始全為0
                    mask[:] = 0
                    flooded = image.copy()
                    cv2.floodFill(image, mask, (i,j), color)
                    color += 1
                    im_floodfill_inv = cv2.bitwise_not(flooded)
        #Create an array which size is 256
        ColorCount = [0]*256
        for i in range(img_width):
            for j in range(img_height):
                if image[j,i] != 255:
                    ColorCount[image[j,i]] += 1
        pArea = float(threshold)
        #Get rid of noise point
        for i in range(len(image)):
            for j in range(len(image[i])):
                if ColorCount[image[i,j]] <= pArea:
                    image[i,j] = 255
        for i in range(img_width):
            for j in range(img_height):
                if image[j,i] < 255:
                    image[j,i] = 0
        return image

if __name__ == '__main__':
    benny = benny_captcha()
    benny.captcha('20170610153454_9241')