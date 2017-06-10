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

sys.path.append('../')
from methods.url.main_captcha import main_captcha
from methods.url.canny_captcha import canny_captcha
from methods.url.benny_captcha import benny_captcha
sys.path.append('../../')
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
        main = main_captcha()
        canny = canny_captcha()
        benny = benny_captcha()
        m1 = main.captcha(path)
        m2 = canny.cannyDetection(path)
        m3 = benny.captcha(path)
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