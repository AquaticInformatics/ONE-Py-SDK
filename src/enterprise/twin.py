import requests
import json
from enterprise.authentication import AuthenticationApi
from shared.helpers.protobuf import DeserializeResponse


class DigitalTwinApi:
    def __init__(self, env, auth:AuthenticationApi):
        self.AppUrl = "/enterprise/twin/v1/"
        self.Environment = env
        self.Authentication = auth       
        
    def GetTwinByRefId(self, twinRefId):
        url = self.Environment+self.AppUrl+"DigitalTwin/Ref/"+twinRefId        
        headers = {'Authorization': self.Authentication.Token.access_token, "Accept": "application/x-protobuf"}
        response = DeserializeResponse(requests.get(url, headers=headers))        
        return response.content.DigitalTwins.items
    
    def GetTwinMeasurementsByRefId(self, twinRefId):
        url = self.Environment+self.AppUrl+"DigitalTwin/Ref/"+twinRefId        
        headers = {'Authorization': self.Authentication.Token.access_token, "Accept":"application/x-protobuf"}
        response = DeserializeResponse(requests.get(url, headers=headers))              
        return json.loads(response.content.DigitalTwins.items[0].twinData.value).get('measurement')      
    
    def TwinMeasurements(self, twinRefId, twinMeasurements):
        try:         
             usefulDictionary ={"Telemetry Id": twinRefId,
                            "Value": twinMeasurements['value'], 
                            "String Value": twinMeasurements['stringValue'],
                            "Timestamp": twinMeasurements['timestamp'].get('jsonDateTime'),
                            "TelemetryPath": self.findTelemetryPath(twinRefId)}
             return usefulDictionary
        except (TypeError):
             return ("No twin data found for "+twinRefId)       
        
    
    def GetDescendantsByRef(self, twinRefId:str):
        pass
    
    def findTelemetryPath(self, twinRefId):
        statusCode=""
        twinPath=[]        
        while (True):
            url = self.Environment+self.AppUrl+"DigitalTwin/Ref/"+str(twinRefId)                         
            headers = {'Authorization': self.Authentication.Token.access_token, "Accept":"application/x-protobuf"}
            response = DeserializeResponse(requests.get(url, headers=headers))
            if (response.statusCode!=200):
                break                                                                          
            twinRefId =response.content.DigitalTwins.items[0].parentTwinReferenceId.value            
            twinPath.append(response.content.DigitalTwins.items[0].name.value)            
        twinPathString=""
        while (len(twinPath)>0):
            twinPathString = twinPathString+str(twinPath.pop())+"/"
        return twinPathString
  
                
        

    
    