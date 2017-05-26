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
    r = requests.get('https://isdna1.yzu.edu.tw/Cnstdsel/SelRandomImage.aspx', headers=HEADER)
    f = open('img/yzu_course/' + str(i) + '.bmp', 'wb')
    f.write(r.content)
    f.close()
    print(i)