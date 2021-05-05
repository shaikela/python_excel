import requests
import os
from pathlib import Path
import json
import base64


url = "http://xpit.4log.com/Magicxpi4.7/MgWebRequester.dll?appname=IFSFourLog_Listener&prgname=HTTP&arguments=-ADelivery%23InterActive"
script_dir = Path(os.path.dirname(__file__)) 
resource_path=os.path.join(Path(os.path.dirname(__file__)),'resources')    

def create_delivery(request,outdir):
        root_key= list(request.keys())[0]
        result={}.fromkeys(['Action','Order Number','Status','Delivery Id','Tracking'])
        try:
                so= request[root_key]['s']['OrderNumber']
                result['Order Number']=so
        except:
                result['Status']="Invalid request"
                return result

        if root_key=='CreateDelivery':
                result['Action']='Create Delivery'
        elif root_key=='CreateShipment':
                result['Action']='Create Shipment'
        else:
                result['Status']="Unknown action type"
                return result
        headers = {
        'Content-Type': 'application/json'
        }
        response = requests.request("POST", url, headers=headers, json = request)
        # check status
        if response.status_code!=200:
            result['Status']="No response from server"
            return result
        #  save response
        with open(os.path.join(outdir,so+"_"+result['Action']+"_response.json"),"w") as out:
                out.write(response.text)
        
        try:
                response_json=response.json()
                response_string=list(response_json.keys())[0]

                # with open(os.path.join(resource_path,'sample','s_response.json')) as response_sample:
                #         response_json=json.loads(response_sample.read())

                result['Status']=response_json[response_string]['StatusMessage']
                if result['Status']=='OK':
                        result['Delivery Id']=response_json[response_string]['Fourlogref']
                        # result['Order Number']=response_json[response_string]['OrderNumber'] # base so on request
                        if root_key=='CreateShipment':
                                result['Tracking']=response_json[response_string]['TrackingNumber']
                                blob=response_json["CreateShipmentResponse"]["base64label"]
                                decoded_blob=base64.b64decode(blob)
                                with open(os.path.join(outdir,so+".pdf"),"wb") as pdf_file:
                                        pdf_file.write(decoded_blob)
                # os.system("start "+outdir+"\\"+so+".pdf")
        
        except:         
            result['Status']='Unknown error reading response'
        
        return result

        # print(response.text)
        # print("response time:"+str(response.elapsed.seconds))
        # with open(os.path.join(outdir,so+"_response_"+action+".json"),"r") as jf:
                # response_blob=jf.read()
        # responseJson=json.loads(response_blob)
def manual_payload():
        action=input('action:')
        env=input('env:')
        filename='new_listener_c'+action+'_'+env+'.json'
        with open(os.path.join(resource_path,filename)) as resource_file:
                        request=resource_file.read()
        return request

