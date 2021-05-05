import pytest
import os 
from pathlib import Path
import  services.delivery_generic as delivery_generic
 
    # testCreateDelivery()
def testCreateDeliveryHeader(): #S.O 1202
    script_dir = Path(os.path.dirname(__file__)) 
    resourcePath=os.path.join(Path(os.path.dirname(__file__)),'resources')    
    myTest=delivery_generic.CreateDelivery(1)
    if not myTest.cancelDelivery("1202","01001274"):
        pytest.fail("Cancel delivery failed. Details:"+myTest.message)
    with open(os.path.join(resourcePath,'1202_01001274_header.json')) as testResourceFile:
        deliveryRequest=testResourceFile.read()
    if not myTest.createDeliveryHeader(deliveryRequest):
        pytest.fail("Delivery header creation failed. Response:"+myTest.message)
        


def testCreateDeliveryItems(): #S.O 1201 - bpost 25008
    script_dir = Path(os.path.dirname(__file__)) 
    resourcePath=os.path.join(Path(os.path.dirname(__file__)),'resources')    
    with open(os.path.join(resourcePath,'1201_01001274_items.json')) as testResourceFile:
        deliveryRequest=testResourceFile.read()

        
    myTest=delivery_generic.CreateDelivery(1)
    currentItemCount=myTest.getDeliveryItemsCount(25008)
    if not myTest.createDeliveryItems(deliveryRequest):
        pytest.fail(" Delivery items creation failed. Response:"+myTest.message)
    if myTest.getDeliveryItemsCount(25008)-currentItemCount!=1:
        pytest.fail(" Unexpected delivery items count")




