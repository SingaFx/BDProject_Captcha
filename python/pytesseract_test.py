from PIL import Image
import pytesseract
import urllib.request
import io
def ocr_text(image_path):
    text = ''

    img = Image.open(image_path)
    img.load()
    text = pytesseract.image_to_string(img, lang='eng')

    return text

def url_to_image(url):
    with urllib.request.urlopen(url) as imageUrl:
        f = io.BytesIO(imageUrl.read())
    img = Image.open(f)
    return img

def ocr_text_url(url):
    text = ''
    print(url)
    img = url_to_image(url)
    img.load()
    text = pytesseract.image_to_string(img, lang='eng')
    return text

if __name__ == "__main__":
    # for t in range(0,100):
    # print(ocr_text("K:\\BDProject_Captcha\\python\\img\\yzu_course\\"+str(t)+"_black2.bmp"))
    print(ocr_text("K:\\BDProject_Captcha\\python\\img\\yzu_course\\3_test.jpg"))
    print(ocr_text_url('http://140.138.152.207/house/BDProject/upload/20170607115031_18979/3_test.jpg'))