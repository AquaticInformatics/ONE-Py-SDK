import requests
import json
from enterprise.authentication import AuthenticationApi

class SpreadsheetApi:
    def __init__(self, env: str, auth: AuthenticationApi):
        self.Environment = env
        self.auth = auth
        self.appUrl ="/operations/spreadsheet/v1/"
    
    def getColumnIdsForWorksheet(self, plantId, wsType):
        url = self.Environment + self.appUrl + plantId + "/worksheet/"+str(wsType)+"/definition"
        headers = {'Authorization': self.auth.Token}
        response = requests.get(url, headers=headers)
        jResponse = json.loads(response.content)
        #print(jResponse['content'].get('worksheetDefinitions').get('items')[0].get('columns')[0])
        columnIds = [col.get('columnId') for col in jResponse['content'].get('worksheetDefinitions').get('items')[0].get('columns') if  col.get('isActive')==True]     
        return columnIds
            