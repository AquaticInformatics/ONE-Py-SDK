import requests
from enterprise.authentication import AuthenticationApi
from shared.helpers.protobuf import DeserializeResponse


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
            