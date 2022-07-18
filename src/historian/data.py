from datetime import datetime
import requests
import json
from enterprise.authentication import AuthenticationApi
from shared.helpers.protobufhelper import DeserializeResponse
from one_interfaces import historian_data_pb2 as Historian 

class HistorianApi:
    def __init__(self, env, auth:AuthenticationApi):
        self.Environment =env
        self.Authentication = auth
        self.AppUrl = "/historian/data/v1/"
        
    def GetHistorianData(self, twinRefId, date:datetime):
        url=f'{self.Environment}{self.AppUrl}{twinRefId}/{date}'
        headers = {'Authorization': self.Authentication.Token.access_token, "Accept":"application/x-protobuf"}
        print(url)
        response = DeserializeResponse(requests.get(url, headers=headers))
        return response.content.historianDatas.items
    
    def GetHistorianDataRange(self, twinRefId, startTime:datetime, endTime: datetime):        
        url=f'{self.Environment}{self.AppUrl}{twinRefId}?startTime={startTime}&endTime={endTime}'
        print(url)
        headers = {'Authorization': self.Authentication.Token.access_token, "Accept":"application/x-protobuf"}
        response = DeserializeResponse(requests.get(url, headers=headers))
        return response.content.historianDatas.items
    
        