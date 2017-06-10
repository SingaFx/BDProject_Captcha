import urllib.request
import io
import numpy as np
import cv2
from PIL import Image
class convertImage:
    def convertCVToPIL(self, cvimg):
        _,cv2_im = cvimg.read()
        cv2_im = cv2.cvtColor(cv2_im,cv2.COLOR_BGR2RGB)
        pil_im = Image.fromarray(cv2_im)
        return pil_im

    def cv_url_to_image(self, url):
        # download the image, convert it to a NumPy array, and then read
        # it into OpenCV format
        # resp = urlfetch.fetch(url)
        resp = urllib.request.urlopen(url)
        image = np.asarray(bytearray(resp.read()), dtype="uint8")
        image = cv2.imdecode(image, cv2.IMREAD_COLOR)
     
        # return the image
        return image

    def url_to_image(self, url):
        with urllib.request.urlopen(url) as imageUrl:
            f = io.BytesIO(imageUrl.read())
        img = Image.open(f)
        return img