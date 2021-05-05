import pytest
import requests
import xml.etree.ElementTree as ET
from datetime import datetime

class ShippingGeneric:
    message=""
    def __init__(self):
        pass

    def generateLabel(self,labelRequest):
        url = "http://xpit.4log.com/Magicxpi4.7/MgWebRequester.dll?appname=IFSShipping_Generic&prgname=HTTP&arguments=-ARest_Incoming%23IncomingFile&testMode=1"

        headers = {}
        labelRequest=labelRequest.encode('utf-8')
        courier_response = requests.request("POST", url, headers=headers, data = labelRequest)
        if (courier_response.status_code!=200):
            self.message="No response from service"
            return 0
        print("response time:"+str(courier_response.elapsed.total_seconds()))
        self.message=courier_response.text
        return 1

