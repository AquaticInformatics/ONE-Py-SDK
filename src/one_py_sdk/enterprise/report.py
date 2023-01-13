import requests
import json
import logging
from one_py_sdk.enterprise.authentication import AuthenticationApi
from one_py_sdk.shared.helpers.protobufhelper import DeserializeResponse

class ReportApi:
    def __init__(self, env, auth: AuthenticationApi):
        self.AppUrl = "/enterprise/report/v1/"
        self.Environment = env
        self.Authentication = auth
        
    def GetReportDefinitions(self, plantId=None):
        url = f'{self.Environment}{self.AppUrl}definitions'
        if plantId:
            url= url+f"?plantId={plantId}"
        headers = {'Authorization': self.Authentication.Token.access_token,
                   "Accept": "application/x-protobuf"}
        response = DeserializeResponse(requests.get(url, headers=headers))
        if response.errors:
            return response
        return response.content.ReportDefinitions.items
    
    def GetColumnIdsByPlant(self, plantId):        
        reportDefs = [json.loads(report.reportDefinitionJson.value) for report in self.GetReportDefinitions(plantId)]
        columns = [d.get('columns') for d in reportDefs]
        ids =[]
        for colLst in columns:
            for col in colLst:
                ids.append(col.get('id'))
        uniqueIds =[]
        for id in ids:
            if id not in uniqueIds:
                uniqueIds.append(id)
        return uniqueIds
    
    def GetReportDefinitionById(self, reportId):
        url = f'{self.Environment}{self.AppUrl}definitions/{reportId}'
        headers = {'Authorization': self.Authentication.Token.access_token,
                   "Accept": "application/x-protobuf"}
        response = DeserializeResponse(requests.get(url, headers=headers))
        if response.errors:
            return response
        return response.content.ReportDefinitions.items
    
    def GetColumnIdsByReportId(self, reportId):        
        reportDefs = [json.loads(report.reportDefinitionJson.value) for report  in self.GetReportDefinitionById(reportId)]
        columns = [d.get('columns') for d in reportDefs]
        ids =[]
        for colLst in columns:
            for col in colLst:
                ids.append(col.get('id'))     
        return ids
    
    def GetColumnIdsByReportName(self, reportName, plantId =None):
        try:
            reportDefs = [json.loads(report.reportDefinitionJson.value) for report  in self.GetReportDefinitions(plantId) if report.name.value== reportName]           
        except:           
            return None
        columns = [d.get('columns') for d in reportDefs]
        ids =[]
        for colLst in columns:
            for col in colLst:
                ids.append(col.get('id'))     
        return ids
