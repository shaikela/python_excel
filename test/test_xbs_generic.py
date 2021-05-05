import requests
from datetime import datetime
import services.xbs_generic as xbs_generic
import pytest
import os 
from pathlib import Path
import json

def testXbsGenericDirect(): 
    cancelReference()
    response=requestLabel('XBS_PPTT_label_request.json')
    try:
        response_json=json.loads(response)
        response_status=response_json['ErrorLevel']
        if response_status!=0:
            pytest.fail("XBS error, level:"+response_status)
    except:
        pytest.fail("unknown error")

    base64_str=response_json['Shipment']['LabelImage']
    if(len(base64_str)<5000):
        pytest.fail("label too short")
    tracking_number =response_json['Shipment']['CarrierTrackingNumber']
    if (len(tracking_number)<10):
        pytest.fail("tracking_number too short")

 
def requestLabel(resouceName):
    myTest=xbs_generic.XbsGeneric()
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

def cancelReference():
    url="https://mtapi.net/?testMode=1"
    body="{\"Apikey\":\"398fd1325dd29018\",\"Command\":\"VoidShipment\",\"Shipment\" : {\"ShipperReference\" : \"Test_001\" }}"
    response=requests.post(url,data=body)
    if response.status_code!=200:
        pytest.fail("cannot cancel reference")
