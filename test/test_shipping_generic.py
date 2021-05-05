import xml.etree.ElementTree as ET
from datetime import datetime
import services.shipping_generic as shipping_generic
import pytest
import os 
from pathlib import Path
import json

def testShippingGenericDirect(): 
    response=requestLabel()
    root = ET.fromstring(response)
    label=root.find(".//Label")
    base64_str=label.find("Parts/Image")
    if(len(base64_str.text)<5000):
        pytest.fail("label too short")
    shipment_details=root.findall("CompletedShipmentDetail")
    tracking_number =shipment_details[0].find("MasterTrackingId/TrackingNumber").text
    if (len(tracking_number)<10):
        pytest.fail("tracking_number too short")

def testShippingGeneric(): 
    response=requestLabel(0)
    try:
        response_json=json.loads(response)
        response_status=response_json['CreateShipmentResponse']['StatusMessage']
        if response_status!='OK':
            pytest.fail(response_status)
    except:
        pytest.fail("unknown error")

    base64_str=response_json['CreateShipmentResponse']['base64label']
    if(len(base64_str)<5000):
        pytest.fail("label too short")
    tracking_number =response_json['CreateShipmentResponse']['TrackingNumber']
    if (len(tracking_number)<10):
        pytest.fail("tracking_number too short")

def requestLabel():
    myTest=shipping_generic.ShippingGeneric()
    labelRequest=loadLabelRequest()
    if not myTest.generateLabel(labelRequest):
        pytest.fail("Label creation failed. Response:"+myTest.message)
    # response_file=open('response.xml','r',encoding='utf-8-sig')
    return myTest.message


