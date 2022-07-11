from datetime import datetime
import requests
from enterprise.authentication import AuthenticationApi
from shared.helpers.protobufhelper import DeserializeResponse


class SpreadsheetApi:
    def __init__(self, env: str, auth: AuthenticationApi):
        self.Environment = env
        self.Auth = auth
        self.AppUrl ="/operations/spreadsheet/v1/"
    
    def GetColumnIdsForWorksheet(self, plantId, wsType):
        url = self.Environment + self.AppUrl + plantId + "/worksheet/"+str(wsType)+"/definition"
        headers = {'Authorization': self.Auth.Token.access_token, "Accept":"application/x-protobuf"}
        response =DeserializeResponse(requests.get(url, headers=headers))        
        columnIds = [col.columnId for col in response.content.worksheetDefinitions.items[0].columns if  col.isActive==True]        
        return columnIds
    
    def GetWorksheet(self, plantId, wsType):
        url = self.Environment + self.AppUrl + plantId + "/worksheet/"+str(wsType)+"/definition"
        headers = {'Authorization': self.Auth.Token.access_token, "Accept":"application/x-protobuf"}
        response =DeserializeResponse(requests.get(url, headers=headers))               
        return response.content.worksheetDefinitions.items
    
    def GetColumnByDay(self, plantId, wsType, columnId, date:datetime):
        url = self.Environment + self.AppUrl + plantId + f'/worksheet/{str(wsType)}/column/{columnId}/byday/{date.year}/{date.month}/{date.day}'
        print(url)
        headers = {'Authorization': self.Auth.Token.access_token, "Accept":"application/x-protobuf"}
        response =DeserializeResponse(requests.get(url, headers=headers))  
        print(response.content)  
        return response.content   
    
    def GetColumnByMonth(self, plantId, wsType, columnId, date:datetime):
        url = self.Environment + self.AppUrl + plantId + f'/worksheet/{str(wsType)}/column/{columnId}/bymonth/{date.year}/{date.month}'
        print(url)
        headers = {'Authorization': self.Auth.Token.access_token, "Accept":"application/x-protobuf"}
        response =DeserializeResponse(requests.get(url, headers=headers))  
        print(response.content)  
        return response.content
    
    def GetColumnByYear(self, plantId, wsType, columnId, date:datetime):
        url = self.Environment + self.AppUrl + plantId + f'/worksheet/{str(wsType)}/column/{columnId}/byyear/{date.year}'
        print(url)
        headers = {'Authorization': self.Auth.Token.access_token, "Accept":"application/x-protobuf"}
        response =DeserializeResponse(requests.get(url, headers=headers))  
        print(response.content)  
        return response.content
            