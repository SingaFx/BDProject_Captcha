import sys
import pytesseract
from convertImage import convertImage

class ocr:
    def __init__(self):
        self.converter = convertImage()


    def ocr_text(self, url):
        
        text = ''
        img = self.converter.url_to_image(url)
        img.load()
        text = pytesseract.image_to_string(img, lang='eng')
        text = text.replace(' ', '')
        print(url + '     ' + text.encode(sys.stdin.encoding, "replace").decode(sys.stdin.encoding))
        return text