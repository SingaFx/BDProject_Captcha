#coding=utf-8  

# OCR引擎套用

import os
import subprocess

folder = 'yzu_course'
filename = '_black2.bmp'
def image_to_string(img, filename, cleanup=True, plus=''):
    subprocess.check_output('tesseract ' + img + ' ' +
                            filename + ' ' + plus, shell=True)
    text = ''
    with open(filename + '.txt', 'r') as f:
        text = f.read().strip()
    if cleanup:
        os.remove(filename + '.txt')
    return text


if __name__ == "__main__":
    for t in range(0,100):
        print(image_to_string('img/' + folder + '/' + str(t) + filename, 'img/' + folder + '/' + str(t), False))