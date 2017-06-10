#coding=utf-8  

# 分割recaptcha的圖片九宮格


from PIL import Image
import os

# divide image into crops
def crop(infile, height, width):
    im = Image.open(infile)
    imgwidth, imgheight = im.size
    for i in range(imgheight//height):
        for j in range(imgwidth//width):
            box = (j*width, i*height, (j+1)*width, (i+1)*height)
            yield im.crop(box)

num = 6

if __name__=='__main__':
    infile = 'img/recaptcha/' + str(num) + '/payload.jpg'
    height = 100
    width = 100
    start_num=1
    for k,piece in enumerate(crop(infile, height, width),start_num):
        img=Image.new('RGB', (height,width), 255)
        img.paste(piece)
        path='img/recaptcha/' + str(num) + '/' + str(k) + '.jpg'
        img.save(path)