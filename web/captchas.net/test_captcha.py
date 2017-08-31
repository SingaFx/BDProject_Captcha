#My Simple Algorithm
#PIL is the package for processing image
from PIL import Image, ImageTk, ImageEnhance
import numpy as np
import cv2
import cv2 as cv
import os
import copy
import sys

threshold = 4
folder = './freebitcoin/'
#灰度化與二值化
def Binarization(im):
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
def NoiseReduce_eight(img, threshold):
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
def NoiseReduce_Burst(image, threshold=30):
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

#文字切割
def Image_Cut(im, num):
    # im = cv2.dilate(im, (2, 2), iterations=1)
    #cv2.imwrite(path + '_result.png', im)
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

        # M = cv2.getRotationMatrix2D((col / 2, row / 2), angle, 1)
        # thresh = cv2.warpAffine(thresh, M, (col, row))
        # # resize 成相同大小以利後續辨識
        # thresh = cv2.resize(thresh, (50, 50))

        cv2.imwrite('..\\..\\img\\'+folder+'\\' + str(num) + '_' + str(index) + '.png', thresh)

def main():
    all_image = os.listdir(folder)
        
    for i in range(len(all_image)):
        print(str(i) + '  ' + all_image[i])
        im = cv2.imread(folder + all_image[i])
        img = Binarization(im)
        img = NoiseReduce_eight(img, threshold)
        img = NoiseReduce_Burst(img)
        cv2.imwrite(folder + all_image[i], img)


if __name__ == "__main__":
    main()
        # Image_Cut(img, i)
        #im_pil = Image.fromarray(img)
        #im_pil.save('img\\OB_my_test\\' + str(i) + '.bmp')
        # 丟進OCR偵測
        #text = ocr(im_pil) 
        #result = text.ocr_text()
        #print(result)
        #將結果存在txt檔
        #with open('result.txt', 'a') as out:
        #        out.write(result + '\n')