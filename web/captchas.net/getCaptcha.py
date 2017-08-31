#coding=utf-8  
from PIL import Image
import requests
import urllib.request
import os
import threading
from bs4 import BeautifulSoup
import random, string

def getImg(num):
    for j in range(5000):
        r = requests.get('http://140.138.152.207/BDProject/captchas.net/query.php')
        soup = BeautifulSoup(r.text, 'lxml')
        img_pwd = soup.find("a", {"id": "pwd"}).string
        print(img_pwd)
        img_url = soup.find("img", {"id": "captchas.net"})
        img_url = img_url['src']
        print(img_url)

        if not os.path.exists('img' + str(num)):
            os.makedirs('img' + str(num))
        urllib.request.urlretrieve(img_url, 'img' + str(num) + '/' + img_pwd + '.png')
        
def getFreebitcoin(num):
    url = 'https://captchas.freebitco.in/cgi-bin/captcha_generator?client=freebitcoin&random='
    randomStr = ''.join(random.choice(string.ascii_letters) for x in range(20))
    urllib.request.urlretrieve(url + randomStr, 'freebitcoin/' + str(num) + '.png')

def pasteLogo():
    all_image = os.listdir('./freebitcoin/')
    logo = Image.open('logo.jpg')
    logo.convert('RGB')
    for file in all_image:
        print(file)
        img = Image.open('./freebitcoin/' + file)
        img.convert('RGB')
        img.paste(logo, (153,61))
        img.save('./freebitcoin/' + file)

pasteLogo()
# for i in range(0, 2):
    # threading.Thread(target = getImg, args = (i,), name = 'Thread-' + str(i)).start() 
    # getFreebitcoin(i)
