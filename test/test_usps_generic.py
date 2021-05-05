import requests
import xml.etree.ElementTree as ET
from datetime import datetime
import services.usps_generic as usps_generic
import pytest
import os 
from pathlib import Path

def testUspsGenericDirect(): 
    response=requestLabel('USPS_FC_W13.txt')
    root = ET.fromstring(response)
    base64_str=root.find(".//LabelImage").text

    if(len(base64_str)<5000):
        pytest.fail("label too short")
    tracking_number =root.find(".//BarcodeNumber").text
    if (len(tracking_number)<10):
        pytest.fail("tracking_number too short")

 
def requestLabel(resouceName):
    myTest=usps_generic.UspsGeneric()
    labelRequest=loadLabelRequest(resouceName)
    if not myTest.generateLabel(labelRequest):
        pytest.fail("Label creation failed. Response:"+myTest.message)
    # response_file=open('response.xml','r',encoding='utf-8-sig')
    return myTest.message


def loadLabelRequest(resourceName):
    script_dir = Path(os.path.dirname(__file__)) 
    resourcePath=os.path.join(Path(os.path.dirname(__file__)),'resources')    
    with open(os.path.join(resourcePath,resourceName),encoding='utf8') as testResourceFile:
        labelRequest=testResourceFile.read()
    return labelRequest

