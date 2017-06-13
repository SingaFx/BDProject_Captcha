from clarifai.rest import ClarifaiApp
from clarifai.rest import Image as ClImage
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

    def predict_local(self, infile, resultPath):
        file = open(resultPath,'w')
        image = ClImage(file_obj=open(infile, 'rb'))
        result = self.model.predict([image])
        print()
        labels = result['outputs'][0]['data']['concepts']
        # file.write(json.dumps(result, indent=4, sort_keys=True))
        for label in labels:
            file.write(label['name'] + '\n')
        
        return labels

if __name__ == "__main__":
    folder = 'road'
    clarifai = clarifai_api()
    # clarifai.predict('https://samples.clarifai.com/metro-north.jpg')
    for i in range(1,6):
        print("開始處理第"+str(i)+"張圖")
        for j in range(1,10):
            print("第" + str(j) + "塊")
            clarifai.predict_local('K:\\BDProject_Captcha\\python\\img\\recaptcha\\'+folder+'\\'+str(i)+'\\'+str(j)+'.jpg', 'K:\\BDProject_Captcha\\python\\img\\recaptcha\\'+folder+'\\'+str(i)+'\\'+str(j)+'.json')