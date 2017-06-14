#coding=utf-8  
# 目前的主要演算法

import sys
import os
import requests
import numpy as np
import cv2
from PIL import Image, ImageEnhance


sys.path.append('../../')
from util.convertImage import convertImage

class main_captcha:
    def __init__(self):
        self.converter = convertImage()
        self.threshold = 3
    def run(self, rand):
        img = self.converter.url_to_image('http://140.138.152.207/house/BDProject/upload/' + rand + '/src.png')
        # Convert to RGB mode
        if img.mode != "RGB":
            img = img.convert("RGB")

        # 影像加強
        enhancer = ImageEnhance.Contrast(img)
        img = enhancer.enhance(5.0)
        enhancer = ImageEnhance.Brightness(img)
        img = enhancer.enhance(10.0)
        pixdata = img.load()

        if not os.path.exists('img'):
            os.makedirs('img')

        if not os.path.exists('img/' + rand):
            os.makedirs('img/' + rand)
            
        img.save('img/' + rand + '/1_bright.png')
        r = requests.post('http://140.138.152.207/house/BDProject/receiver.php', files={'1_bright': open('img/' + rand + '/1_bright.png', 'rb')}, data={'path':rand})
        print (r.text)
        # for y in range(img.size[1]): 
            # for x in range(img.size[0]): 
                # if pixdata[x, y][0] < 10: 
                    # pixdata[x, y] = (0, 0, 0, 255) 
        # for y in range(img.size[1]): 
            # for x in range(img.size[0]): 
                # if pixdata[x, y][1] < 50: 
                    # pixdata[x, y] = (0, 0, 0, 255) 
        # for y in range(img.size[1]): 
            # for x in range(img.size[0]): 
                # if pixdata[x, y][2] > 0:
                    # pixdata[x, y] = (255, 255, 255, 255)
                    

        # for x in range(img.width):
        #     for y in range(img.height):
        #         if pixdata[x , y][1] != 255 and pixdata[x , y][2] == 255:
        #             pixdata[x , y] = (0 , 0 , 0 , 255)
        #         else:
        #             pixdata[x , y] = (255 , 255 , 255 , 255)

        # 去外框
        for i in range(img.width):
            for j in range(img.height):
                if i == 0 or i == img.width - 1 or j == 0 or j == img.height -1:
                    pixdata[i,j] = (255 , 255 , 255)


        # 8鄰域降噪
        count = 0
        for i in range(img.width):
            for j in range(img.height):
                # if pixdata[i,j][0] == 0 and pixdata[i,j][1] == 0 and pixdata[i,j][2] == 0:
                count = 0 
                for k in range(1, -2, -1):
                    for l in range(1, -2, -1):
                        try:
                            if i + k >= 0 and i + k < img.width and j + l >= 0 and j + l < img.height:
                                if pixdata[i+k,j+l][0] == 255 and pixdata[i+k,j+l][1] == 255 and pixdata[i+k,j+l][2] == 255:
                                    count += 1
                        except TypeError:
                            pixdata[i,j] = (255 , 255 , 255)
                            pass
                if count >= 7:
                    pixdata[i,j] = (255 , 255 , 255)    
        
        

        img.save('img/' + rand + '/1_black.png')
        r = requests.post('http://140.138.152.207/house/BDProject/receiver.php', files={'1_black': open('img/' + rand + '/1_black.png', 'rb')}, data={'path':rand})
        print (r.text)

        # 平滑補強
        # im = cv2.imread('img/' + rand + '/1_black.png' , 0)
        # # im = self.converter.convertPILToCV(img)
        # im = self.NoiseReduce_Burst(im, self.threshold)
        # kernel = np.ones((2 , 2) , np.uint8)
        # opening = cv2.morphologyEx(im, cv2.MORPH_OPEN, kernel)

        # opening = cv2.dilate(im, (1, 1), iterations=1)
        # opening = cv2.blur(im, (2, 2))
        # cv2.imwrite('img/' + rand + '/1_black2.png', opening)
        return rand + '/1_black.png'

if __name__ == "__main__":
    main = main_captcha()
    main.captcha('20170614063115_19753')