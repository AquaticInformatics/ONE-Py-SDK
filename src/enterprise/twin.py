import requests
import json

class DigitalTwinApi:
    def __init__(self, env, auth):
        self.AppUrl = "/enterprise/twin/v1/"
        self.Environment = env
        self.Auth = auth       
        
    def getTwinByRefId(self, twinRefId):
        url = self.Environment+self.AppUrl+"DigitalTwin/Ref/"+twinRefId        
        headers = {'Authorization': self.Auth.Token}
        response = requests.get(url, headers=headers )
        jResponse = json.loads(response.content)
        return jResponse
    
    def getTwinMeasurementsByRefId(self, twinRefId):
        url = self.Environment+self.AppUrl+"DigitalTwin/Ref/"+twinRefId        
        headers = {'Authorization': self.Auth.Token}
        response = requests.get(url, headers=headers )
        jResponse = json.loads(response.content)
        twinData= jResponse['content'].get('digitalTwins').get('items')[0].get('twinData')
        twinData2=json.loads(twinData)
        try: 
            twinMeasurements =twinData2.get('measurement')
            usefulDictionary ={"Telemetry Id": twinRefId,
                           "Value": twinMeasurements['value'], 
                           "String Value": twinMeasurements['stringValue'],
                           "Timestamp": twinMeasurements['timestamp'].get('jsonDateTime')}
                           #"TelemetryPath": self.findTelemetryPath(twinRefId)}
        except (TypeError):
            return ("No twin data found for "+twinRefId)       
        return usefulDictionary
    
    def getDescendantsByRef(self, twinRefId:str):
        pass
    
    def findTelemetryPath(self, twinRefId):
        statusCode=""
        twinPath=[]
        while (True):
            url = self.Environment+self.AppUrl+"DigitalTwin/Ref/"+twinRefId                
            headers = {'Authorization': self.Auth.Token, "Accept": "application/json"}
            response = requests.get(url, headers=headers )            
            if (response.status_code==403):
                break                        
            jResponse = json.loads(response.content)
            twinRefId=jResponse['content'].get('digitalTwins').get('items')[0].get('parentTwinReferenceId')
            twinPath.append(jResponse['content'].get('digitalTwins').get('items')[0].get('name'))           
        twinPathString=""
        while (len(twinPath)>0):
            twinPathString = twinPathString+twinPath.pop()+"/"
        return twinPathString
  
                
        

    
    