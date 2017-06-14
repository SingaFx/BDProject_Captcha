import pytesseract
class ocr:
    """docstring for ClassName"""
    def __init__(self, arg):
        self.img = arg
    def ocr_text(self):
        text = ''
        #img = url_to_image(url)
        #img.load()
        text = pytesseract.image_to_string(self.img, lang='eng')
        text = text.replace(' ', '')
        #print(url + '     ' + text)
        return text