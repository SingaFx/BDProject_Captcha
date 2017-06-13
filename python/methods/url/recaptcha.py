#coding=utf-8  

# 分割recaptcha的圖片九宮格
from PIL import Image
import os
import sys
import json
import fnmatch

from convertImage import convertImage
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
        path = '../../img/recaptcha/' + keyword + '/'
        if not os.path.exists(path):
            os.makedirs(path)
        # 依序存檔
        fileNum = len(fnmatch.filter(os.listdir(path), '*.jpg'))
        img.save(path + str(fileNum + 1) + '.jpg')
        # 驗證碼切塊
        pathArr = self.cropCaptcha(path, str(fileNum + 1))
        resultArr = []
        for index, blockPath in enumerate(pathArr):
            labels = self.clarifai.predict_local(blockPath, blockPath.replace('.jpg', '_labels.txt'))
            if self.isContain(labels, keyword):
                resultArr.append(index+1)

        f = open(path + str(fileNum + 1) + '_result.txt','w')
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
        img.save(path + str(fileNum + 1) + '.jpg')
        # 驗證碼切塊
        pathArr = self.cropCaptcha(path, str(fileNum + 1))
        resultArr = []
        for index, blockPath in enumerate(pathArr):
            labels = self.vision.detectLabel(blockPath, blockPath.replace('.jpg', '_labels.txt'))
            if self.isContain(labels, keyword):
                resultArr.append(index+1)

        f = open(path + str(fileNum + 1) + '_result.txt','w')
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
            infile = '../../img/recaptcha/' + folder + '/' + str(i) +'.jpg'
            
            directory = '../../img/recaptcha/' + folder + '/' + str(i)
            for k,piece in enumerate(self.crop(infile, height, width),start_num):
                img = Image.new('RGB', (height,width), 255)
                img.paste(piece)
                if not os.path.exists(directory):
                    os.makedirs(directory)
                path = '../../img/recaptcha/' + folder + '/' + str(i) + '/' + str(k) + '.jpg'
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
    reCaptcha.process('https://www.google.com/recaptcha/api2/payload?c=03AOPBWq8vJTdnr_6kObbPjJZkSpF8_i1RSXLIyE9xTtsapF5TsswEfbjJOMlF6e9CSZJfqva1hg5ke9NGfY-cbwvvKzAPhW29aE8BHU_DEAAObuiykpRUvUgfHmBMC3rGHGeHErYjoN_Ehq04qdthlDq0XB51MUmyHm6DDm-4wJG6doWN9sBr2ZJDQ9HkIxrPgrahhdNYLL11tC0Dkn7_vQ7L-rgtpGixEJfNbDxD3uNNDbOUr1UwDsVTCNXxeX3Vn7aEJqQyawZmC91alB2e0lFI0N6kQTCOWG4z7rK2oT46klY0mxYhYIBRKcX9VXG9S7SM0Rwuqd6VL9W8rHt8hSbomdQ_C7N0Y0lzV6mCfuumI8PeD5lH2UgL9R-xlzw_5kp98Jo7eAQMw8vx3Lh_UWa5-C-xeWWVh9sFx8XWMeo_zd4PZuOG9pOh9saa0MPe6EFsKeuUp_mJzo7xC4S55RxGiKOM50ZIkI6VJBV7hhP_0I7tEkXeA3spmI5K9kYtinycHsBJJQLtMDxbEATRi1ySCm6fwKZ-9PGLHleq4K8P1qHAEGXkEZCReAk_lIq27Rx3oJUFKcdOD7057lxp0Uq871Pl7bhWeDLPAjbz5wIs7xCQGkviKj9XH4m3ARlH1wUijPqwpaGCwA3qPLGSgEx3DYdBChWETaBE7XZlSA_c-0zqNT2Nl-igS_3nj-yuKqGmr1LhhGmT3p9kEVhia1col5C_lzlG8NyAorRHnOP5cYNAWGh91ig8wzZd-l6gkTDXhX5CxdAD8yWCXoV_G4wcHAkjchF1Rdt57qt9SKCIOLXJCIfS0diQ7eQ4t5kTFHwjYoZLT_EIztTiLlHxink6xr2z8IVegvx3SekQSH37VwQiiH6pg8ZKmYTcX8AYQPX7k883FJXeT3fxz23wXHz15Ehdv-R6ONLJ1CnOPTwrmM_Rkp3v0Q_DoscmjV0GhzPkr9MwN4CmqX9MZMl6Pnai4-WczNoxnMU5umI150b8cKJoOYkhqjTlb6nyW2216md3nR1Fzsp2vEOMehrnWOoW9zokULXbtJxQVDkxOLMOZCyGfKK7pL0_10qyzIhT24gImKrv-XJPHhuu0NOnMG8hDR0SqWIqyAkPIbWVFDonL8zXTYvcpwROJZuPYQOxc2lzoVDwGyZtdUEF40aFk6svbIA10NJkg2MDaYgBuAkL8I76o7jLpkZIbU5d1RepOmsTQnJ-K4HWB9WbeV7TAZ_0d8NbD6YJI56nsDCpiFNpsvEE9RzQXR9jDSQ-Fedi94FuAEes08BERDY8JHzSlRmfhq5oiv720jjrmshxx5GRTyEi2WMcEgv8nlafsA5KYvD6p1BFJh3G5oPCX6T5QVHrSzRFRgNLC-9FsTrx8JI7SpbJSYEfeuO3JqCKOGxuPIuEMkEXIav5EuJ-dFoqjmlM62IzzZBHPxlrXtEPxzuUAn-fffj8DohlI7OtGu8-fZT_IMlOiujEySxiKgyb3KWI-6nFF_1xKFseOE_FfpH0cpUA4VYi42rXjvarpb1BhwejAM-1AZFuRke0uPgf22_gHEFLbdhCOYMkptmm2JKANcNViKN01qaJh6sDn8miJhTWHlk9C7p6cS4769NUtRNnM-24K8iiZeSd9bR1blvatxQilq5mKob1andHmaDG_0S7D7U_ZQeZOcHavhW_9j1rDf5r3lbf774pbuGMtasJZ4kiU6UnijnlsuMcygo6RojD-YCQ18h_ncn5r79wOTHV2OVo3ip-iu8MaOtSA-cKv2WXuwZ6opZzE6AreWDcs_IyxsZQ2hkhz869pz92jLxlvgjvfl9lrsgWkXedCks-tsW961aWAvOR6CtGxzA4QEYiK2txlCWdY6jhtXiV6hOGFq7VYTv9QMdhaBgQ0d2YAOJ8Pf4zTxsqw-CD_z23EJKMgfuNeaLxojYdTdpGYaiMtkHnElQr0jRb49bPlZg0ewzSPYlFOrk1LnZQf-ydKYdbP84PxsCDmDpG_Mcjxe2ZEeZ3YO3v4eTGGgcAAfVwMQdqnfZ53jyZQJ4r4Ahj9n5vvPe9L4TARQeN3jDFab7Gk47Bc7p7QO_sJOXdc1lLvQsKkHTX5KUaWm3C4KzfY3NT3yh_4hJrH3yPgmmPzLlJAVreWLJM4A&k=6Le-wvkSAAAAAPBMRTvw0Q4Muexq9bi0DJwx_mJ-', 'car')