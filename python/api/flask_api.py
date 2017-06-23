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
import re
import urllib.request
import datetime
from random import randint
from PIL import Image, ImageEnhance
from io import StringIO

from googleVision import googleVision
# methods import
sys.path.append('../')
from methods.url.main_captcha import main_captcha
from methods.url.canny_captcha import canny_captcha
from methods.url.benny_captcha import benny_captcha
from methods.url.recaptcha import recaptcha
# util import
sys.path.append('../')
from util.convertImage import convertImage
from util.ocr import ocr
from util.db import db

auth = HTTPBasicAuth()
app = Flask(__name__)
CORS(app)
methods = [
    {
        'id': 1,
        'description': u'Our first algorithm'
    },
    {
        'id': 2,
        'description': u'Our second algorithm'
    },
    {
        'id': 3,
        'description': u'Canny Detection algorithm'
    },
    {
        'id': 4,
        'description': u'google cloud vision API'
    },
    {
        'id': 5,
        'description': u'clarifai API'
    }
]


# init
db = db()
vision = googleVision()
reCaptcha = recaptcha()
ocr = ocr()
uri = 'http://140.138.152.207/house/BDProject/upload/'
main = main_captcha()
benny = benny_captcha()
canny = canny_captcha()
captcha_methods = [main, benny, canny]
@app.route('/BD_Project/api/v1.0/methods', methods=['GET'])
def get_methods():
    return jsonify({'methods': methods})

@app.route('/BD_Project/api/v1.0/methods/runAll', methods=['GET'])
# @auth.login_required
def runAll():
    path = request.args.get('path')
    if path is None:
        abort(404)
    pathArr = []
    for index, method in enumerate(captcha_methods):
        # 'http://140.138.152.207/house/BDProject/upload/' + rand + '/src.png'
        pathArr.append(captcha_methods[index].run('http://140.138.152.207/house/BDProject/upload/' + path + '/src.png', path))
    resultArr = []
    
    for index, captcha in enumerate(pathArr):
        resultArr.append([])
        if captcha != '':
            resultArr[index].append(re.sub('[^a-zA-Z0-9]', '', ocr.ocr_text(uri + captcha).replace(' ', '')))
            resultArr[index].append(re.sub('[^a-zA-Z0-9]', '', vision.detect_text_uri(uri + captcha).replace(' ', '')))
        else:
            resultArr[index].append('')
            resultArr[index].append('')
            

    return jsonify(
        {
            'method1' : 
            {
                'name' : 'Our first algorithm',
                'path' : pathArr[0], 
                'tesseract_result' : resultArr[0][0],
                'googleVision_result' : resultArr[0][1]
                # 'googleVision_result' : ''
            }, 
            'method2' : 
            {
                'name' : 'Our second algorithm',
                'path' : pathArr[1], 
                'tesseract_result' : resultArr[1][0],
                'googleVision_result' : resultArr[1][1],
                # 'googleVision_result' : ''
            }, 
            'method3' : 
            {
                'name' : 'Canny Detection algorithm',
                'path' : pathArr[2], 
                'tesseract_result' : resultArr[2][0],
                'googleVision_result' : resultArr[2][1],
                # 'googleVision_result' : ''
            }
        })

@app.route('/BD_Project/api/v1.0/methods/reCaptcha', methods=['GET'])
# @auth.login_required
def googleReCaptcha():

    ClarifaiResult = ''
    VisionResult = ''
    path = request.args.get('path')
    keyword = request.args.get('keyword')
    ClarifaiResult = reCaptcha.clarifai_process(uri+path+'/src.png', keyword)
    VisionResult = reCaptcha.vision_process(uri+path+'/src.png', keyword)
    return jsonify(
        {
            'method1' : 
            {
                'name' : 'GoogleVision',
                'result' : VisionResult
            }, 
            'method2' : 
            {
                'name' : 'Clarifai',
                'result' : ClarifaiResult
            }
        })


@app.route('/BD_Project/api/v1.0/methods/<int:method_id>', methods=['GET'])
# @auth.login_required
def get_method(method_id):
    url = request.args.get('url')
    api_key = request.args.get('key')
    method = list(filter(lambda t: t['id'] == method_id, methods))
    if len(method) == 0 or url is None or api_key is None:
        abort(404)

    if validate(api_key):
        rand = datetime.datetime.now().strftime("%Y%m%d%H%M%S") + '_' + str(randint(1,32768))
        captchaResult = captcha_methods[method_id-1].run(url, rand)
        if captchaResult != '':
            tesseractResult = re.sub('[^a-zA-Z0-9]', '', ocr.ocr_text(uri + captchaResult).replace(' ', ''))
            visionResult = re.sub('[^a-zA-Z0-9]', '', vision.detect_text_uri(uri + captchaResult).replace(' ', ''))
        else:
            tesseractResult = ''
            visionResult = ''

        return jsonify(
            {
                'method' + str(method_id): 
                {
                    'name' : methods[method_id-1]['description'],
                    'tesseract_result' : tesseractResult,
                    'googleVision_result' : visionResult
                }
            })
    else:
        abort(422)

@auth.get_password
def get_password(username):
    if username == 'frank85':
        return 'ak800730'
    return None

@auth.error_handler
def unauthorized():
    return make_response(jsonify({'error': 'Unauthorized access'}), 401)

def validate(api_key):
    print(api_key)
    data = db.execute('SELECT * FROM db_captcha_user WHERE api_key="'+api_key+'"')
    if data is not None:
        return True
    else:
        return False

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)