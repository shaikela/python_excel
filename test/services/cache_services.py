from convert import profile
import requests
import json

get_delivery_details_url="http://192.117.139.143:57772/rest/api/TRN/GetDeliveryDetails/"
get_delivery_url="http://192.117.139.143:57772/rest/api/Shipping1/GetDelivery/"
def get_delivery_id(so,vendor):
    get_delivery_details=get_delivery_details_url+so+'/'+vendor+'/0'
    response=requests.get(get_delivery_details)
    response_json=json.loads(response.text)
    if len(response_json['children'])>0:
        return str(response_json['children'][0]['DeliveryID'])+','+str(response_json['children'][0]['Awb'])
    else:
        return 0

def get_delivery_details(so,username):
    #verify profile of the user
    prof = profile()
    env=''
    if (username.find('Test')>0):
        env='t'
    else:
        env='p'
    user = prof.manageprofile(env, None, username)
    vendor = user.vendor
    get_delivery=get_delivery_details_url+so+'/'+vendor+'/0'
    response=requests.get(get_delivery)
    response_json=json.loads(response.text)
    if len(response_json['children'])>0:
        deliveryid=str(response_json['children'][0]['DeliveryID'])
        awb=str(response_json['children'][0]['Awb'])
        rtrn=deliveryid+','+awb
        return rtrn
    else:
        return 0