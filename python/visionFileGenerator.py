"""
This file is used to test Google Vision API. 
A JSON file with specified image would be generated according to user's input parameters. 
This file can be further sent to vision.googleapis.com for further analysis.

VMware SE:Shawn Ho 
Date: 2016/02/21
"""
import sys
import json
import base64
import argparse
import urllib.request

class VisionProcess:
    def __init__(self, ProcessName):
        self._processName = ProcessName
    def __repr__(self):
        return json.dumps({'requests': [{'image': {'content': self._imgContent}, 'features': [{'type': self._processName, 'maxResults': 1}]}]}, indent=4)
    def setProcessName(self, ProcessName):
        self._processName = ProcessName
    def loadImage(self, ImgName):
        with open(ImgName, 'r') as f:
            self._imgContent = base64.b64encode(f.read())
    def loadUrl(self, url):
        with urllib.request.urlopen(url) as url:
            self._imgContent = base64.b64encode(url.read())
    def save(self, fileName):
        with open(fileName, 'wt') as f:
            f.write(json.dumps({'requests': [{'image': {'content': self._imgContent.decode("utf-8")}, 'features': [{'type': self._processName, 'maxResults': 3}]}]}, indent=4))
if __name__ == '__main__':
    apiInput = VisionProcess("LABEL_DETECTION")
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-u', '--url', help="Image URL for Analysis", dest="source")
    parser.add_argument('-p', '--process', help="Set Detection Process", default="LABEL_DETECTION")
    parser.add_argument('-o', '--outputName', help="Output JSON file name", default="test.txt")
    group.add_argument('-f', '--file', help="Image File Path for Analysis", dest="source")
    try:
        args = parser.parse_args()
        apiInput.setProcessName(args.process)
        print (args.source)
        if 'http' in args.source:
            apiInput.loadUrl(args.source)
        else:
            apiInput.loadImage(args.source)
        apiInput.save(args.outputName)
    except IOError as msg:
        parser.error(str(msg))