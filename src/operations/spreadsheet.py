from datetime import datetime
import uuid
import requests
from enterprise.authentication import AuthenticationApi
from shared.helpers.protobufhelper import DeserializeResponse
from shared.helpers.datetimehelper import *

class SpreadsheetApi:
    def __init__(self, env: str, auth: AuthenticationApi):
        self.Environment = env
        self.Auth = auth
        self.AppUrl ="/operations/spreadsheet/v1/"
    
    def GetWorksheetColumnIds(self, plantId, wsType):
        url = self.Environment + self.AppUrl + plantId + "/worksheet/"+str(wsType)+"/definition"
        headers = {'Authorization': self.Auth.Token.access_token, "Accept":"application/x-protobuf"}
        response =DeserializeResponse(requests.get(url, headers=headers))   
        if response.errors:            
            return response     
        columnIds = [col.columnId for col in response.content.worksheetDefinitions.items[0].columns if  col.isActive==True]        
        return columnIds
    
    def GetWorksheetColumnNumbers(self, plantId, wsType):
        url = self.Environment + self.AppUrl + plantId + "/worksheet/"+str(wsType)+"/definition"
        headers = {'Authorization': self.Auth.Token.access_token, "Accept":"application/x-protobuf"}
        response =DeserializeResponse(requests.get(url, headers=headers)) 
        if response.errors:            
            return response       
        columnNumbers = [col.columnNumber for col in response.content.worksheetDefinitions.items[0].columns if  col.isActive==True]                
        return columnNumbers
    
    def GetWorksheetDefinition(self, plantId, wsType):
        url = self.Environment + self.AppUrl + plantId + "/worksheet/"+str(wsType)+"/definition"
        headers = {'Authorization': self.Auth.Token.access_token, "Accept":"application/x-protobuf"}
        response =DeserializeResponse(requests.get(url, headers=headers))    
        if response.errors:            
            return response           
        return response.content.worksheetDefinitions.items
    
    def GetSpreadsheetDefinition(self, plantId):
        url = f'{self.Environment}{self.AppUrl}{plantId}/definition'
        headers = {'Authorization': self.Auth.Token.access_token, "Accept":"application/x-protobuf"}
        response =DeserializeResponse(requests.get(url, headers=headers))               
        return response.content.spreadsheetDefinitions.items
    
    def GetColumnByDay(self, plantId, wsType, columnId, date:datetime):
        url = self.Environment + self.AppUrl + plantId + f'/worksheet/{str(wsType)}/column/{columnId}/byday/{date.year}/{date.month}/{date.day}'        
        headers = {'Authorization': self.Auth.Token.access_token, "Accept":"application/x-protobuf"}       
        response =DeserializeResponse(requests.get(url, headers=headers))          
        if response.errors:            
            return response
        return response.content.measurements.items   
    
    def GetColumnByMonth(self, plantId:str, wsType:int, columnId:int, date:datetime):
        url = self.Environment + self.AppUrl + plantId + f'/worksheet/{str(wsType)}/column/{columnId}/bymonth/{date.year}/{date.month}'        
        headers = {'Authorization': self.Auth.Token.access_token, "Accept":"application/x-protobuf"}
        response =DeserializeResponse(requests.get(url, headers=headers))  
        if response.errors:            
            return response
        return response.content.measurements.items  
    
    def GetColumnByYear(self, plantId, wsType, columnId, date:datetime):
        url = self.Environment + self.AppUrl + plantId + f'/worksheet/{str(wsType)}/column/{columnId}/byyear/{date.year}'        
        headers = {'Authorization': self.Auth.Token.access_token, "Accept":"application/x-protobuf"}
        response =DeserializeResponse(requests.get(url, headers=headers))  
        if response.errors:            
            return response
        return response.content.measurements.items  
            
    def GetRows(self, plantId, wsType, startRow=None, endRow=None, columns=None, viewId=None):
        if columns and viewId:
            return print("Using both columns and viewId parameters together is not supported.")
        requestId = uuid.uuid4()
        url=f'{self.Environment}{self.AppUrl}{plantId}/worksheet/{str(wsType)}/rows?requestId={requestId}'
        if startRow:
            url=url+f'&startRow={startRow}'
        if endRow:
            url=url+f'&endRow={endRow}'
        if columns:
            url=url+f'&columns={columns}'
        if viewId:
            url=url+f'&viewId={viewId}'        
        headers = {'Authorization': self.Auth.Token.access_token, "Accept":"application/x-protobuf"}
        response =DeserializeResponse(requests.get(url, headers=headers)) 
        if response.errors:            
            return response
        return response.content.rows.items
    
    def GetRowsByDay(self, plantId, wsType, date:datetime, columns=None, viewId=None):
        if columns and viewId:
            return print("Using both columns and viewId parameters together is not supported.")
        url = self.Environment + self.AppUrl +f'{plantId}/worksheet/{str(wsType)}/rows/byday/{date.year}/{date.month}/{date.day}'  
        headers = {'Authorization': self.Auth.Token.access_token, "Accept":"application/x-protobuf"}
        response =DeserializeResponse(requests.get(url, headers=headers)) 
        if response.errors:            
            return response
        return response.content.rows.items
    
    def GetRowsByMonth(self, plantId, wsType, date:datetime, columns=None, viewId=None):
        if columns and viewId:
            return print("Using both columns and viewId parameters together is not supported.")
        url = self.Environment + self.AppUrl +f'{plantId}/worksheet/{str(wsType)}/rows/bymonth/{date.year}/{date.month}'  
        headers = {'Authorization': self.Auth.Token.access_token, "Accept":"application/x-protobuf"}
        response =DeserializeResponse(requests.get(url, headers=headers)) 
        if response.errors:            
            return response
        return response.content.rows.items
    
    def GetRowsForTimeRange(self, plantId, wsType, startDate:datetime, endDate:datetime):
        startRow =GetRowNumber(startDate, wsType)
        endRow =GetRowNumber(endDate, wsType)
        return self.GetRows(plantId, wsType, startRow, endRow)