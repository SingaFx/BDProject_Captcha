#coding=utf-8  

# 批量儲存驗證碼


import requests
HEADER = {'Connection': 'keep-alive',
          'Cache-Control': 'max-age=0',
          'Upgrade-Insecure-Requests': '1',
          'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko)',
          'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
          'Accept-Encoding': 'gzip, deflate, sdch',
          'Accept-Language': 'zh-CN,zh;q=0.8',
          }
for i in range(0,100):
    # r = requests.get('http://railway.hinet.net/ImageOut.jsp?pageRandom=0.026864249647313043', headers=HEADER)
    r = requests.get('http://140.138.152.207/house/BDProject/upload/20170604110606_8373/src.jpg', headers=HEADER)
    # f = open('img/railway/' + str(i) + '.bmp', 'wb')
    f = open('img/get.bmp', 'wb')
    f.write(r.content)
    f.close()
    print(i)