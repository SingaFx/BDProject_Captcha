#coding=utf-8  
# 目前的主要演算法

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
        img = Image.open(path + '.bmp', 'r')
        print('讀取' + path + '.bmp' + '...')

        #去除噪點 干擾線
        # enhancer = ImageEnhance.Contrast(img)
        # img = enhancer.enhance(5.0)
        # enhancer = ImageEnhance.Brightness(img)
        # img = enhancer.enhance(10.0)
        pixdata = img.load()
        img.save(path + '_bright.bmp')


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
                    
        
        #二值化

        # for x in range(img.width):
        #     for y in range(img.height):
        #         if pixdata[x , y][1] != 255 and pixdata[x , y][2] == 255:
        #             pixdata[x , y] = (0 , 0 , 0 , 255)
        #         else:
        #             pixdata[x , y] = (255 , 255 , 255 , 255)


        #去除噪點
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
                            pass
                if count >= 7:
                    pixdata[i,j] = (255 , 255 , 255 , 255)    
         
        #存檔
        img.save(path + '_black.bmp')

        im = cv2.imread(path + '_black.bmp' , 0)

        #平滑化
        kernel = np.ones((2 , 2) , np.uint8)
        opening = cv2.morphologyEx(im, cv2.MORPH_OPEN, kernel)

        #opening = cv2.blur(opening , (2, 2))
        #opening = cv2.dilate(opening, (1, 1), iterations=1)
        cv2.imwrite(path +'_black2.bmp', opening)

if __name__ == "__main__":
    Captcha()