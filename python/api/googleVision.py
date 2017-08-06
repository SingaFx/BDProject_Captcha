import io
import os
import sys

# Imports the Google Cloud client library
from google.cloud import vision
from google.cloud.vision import types

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

    def detect_text(self, path):
        """Detects text in the file."""
        client = vision.ImageAnnotatorClient()

        with io.open(path, 'rb') as image_file:
            content = image_file.read()

        image = types.Image(content=content)

        response = client.text_detection(image=image)
        texts = response.text_annotations
        print('Texts:')

        for text in texts:
            print('\n"{}"'.format(text.description))

            vertices = (['({},{})'.format(vertex.x, vertex.y)
                        for vertex in text.bounding_poly.vertices])

            print('bounds: {}'.format(','.join(vertices)))

    def detect_text_uri(self, uri):
        """Detects text in the file located in Google Cloud Storage or on the Web.
        """
        # image = self.vision_client.image(source_uri=uri)

        # texts = image.detect_text()
        # print(texts)
        # if len(texts) > 0:
        #     print('Text:' + texts[0].description.replace('\n', '').encode(sys.stdin.encoding, "replace").decode(sys.stdin.encoding))
        #     return texts[0].description.replace('\n', '')
        # else:
        #     return ''
        # # for text in texts:
        # #     print(text)
        # #     print('\n"{}"'.format(text.description))
        # #     vertices = (['({},{})'.format(bound.x_coordinate, bound.y_coordinate)
        # #                 for bound in text.bounds.vertices])

        # #     print('bounds: {}'.format(','.join(vertices)))


        """Detects text in the file located in Google Cloud Storage or on the Web.
        """
        client = vision.ImageAnnotatorClient()
        image = types.Image()
        image.source.image_uri = uri

        response = client.text_detection(image=image)
        print(response)
        texts = response.text_annotations
        print('Texts:')

        for text in texts:
            print('\n"{}"'.format(text.description))

            vertices = (['({},{})'.format(vertex.x, vertex.y)
                        for vertex in text.bounding_poly.vertices])

            print('bounds: {}'.format(','.join(vertices)))

if __name__ == "__main__":
    v = googleVision()
    print(v.detect_text_uri('http://218.161.48.30/BDProject/upload/20170805143147_785264572/3_test.png'))
    # v.detect_text('./img/text.png')