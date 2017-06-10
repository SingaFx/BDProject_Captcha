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

    def captcha(self, rand):
        im = self.converter.cv_url_to_image('http://140.138.152.207/house/BDProject/upload/' + rand + '/src.png')
        if im is not None:
            #Convert image file to gray map
            #OpenCv Get Image Channels
            channels = len(im.shape)
            if channels == 3:
                #Give image width to width and image height to height 
                width, height = im.shape[:2]
                #print('Size width : ' + str(width))
                #print('Size height : ' + str(height))
                img = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
                #print('The file has been converted to gray map successfully')
            else:
                print('The image file is not a RGB file.')

            # 去外框
            for i in range(len(img)):
                for j in range(len(img[i])):
                    if i == 0 or i == len(img) - 1 or j == 0 or j == len(img[i]) -1:
                        img[i,j] = 255

            #暫存閥值
            ucThre = 0
            #初始閥值
            ucThre_new = 127
            #print('Initial Threshold is:' + str(ucThre_new))
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
            #print('After Binarization threshold is :' + str(ucThre_new))

            nBlack = 0
            nWhite = 0
            for i in range(len(img)):
                for j in range(len(img[i])):
                    nValue = img[i,j]
                    if nValue > ucThre_new:
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
                            img[i,j] = 0
                        else:
                            img[i,j] = 255
            img = self.denoise(img)
            cv2.imwrite('img/' + rand + '/3_test.png', img)
            r = requests.post('http://140.138.152.207/house/BDProject/receiver.php', files={'3_test': open('img/' + rand + '/3_test.png', 'rb')}, data={'path':rand})
            print (r.text)
            return rand + '/3_test.png'

    def denoise(self, cvimg):
        count = 0
        width = len(cvimg)
        for i in range(width):
            height = len(cvimg[i])
            for j in range(height):
                count = 0 
                for k in range(1, -2, -1):
                    for l in range(1, -2, -1):
                        try:
                            if i + k >= 0 and i + k < width and j + l >= 0 and j + l < height:
                                if cvimg[i+k,j+l] == 255:
                                    count += 1
                        except TypeError:
                            pass
                if count >= 7:
                    cvimg[i,j] = 255
        return cvimg

if __name__ == '__main__':
    benny = benny_captcha()
    benny.captcha('20170610153454_9241')