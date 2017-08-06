#coding=utf-8  

# 分割recaptcha的圖片九宮格
from PIL import Image
import os
import sys
import json
import fnmatch
sys.path.append('../../')
from util.convertImage import convertImage
sys.path.append('../')
from api.clarifai_api import clarifai_api
from api.googleVision import googleVision

class recaptcha:
    def __init__(self):
        self.vision = googleVision()
        self.clarifai = clarifai_api()
        self.converter = convertImage()

    def clarifai_process(self, uri, keyword):
        # 從網路上得到圖片
        img = self.converter.url_to_image(uri)
        path = '../img/recaptcha/' + keyword + '/'
        if not os.path.exists(path):
            os.makedirs(path)
        # 依序存檔
        fileNum = len(fnmatch.filter(os.listdir(path), '*.jpg'))
        img.save(path + str(fileNum + 1) + '.jpg')
        # 驗證碼切塊
        pathArr = self.cropCaptcha(path, str(fileNum + 1))
        resultArr = []
        for index, blockPath in enumerate(pathArr):
            labels = self.clarifai.predict_local(blockPath, blockPath.replace('.jpg', '_ClarifaiLabels.txt'))
            if self.isContain(labels, keyword):
                resultArr.append(index+1)

        f = open(path + str(fileNum + 1) + '_clarifai.txt','w')
        for result in resultArr:
            f.write(str(result) + '\n')

        return resultArr

    def vision_process(self, uri, keyword):
        # 從網路上得到圖片
        img = self.converter.url_to_image(uri)
        path = '../../img/recaptcha/' + keyword + '/'
        if not os.path.exists(path):
            os.makedirs(path)
        # 依序存檔
        fileNum = len(fnmatch.filter(os.listdir(path), '*.jpg'))
        print(path + str(fileNum + 1) + '.jpg')
        img.save(path + str(fileNum + 1) + '.jpg')
        # 驗證碼切塊
        pathArr = self.cropCaptcha(path, str(fileNum + 1))
        resultArr = []
        for index, blockPath in enumerate(pathArr):
            print(str(index) + '......' + blockPath)
            labels = self.vision.detectLabel(blockPath, blockPath.replace('.jpg', '_VisionLabels.txt'))
            if self.isContain(labels, keyword):
                resultArr.append(index+1)

        f = open(path + str(fileNum + 1) + '_vision.txt','w')
        for result in resultArr:
            f.write(str(result) + '\n')

        return resultArr


        
    # divide image into crops
    def crop(self, infile, height, width):
        im = Image.open(infile)
        imgwidth, imgheight = im.size
        for i in range(imgheight//height):
            for j in range(imgwidth//width):
                box = (j*width, i*height, (j+1)*width, (i+1)*height)
                yield im.crop(box)

    def cropCaptcha(self, directory, num):
        infile = directory + num + '.jpg'
        pathArr = []
        height = 100
        width = 100
        start_num = 1 
        for k,piece in enumerate(self.crop(infile, height, width),start_num):
            img = Image.new('RGB', (height,width), 255)
            img.paste(piece)
            if not os.path.exists(directory + num + '/'):
                os.makedirs(directory + num + '/')
            path = directory + num + '/' + str(k) + '.jpg'
            img.save(path)
            pathArr.append(path)
        return pathArr

    def isContain(self, labels, keyword):
        for label in labels:
            print(label + '-----' + keyword)
            if keyword == label:
                return True
        return False

    # 將本地端全部recaptcha切塊
    def cropAll(self, num):
        folder = 'car'
        height = 100
        width = 100
        start_num = 1 
        pathArr = []
        for i in range(1, num+1):
            pathArr.append([])
            infile = '../img/recaptcha/' + folder + '/' + str(i) +'.jpg'
            
            directory = '../img/recaptcha/' + folder + '/' + str(i)
            for k,piece in enumerate(self.crop(infile, height, width),start_num):
                img = Image.new('RGB', (height,width), 255)
                img.paste(piece)
                if not os.path.exists(directory):
                    os.makedirs(directory)
                path = '../img/recaptcha/' + folder + '/' + str(i) + '/' + str(k) + '.jpg'
                img.save(path)
                pathArr[i-1].append(path)
        return pathArr

    # 從clarifai取得結果
    def getLabels(self, infile):
        with open(infile, 'r') as f:
            data = json.load(f)
            labels = data['outputs'][0]['data']['concepts']
            labelArr = []
            f = open(infile.replace('.json', '_labels.txt'),'w')
            for label in labels:
                labelArr.append(label['name'])
                f.write(label['name'] + '\n')
            return labelArr

    # 是否包含關鍵字
    # def isContain(self, infile, keyword):
    #     f = open(infile, 'r')
    #     for line in f:
    #         if keyword == line.replace('\n', ''):
    #             return True
    #     return False

if __name__=='__main__':
    reCaptcha = recaptcha()
    # results = []
    # keyword = 'road'
    # for i in range(1,6):
    #     results.append([])
    #     print("開始處理第"+str(i)+"個JSON結果")
    #     for j in range(1,10):
    #         labels = reCaptcha.getLabels('K:\\BDProject_Captcha\\python\\img\\recaptcha\\'+keyword+'\\'+str(i)+'\\'+str(j)+'.json')
    #         result = reCaptcha.isContain('K:\\BDProject_Captcha\\python\\img\\recaptcha\\'+keyword+'\\'+str(i)+'\\'+str(j)+'_labels.txt', keyword)
    #         print(result)
    #         results[i-1].append(result)
    # for i in range(1,6):
    #     f = open('K:\\BDProject_Captcha\\python\\img\\recaptcha\\'+keyword+'\\'+str(i)+'_result.txt', 'w')
    #     for index, element in enumerate(results[i-1]):
    #         if element == True:
    #             f.write(str(index+1) + '\n')
    # print (len(fnmatch.filter(os.listdir('../img/recaptcha/road/'), '*.txt')))
    reCaptcha.vision_process('http://140.138.152.207/house/BDProject/upload/20170613131136_23037/src.png', 'car')