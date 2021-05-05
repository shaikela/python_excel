import requests
import xml.etree.ElementTree as ET
import json 

class CreateDelivery:
    testMode=1
    message=""
    def __init__(self,testMode):
        self.testMode=testMode

    # S.O number 1201
    def createDeliveryHeader(self,delivery_request):
        create_delivery_url="http://xpit.4log.com/Magicxpi4.7/MgWebRequester.dll?appname=IFSDelivery_Generic&prgname=HTTP&arguments=-ARest_Incoming%23IncomingFile"
        # delivery_request='{"CreateDelivery": {"userName": "JWGusernameTest","password": "JWGpasswardTest","s": {"AddrValid": "ACK","Location": 0,"ShipType": "1","AddressLine1": "2796 Garrett Place","AddressLine3City": "Woodland","AddressLine4State": "CA","CountryCode": "US","EndContactEmail": "richrowe_2000@yahoo.com","EndContactPhone": "5108213739","FirstName": "Richard","Height": 0,"LastName": "Rowe","Length": 0,"OrderNumber": "1201","ParcelWeight": 2.1,"Postcode": "95776","ShipmentItemsArray": [{"ProductDescription": "ViriMASK™","ProductItemOrigin": "IL","ProductQuantity": 5.0,"ProductUnitValue": 0,"ProductUnitWeight": 0.42}],"Width": 0}}}'
        delivery_request=delivery_request.encode('utf-8')
        response= requests.post(create_delivery_url,data=delivery_request)
        if response.status_code!=200:
            self.message="no response from server"
            return 0
        print("delivery response time:"+str(response.elapsed.total_seconds()))
        
        try:
            response_json=response.json()
            response_status=response_json['CreateDeliveryResponse']['StatusMessage']
            new_delivery_id=int(response_json['CreateDeliveryResponse']['Fourlogref'])
            if response_status!='OK':
                self.message=response_status
                return 0
        except:
            self.message="unknown error"
            return 0
        self.message=new_delivery_id
        return 1

    # test create items
    def createDeliveryItems(self,delivery_request):
        # jsonRequest= json.loads(delivery_request)
        # deliveryId=jsonRequest['CreateDelivery']['s']['Fourlogref']
        # deliveryItemsCount= self.getDeliveryItemsCount(deliveryId)
        # delivery_request='{"CreateDelivery": {"userName": "JWGusernameTest","password": "JWGpasswardTest","s": {"Fourlogref":"25007","AddrValid": "ACK","Location": 0,"ShipType": "1","AddressLine1": "2796 Garrett Place","AddressLine3City": "Woodland","AddressLine4State": "CA","CountryCode": "US","EndContactEmail": "richrowe_2000@yahoo.com","EndContactPhone": "5108213739","FirstName": "Richard","Height": 0,"LastName": "Rowe","Length": 0,"OrderNumber": "1201","ParcelWeight": 2.1,"Postcode": "95776","ShipmentItemsArray": [{"ProductDescription": "ViriMASK™","ProductItemOrigin": "IL","ProductQuantity": 5.0,"ProductUnitValue": 0,"ProductUnitWeight": 0.42}],"Width": 0}}}'

        create_delivery_url="http://xpit.4log.com/Magicxpi4.7/MgWebRequester.dll?appname=IFSDelivery_Generic&prgname=HTTP&arguments=-ARest_Incoming%23IncomingFile&testMode="+str(self.testMode)
        delivery_request=delivery_request.encode('utf-8')
        response= requests.post(create_delivery_url,data=delivery_request)
        if response.status_code!=200:
            self.message="no response from server"
            return 0
        print("delivery response time:"+str(response.elapsed.total_seconds()))
        
        try:
            response_json=response.json()       
            response_message=response_json['CreateDeliveryResponse']['StatusMessage']
            if response_message!='OK':
                self.message=response_message
                return 0
        except:
            self.message="unknown error"
            return 0
        return 1

    def getDeliveryItemsCount(self,deliveryID):
        get_items_url="http://192.117.139.143:57772/rest/api/Shipping1/CountDeliveryItems/"+str(deliveryID)
        response = requests.get(get_items_url)
        if response.status_code!=200:
            return -1
        try:         
            response_json=response.json()
            return response_json['ItemCount']
        except:
            return -1

    def getDeliveryDetails(self,soNumber,vendorCode,deliveryId):
        if deliveryId:
            get_details_url="http://192.117.139.143:57772/rest/api/TRN/GetDeliveryDetails/"+str(soNumber)+"/"+str(vendorCode)+"/"+str(deliveryId)
        else:
            get_details_url="http://192.117.139.143:57772/rest/api/TRN/GetDeliveryDetails/"+str(soNumber)+"/"+str(vendorCode)+"/0"
        response = requests.get(get_details_url)
        if response.status_code!=200:
            print("no response from server")    
            return None
        response_json=response.json()
        
        if (len(response_json['children'])):
            return response_json['children'][0]['DeliveryID']
        else:
            return 0
    def updateDeliveryStatus(self,deliveryId,status):
        update_delivery_status_url="http://192.117.139.143:57772/rest/api/Shipping1/UpdateDeliveryStatus"
        update_status_url=update_delivery_status_url +"/"+str(deliveryId)+"/"+str(status)
        response = requests.post(update_status_url)
        if response.status_code!=200:
            self.message='no response from server'
            return 0
        response_json=response.json()
        if (response_json['ErrorLevel'])!=0:
            self.message='error updating delivery status'
            return 0
        print("updated deliver "+str(deliveryId)+" status to:"+status)
        return 1

    def cancelDelivery(self,soNumber,vendorCode):
        deliveryId=self.getDeliveryDetails(soNumber,vendorCode,0) # deliveryId=getDeliveryDetails("1201","01001274")       
        if (deliveryId is not None and deliveryId!=0):
            return  self.updateDeliveryStatus(deliveryId,"Cancelled")
        else:
            return 1




