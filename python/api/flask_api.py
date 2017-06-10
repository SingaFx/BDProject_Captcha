#coding=utf-8  

# Flask API

#!flask/bin/python
from flask import Flask, jsonify
from flask import abort
from flask import make_response
from flask_httpauth import HTTPBasicAuth
from flask_cors import CORS
from flask import request
import io
import requests
import os
import sys
import numpy as np
import cv2
import urllib.request
import pytesseract
from PIL import Image, ImageEnhance
from io import StringIO
# from google.appengine.api import urlfetch

auth = HTTPBasicAuth()

app = Flask(__name__)
CORS(app)
methods = [
    {
        'id': 1,
        'description': u'Our algorithm'
    },
    {
        'id': 2,
        'description': u'Canny edge detection'
    },
    {
        'id': 3,
        'description': u'clarifai API'
    },
    {
        'id': 4,
        'description': u'google cloud vision API'
    }
]

@app.route('/BD_Project/api/v1.0/methods', methods=['GET'])
def get_methods():
    return jsonify({'methods': methods})

@app.route('/BD_Project/api/v1.0/methods/runAll', methods=['GET'])
# @auth.login_required
def runAll():
    error = ''
    m1 = ''
    m2 = ''
    m3 = ''
    m1_result = ''
    m2_result = ''
    m3_result = ''
    try:
        path = request.args.get('path')
        
        m1 = captcha(path)
        m2 = cannyDetection(path)
        m3 = testCaptcha(path)
        m1_result = ocr_text('http://140.138.152.207/house/BDProject/upload/' + m1)
        m2_result = ocr_text('http://140.138.152.207/house/BDProject/upload/' + m2)
        m3_result = ocr_text('http://140.138.152.207/house/BDProject/upload/' + m3)
    except Exception as e:
        error = e
        print(e)
    
    
    return jsonify(
        {
            'method1' : 
            {
                'path' : m1, 
                'result' : m1_result
            }, 
            'method2' : 
            {
                'path' : m2, 
                'result' : m2_result
            }, 
            'method3' : 
            {
                'path' : m3, 
                'result' : m3_result
            }
        })

@app.route('/BD_Project/api/v1.0/methods/<int:method_id>?<string:path>', methods=['GET'])
@auth.login_required
def get_method(method_id, path):

    method = list(filter(lambda t: t['id'] == method_id, methods))
    if len(method) == 0:
        abort(404)
    return jsonify({'method': method[0]})

@app.route('/BD_Project/api/v1.0/methods/<int:method_id>', methods=['POST'])
def create_method(method_id):
    if not request.json or not 'image' in request.json:
        abort(400)
    # with open('report.xls', 'rb') as f: 
        # r = requests.post('http://httpbin.org/post', files={'report.xls': f})
    method = {
        'id': methods[-1]['id'] + 1,
        'method': request.json.get('method', ""),
        'description': request.json.get('description', ""),
        'result': 'pathtofile'
    }
    methods.append(method)
    return jsonify({'method': method}), 201

@auth.get_password
def get_password(username):
    if username == 'frank85':
        return 'ak800730'
    return None

@auth.error_handler
def unauthorized():
    return make_response(jsonify({'error': 'Unauthorized access'}), 401)


def captcha(url):
    img = url_to_image('http://140.138.152.207/house/BDProject/upload/' + url + '/src.png')

    # 影像加強
    enhancer = ImageEnhance.Contrast(img)
    img = enhancer.enhance(5.0)
    enhancer = ImageEnhance.Brightness(img)
    img = enhancer.enhance(10.0)
    pixdata = img.load()

    if not os.path.exists('img'):
        os.makedirs('img')

    if not os.path.exists('img/' + url):
        os.makedirs('img/' + url)
        
    img.save('img/' + url + '/1_bright.png')
    r = requests.post('http://140.138.152.207/house/BDProject/receiver.php', files={'1_bright': open('img/' + url + '/1_bright.png', 'rb')}, data={'path':url})
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
                pixdata[i,j] = (255 , 255 , 255 , 255)


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
                        pixdata[i,j] = (255 , 255 , 255 , 255)
                        pass
            if count >= 7:
                pixdata[i,j] = (255 , 255 , 255 , 255)    
     
    img.save('img/' + url + '/1_black.png')
    r = requests.post('http://140.138.152.207/house/BDProject/receiver.php', files={'1_black': open('img/' + url + '/1_black.png', 'rb')}, data={'path':url})
    print (r.text)

    # 平滑補強
    # im = cv2.imread(path + '_black.png' , 0)

    # kernel = np.ones((2 , 2) , np.uint8)
    # opening = cv2.morphologyEx(im, cv2.MORPH_OPEN, kernel)

    # #opening = cv2.blur(opening , (2, 2))
    # #opening = cv2.dilate(opening, (1, 1), iterations=1)
    # cv2.imwrite(path +'_black2.png', opening)
    return url + '/1_black.png'

def cannyDetection(url):
    img = cv_url_to_image('http://140.138.152.207/house/BDProject/upload/' + url + '/src.png')
    if img is not None:
        height, width = img.shape[:2]

        # 去外框
        for i in range(len(img)):
            for j in range(len(img[i])):
                if i == 0 or i == len(img) - 1 or j == 0 or j == len(img[i]) -1:
                    img[i,j] = 255

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



        img = cv2.GaussianBlur(img,(3,3),0)  
        canny = cv2.Canny(img, 300, 150)  
        if not os.path.exists('img/' + url):
            os.makedirs('img/' + url)
        # cv2.imshow('Canny', canny)  
        cv2.imwrite('img/' + url + '/2_canny.png', canny)
        r = requests.post('http://140.138.152.207/house/BDProject/receiver.php', files={'2_canny': open('img/' + url + '/2_canny.png', 'rb')}, data={'path':url})
        print (r.text)
        # cv2.waitKey(0)  
        # cv2.destroyAllWindows()
        return url + '/2_canny.png'

def testCaptcha(url):
    im = cv_url_to_image('http://140.138.152.207/house/BDProject/upload/' + url + '/src.png')
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
        img = denoise(img)
        cv2.imwrite('img/' + url + '/3_test.png', img)
        r = requests.post('http://140.138.152.207/house/BDProject/receiver.php', files={'3_test': open('img/' + url + '/3_test.png', 'rb')}, data={'path':url})
        print (r.text)
        return url + '/3_test.png'

def denoise(cvimg):
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

def convertCVToPIL(cvimg):
    _,cv2_im = cvimg.read()
    cv2_im = cv2.cvtColor(cv2_im,cv2.COLOR_BGR2RGB)
    pil_im = Image.fromarray(cv2_im)
    return pil_im

def cv_url_to_image(url):
    # download the image, convert it to a NumPy array, and then read
    # it into OpenCV format
    # resp = urlfetch.fetch(url)
    resp = urllib.request.urlopen(url)
    image = np.asarray(bytearray(resp.read()), dtype="uint8")
    image = cv2.imdecode(image, cv2.IMREAD_COLOR)
 
    # return the image
    return image

def url_to_image(url):
    with urllib.request.urlopen(url) as imageUrl:
        f = io.BytesIO(imageUrl.read())
    img = Image.open(f)
    return img

def ocr_text(url):
    text = ''
    img = url_to_image(url)
    img.load()
    text = pytesseract.image_to_string(img, lang='eng')
    text = text.replace(' ', '')
    print(url + '     ' + text)
    return text

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)