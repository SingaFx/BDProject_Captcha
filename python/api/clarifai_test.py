from clarifai.rest import ClarifaiApp
import json
app = ClarifaiApp("2WskerTZYXTY5qe_p2m6NyYBz2JSEVLR0oS2Md0P", "c4H1_GGXF7ghm4PZd2F9MeUxyXmoXtf23wfGenls")

# get the general model
model = app.models.get("general-v1.3")

# predict with the model
print(json.dumps(model.predict_by_url(url='https://samples.clarifai.com/metro-north.jpg'), indent=4, sort_keys=True))