def loadLabelRequest():
    script_dir = Path(os.path.dirname(__file__)) 
    resourcePath=os.path.join(Path(os.path.dirname(__file__)),'resources')    
    with open(os.path.join(resourcePath,'1201_01001274_generic_label.json')) as testResourceFile:
        labelRequest=testResourceFile.read()
    return labelRequest
    # request_str="<?xml version=\"1.0\" encoding=\"UTF-8\" standalone=\"no\" ?>\n\t<ns:ProcessShipmentRequest xmlns:ns=\"http://fedex.com/ws/ship/v23\" xmlns:xs=\"http://www.w3.org/2001/XMLSchema\" xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\">\n\t\t<ns:WebAuthenticationDetail>\n\t\t\t<ns:ParentCredential>\n\t\t\t\t<ns:Key>1adTJtjjeYK2yoY8</ns:Key>\n\t\t\t\t<ns:Password>iZOgdGnpfVmT4zrPkrqBH8uvR</ns:Password>\n\t\t\t</ns:ParentCredential>\n\t\t\t<ns:UserCredential>\n\t\t\t\t<ns:Key>1adTJtjjeYK2yoY8</ns:Key>\n\t\t\t\t<ns:Password>iZOgdGnpfVmT4zrPkrqBH8uvR</ns:Password>\n\t\t\t</ns:UserCredential>\n\t\t</ns:WebAuthenticationDetail>\n\t\t<ns:ClientDetail>\n\t\t\t<ns:AccountNumber>510087640</ns:AccountNumber>\n\t\t\t<ns:MeterNumber>119057338</ns:MeterNumber>\n\t\t\t<ns:Localization>\n\t\t\t\t<ns:LanguageCode>EN</ns:LanguageCode>\n\t\t\t\t<ns:LocaleCode>US</ns:LocaleCode>\n\t\t\t</ns:Localization>\n\t\t</ns:ClientDetail>\n\t\t<ns:TransactionDetail>\n\t\t\t<ns:Localization>\n\t\t\t\t<ns:LanguageCode>EN</ns:LanguageCode>\n\t\t\t\t<ns:LocaleCode>US</ns:LocaleCode>\n\t\t\t</ns:Localization>\n\t\t</ns:TransactionDetail>\n\t\t<ns:Version>\n\t\t\t<ns:ServiceId>ship</ns:ServiceId>\n\t\t\t<ns:Major>23</ns:Major>\n\t\t\t<ns:Intermediate>0</ns:Intermediate>\n\t\t\t<ns:Minor>0</ns:Minor>\n\t\t</ns:Version>\n\t\t<ns:RequestedShipment> <ns:ShipTimestamp>*ShipTimestamp*</ns:ShipTimestamp>\n\t\t\t<ns:DropoffType>REGULAR_PICKUP</ns:DropoffType>\n\t\t\t<ns:ServiceType>SMART_POST</ns:ServiceType>\n\t\t\t<ns:PackagingType>YOUR_PACKAGING</ns:PackagingType>\n\t\t\t<ns:ManifestDetail>\n\t\t\t\t<ns:ManifestReferenceType>CUSTOMER_REFERENCE</ns:ManifestReferenceType>\n\t\t\t</ns:ManifestDetail>\n\t\t\t<ns:TotalWeight>\n\t\t\t\t<ns:Units>KG</ns:Units>\n\t\t\t\t<ns:Value>0.8</ns:Value>\n\t\t\t</ns:TotalWeight>\n\t\t\t<ns:PreferredCurrency>USD</ns:PreferredCurrency>\n\t\t\t<ns:Shipper>\n\t\t\t\t<ns:AccountNumber>510087640</ns:AccountNumber>\n\t\t\t\t<ns:Contact>\n\t\t\t\t\t<ns:PersonName>Avi Chinaman</ns:PersonName>\n\t\t\t\t\t<ns:CompanyName>4LOG LTD (jwg) C/O Freight Bro</ns:CompanyName>\n\t\t\t\t\t<ns:PhoneNumber>15165234637</ns:PhoneNumber>\n\t\t\t\t</ns:Contact>\n\t\t\t\t<ns:Address>\n\t\t\t\t\t<ns:StreetLines>12000 Brunswick Ave</ns:StreetLines>\n\t\t\t\t\t<ns:City>Far Rockaway</ns:City>\n\t\t\t\t\t<ns:StateOrProvinceCode>NY</ns:StateOrProvinceCode>\n\t\t\t\t\t<ns:PostalCode>11691</ns:PostalCode>\n\t\t\t\t\t<ns:CountryCode>US</ns:CountryCode>\n\t\t\t\t\t<ns:Residential>0</ns:Residential>\n\t\t\t\t</ns:Address>\n\t\t\t</ns:Shipper>\n\t\t\t<ns:Recipient>\n\t\t\t\t<ns:Contact>\n\t\t\t\t\t<ns:PersonName>Nissim Barron</ns:PersonName>\n\t\t\t\t\t<ns:CompanyName></ns:CompanyName>\n\t\t\t\t\t<ns:PhoneNumber>3019439450</ns:PhoneNumber>\n\t\t\t\t\t<ns:EMailAddress>elyssalinn@gmail.com</ns:EMailAddress>\n\t\t\t\t</ns:Contact>\n\t\t\t\t<ns:Address>\n\t\t\t\t\t<ns:StreetLines>3333 shuki Hudson Parkway</ns:StreetLines>\n\t\t\t\t\t<ns:City>Bronx</ns:City>\n\t\t\t\t\t<ns:StateOrProvinceCode>NY</ns:StateOrProvinceCode>\n\t\t\t\t\t<ns:PostalCode>10463</ns:PostalCode>\n\t\t\t\t\t<ns:CountryCode>US</ns:CountryCode>\n\t\t\t\t\t<ns:Residential>1</ns:Residential>\n\t\t\t\t</ns:Address>\n\t\t\t</ns:Recipient>\n\t\t\t<ns:ShippingChargesPayment>\n\t\t\t\t<ns:PaymentType>SENDER</ns:PaymentType>\n\t\t\t\t<ns:Payor>\n\t\t\t\t\t<ns:ResponsibleParty>\n\t\t\t\t\t\t<ns:AccountNumber>510087640</ns:AccountNumber>\n\t\t\t\t\t\t<ns:Contact>\n\t\t\t\t\t\t\t<ns:PersonName>Avi Chinaman</ns:PersonName>\n\t\t\t\t\t\t\t<ns:CompanyName>4LOG LTD (jwg) C/O Freight Bro</ns:CompanyName>\n\t\t\t\t\t\t\t<ns:PhoneNumber>15165234637</ns:PhoneNumber>\n\t\t\t\t\t\t</ns:Contact>\n\t\t\t\t\t\t<ns:Address>\n\t\t\t\t\t\t\t<ns:StreetLines>12000 Brunswick Ave</ns:StreetLines>\n\t\t\t\t\t\t\t<ns:City>Far Rockaway</ns:City>\n\t\t\t\t\t\t\t<ns:StateOrProvinceCode>NY</ns:StateOrProvinceCode>\n\t\t\t\t\t\t\t<ns:PostalCode>11691</ns:PostalCode>\n\t\t\t\t\t\t\t<ns:CountryCode>US</ns:CountryCode>\n\t\t\t\t\t\t</ns:Address>\n\t\t\t\t\t</ns:ResponsibleParty>\n\t\t\t\t</ns:Payor>\n\t\t\t</ns:ShippingChargesPayment>\n\t\t\t<ns:PickupDetail>\n\t\t\t\t<ns:ReadyDateTime>2020-03-22T16:00:00</ns:ReadyDateTime>\n\t\t\t\t<ns:LatestPickupDateTime>2020-03-22T19:00:00</ns:LatestPickupDateTime>\n\t\t\t\t<ns:CourierInstructions>En Route to the USA</ns:CourierInstructions>\n\t\t\t\t<ns:RequestType>FUTURE_DAY</ns:RequestType>\n\t\t\t</ns:PickupDetail>\n\t\t\t<ns:SmartPostDetail>\n\t\t\t\t<ns:Indicia>PARCEL_SELECT</ns:Indicia>\n\t\t\t\t<ns:HubId>5531</ns:HubId>\n\t\t\t</ns:SmartPostDetail>\n\t\t\t<ns:LabelSpecification>\n\t\t\t\t<ns:LabelFormatType>COMMON2D</ns:LabelFormatType>\n\t\t\t\t<ns:ImageType>PDF</ns:ImageType>\n\t\t\t\t<ns:LabelStockType>STOCK_4X6</ns:LabelStockType>\n\t\t\t\t<ns:LabelOrder>SHIPPING_LABEL_FIRST</ns:LabelOrder>\n\t\t\t</ns:LabelSpecification>\n\t\t\t<ns:ShippingDocumentSpecification>\n\t\t\t\t<ns:ShippingDocumentTypes>COMMERCIAL_INVOICE</ns:ShippingDocumentTypes>\n\t\t\t\t<ns:CertificateOfOrigin>\n\t\t\t\t\t<ns:DocumentFormat>\n\t\t\t\t\t\t<ns:ImageType>PDF</ns:ImageType>\n\t\t\t\t\t\t<ns:StockType>PAPER_LETTER</ns:StockType>\n\t\t\t\t\t\t<ns:Localization>\n\t\t\t\t\t\t\t<ns:LanguageCode>EN</ns:LanguageCode>\n\t\t\t\t\t\t\t<ns:LocaleCode>US</ns:LocaleCode>\n\t\t\t\t\t\t</ns:Localization>\n\t\t\t\t\t</ns:DocumentFormat>\n\t\t\t\t</ns:CertificateOfOrigin>\n\t\t\t\t<ns:CommercialInvoiceDetail>\n\t\t\t\t\t<ns:Format>\n\t\t\t\t\t\t<ns:ImageType>PDF</ns:ImageType>\n\t\t\t\t\t\t<ns:StockType>PAPER_LETTER</ns:StockType>\n\t\t\t\t\t</ns:Format>\n\t\t\t\t</ns:CommercialInvoiceDetail>\n\t\t\t</ns:ShippingDocumentSpecification>\n\t\t\t<ns:RateRequestTypes>LIST</ns:RateRequestTypes>\n\t\t\t<ns:PackageCount>1</ns:PackageCount>\n\t\t\t<ns:RequestedPackageLineItems>\n\t\t\t\t<ns:Weight>\n\t\t\t\t\t<ns:Units>KG</ns:Units>\n\t\t\t\t\t<ns:Value>0.8</ns:Value>\n\t\t\t\t</ns:Weight>\n\t\t\t\t<ns:Dimensions>\n\t\t\t\t\t<ns:Length>16</ns:Length>\n\t\t\t\t\t<ns:Width>16</ns:Width>\n\t\t\t\t\t<ns:Height>3</ns:Height>\n\t\t\t\t\t<ns:Units>CM</ns:Units>\n\t\t\t\t</ns:Dimensions>\n\t\t\t\t<ns:CustomerReferences>\n\t\t\t\t\t<ns:CustomerReferenceType>CUSTOMER_REFERENCE</ns:CustomerReferenceType>\n\t\t\t\t\t<ns:Value>X1000491255</ns:Value>\n\t\t\t\t</ns:CustomerReferences>\n\t\t\t</ns:RequestedPackageLineItems>\n\t\t</ns:RequestedShipment>\n\t</ns:ProcessShipmentRequest>"
