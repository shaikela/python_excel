import pytest
import requests
import xml.etree.ElementTree as ET
from datetime import datetime

class FedexGeneric:
    message=""
    def __init__(self):
        pass

    def generateLabel(self,labelRequest):
        url = "http://xpit.4log.com/Magicxpi4.7/MgWebRequester.dll?appname=IFSFedex_Generic&prgname=HTTP&arguments=-AFedex_Generic%23Trigger1&testMode=1"
        headers = {}
        fedex_response = requests.request("POST", url, headers=headers, data = labelRequest)
        if (fedex_response.status_code!=200):
            self.message="No response from service"
            return 0
        print("response time:"+str(fedex_response.elapsed.total_seconds()))
        self.message=fedex_response.text
        return 1

