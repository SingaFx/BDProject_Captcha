import sys
import pytesseract
from .convertImage import convertImage
from .GetConfig import GetConfig
class ocr:
    def __init__(self):
        self.converter = convertImage()
        self.config = GetConfig()

    def ocr_text(self, url):
        
        text = ''
        img = self.converter.url_to_image(url)
        img.load()
        text = pytesseract.image_to_string(img, lang='eng', config=self.config.pytesseract_traindata)
        text = text.replace(' ', '')
        print(url + '     ' + text.encode(sys.stdin.encoding, "replace").decode(sys.stdin.encoding))
        return text

    def ocr_text_img(self, img):
        img.load()
        text = pytesseract.image_to_string(img, lang='eng')
        text = text.replace(' ', '')
        print('驗證碼: ' + text)
        return text

if __name__ == "__main__":
    print(ocr().ocr_text('http://140.138.152.207/house/BDProject/upload/20170613170511_3819/src.png'))