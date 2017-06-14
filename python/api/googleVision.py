import io
import os
import sys

# Imports the Google Cloud client library
from google.cloud import vision


class googleVision:

    def __init__(self):

        # Instantiates a client
        self.vision_client = vision.Client('plucky-lane-147516')

    def detectLabel(self, file_name, resultPath):
        file = open(resultPath,'w')
        # Loads the image into memory
        with io.open(file_name, 'rb') as image_file:
            content = image_file.read()
            image = self.vision_client.image(content=content)

        # Performs label detection on the image file
        labels = image.detect_labels()
        labelArr = []
        for label in labels:
            file.write(label.description + '\n')
            labelArr.append(label.description)
        return labelArr

    def detect_text_uri(self, uri):
        """Detects text in the file located in Google Cloud Storage or on the Web.
        """
        image = self.vision_client.image(source_uri=uri)

        texts = image.detect_text()
        if len(texts) > 0:
            print('Text:' + texts[0].description.replace('\n', '').encode(sys.stdin.encoding, "replace").decode(sys.stdin.encoding))
            return texts[0].description.replace('\n', '')
        else:
            return ''
        # for text in texts:
        #     print(text)
        #     print('\n"{}"'.format(text.description))
        #     vertices = (['({},{})'.format(bound.x_coordinate, bound.y_coordinate)
        #                 for bound in text.bounds.vertices])

        #     print('bounds: {}'.format(','.join(vertices)))

if __name__ == "__main__":
    vision = googleVision()
    # vision.detectLabel()
    vision.detect_text_uri('http://140.138.152.207/house/BDProject/upload/20170610133100_13776/3_test.png')