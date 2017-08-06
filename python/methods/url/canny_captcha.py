#coding=utf-8  
import sys
import cv2
import os
import requests
sys.path.append('../../')
from util.convertImage import convertImage
from util.GetConfig import GetConfig

class canny_captcha:
    def __init__(self):
        self.converter = convertImage()
        self.config = GetConfig()
        self.threshold = 3

    def run(self, url, rand):
        img = self.converter.cv_url_to_image(url)
        if img is not None:
            height, width = img.shape[:2]

            # # 去外框
            # for i in range(len(img)):
            #     for j in range(len(img[i])):
            #         if i == 0 or i == len(img) - 1 or j == 0 or j == len(img[i]) -1:
            #             img[i,j] = 255

            # 8鄰域降噪
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

            # img = self.NoiseReduce_Burst(img, self.threshold)

            img = cv2.GaussianBlur(img,(3,3),0)  
            canny = cv2.Canny(img, 300, 150)  
            if not os.path.exists('img'):
                os.makedirs('img')

            if not os.path.exists('img/' + rand):
                os.makedirs('img/' + rand)        
            # cv2.imshow('Canny', canny)  
            cv2.imwrite('img/' + rand + '/2_canny.png', canny)
            r = requests.post(self.config.Web_host + 'receiver.php', files={'2_canny': open('img/' + rand + '/2_canny.png', 'rb')}, data={'path':rand})
            print (r.text)
            # cv2.waitKey(0)  
            # cv2.destroyAllWindows()
            return rand + '/2_canny.png'
        return ''

if __name__ == "__main__":
    canny = canny_captcha()
    canny.cannyDetection('20170614063115_19753')