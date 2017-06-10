import io
import os

# Imports the Google Cloud client library
from google.cloud import vision


class googleVision:

    def __init__(self):

        # Instantiates a client
        self.vision_client = vision.Client()

    def detectLabel(self):
        # The name of the image file to annotate
        file_name = 'demo-010.jpg'

        # Loads the image into memory
        with io.open(file_name, 'rb') as image_file:
            content = image_file.read()
            image = self.vision_client.image(content=content)

        # Performs label detection on the image file
        labels = image.detect_labels()

        print('Labels:')
        for label in labels:
            print(label.description)

    def detect_text_uri(self, uri):
        """Detects text in the file located in Google Cloud Storage or on the Web.
        """
        image = self.vision_client.image(source_uri=uri)

        texts = image.detect_text()
        print('Text:' + texts[0].description.replace('\n', ''))
        return texts[0].description.replace('\n', '')
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