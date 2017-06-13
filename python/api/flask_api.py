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

from googleVision import googleVision
sys.path.append('../')
from methods.url.main_captcha import main_captcha
from methods.url.canny_captcha import canny_captcha
from methods.url.benny_captcha import benny_captcha
from methods.url.recaptcha import recaptcha
sys.path.append('../')
from util.convertImage import convertImage

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
        'description': u'Our anoter algorithm'
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
vision = googleVision()
reCaptcha = recaptcha()
uri = 'http://140.138.152.207/house/BDProject/upload/'

@app.route('/BD_Project/api/v1.0/methods', methods=['GET'])
def get_methods():
    return jsonify({'methods': methods})

@app.route('/BD_Project/api/v1.0/methods/runAll', methods=['GET'])
# @auth.login_required
def runAll():
    
    
    path = request.args.get('path')
    main = main_captcha()
    canny = canny_captcha()
    benny = benny_captcha()
    m1 = main.captcha(path)
    m2 = benny.captcha(path)
    m3 = canny.cannyDetection(path)
    m1_result = ocr_text(uri + m1)
    m2_result = ocr_text(uri + m2)
    m3_result = ocr_text(uri + m3)
    
    
    return jsonify(
        {
            'method1' : 
            {
                'name' : 'Our algorithm',
                'path' : m1, 
                'tesseract_result' : m1_result,
                'googleVision_result' : vision.detect_text_uri(uri+m1).replace(' ', '')
                # 'googleVision_result' : ''
            }, 
            'method2' : 
            {
                'name' : 'Our anoter algorithm',
                'path' : m2, 
                'tesseract_result' : m2_result,
                'googleVision_result' : vision.detect_text_uri(uri+m2).replace(' ', '')
                # 'googleVision_result' : ''
            }, 
            'method3' : 
            {
                'name' : 'Canny Detection algorithm',
                'path' : m3, 
                'tesseract_result' : m3_result,
                'googleVision_result' : vision.detect_text_uri(uri+m3).replace(' ', '')
                # 'googleVision_result' : ''
            }
        })

@app.route('/BD_Project/api/v1.0/methods/reCaptcha', methods=['GET'])
# @auth.login_required
def googleReCaptcha():

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

def ocr_text(url):
    converter = convertImage()
    text = ''
    img = converter.url_to_image(url)
    img.load()
    text = pytesseract.image_to_string(img, lang='eng')
    text = text.replace(' ', '')
    print(url + '     ' + text)
    return text

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)