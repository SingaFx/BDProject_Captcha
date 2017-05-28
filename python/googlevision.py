from google.cloud import vision

def detect_labels_uri(uri):
    """Detects labels in the file located in Google Cloud Storage or on the
    Web."""
    vision_client = vision.Client()
    image = vision_client.image(source_uri=uri)

    labels = image.detect_labels()
    print('Labels:')

    for label in labels:
        print(label.description)