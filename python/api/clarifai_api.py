from clarifai.rest import ClarifaiApp
import json


class clarifai_api:

    def __init__(self):
        self.app = ClarifaiApp("2WskerTZYXTY5qe_p2m6NyYBz2JSEVLR0oS2Md0P", "c4H1_GGXF7ghm4PZd2F9MeUxyXmoXtf23wfGenls")
        # get the general model
        self.model = self.app.models.get("general-v1.3")

    def predict(self, uri):
        # predict with the model
        result = self.model.predict_by_url(url=uri)

        labels = result['outputs']['data']['concepts']
        # print(json.dumps(result, indent=4, sort_keys=True))

        return labels

if __name__ == "__main__":
    clarifai = clarifai_api()
    clarifai.predict('https://samples.clarifai.com/metro-north.jpg')