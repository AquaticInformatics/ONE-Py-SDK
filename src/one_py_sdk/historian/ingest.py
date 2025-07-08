from datetime import datetime
import requests
import json
from one_py_sdk.enterprise.authentication import AuthenticationApi
from one_py_sdk.shared.helpers.protobufhelper import DeserializeResponse



class IngestApi:
    def __init__(self, env, auth: AuthenticationApi, session: requests.Session=None):
        self.Environment = env
        self.Authentication = auth
        self.AppUrl = "/historian/ingest/v1/"
        if not session:
            self.Session = requests.Session()
            self.Session.headers = {"Content-Type": "application/x-protobuf", "Accept": "application/x-protobuf"}            
        else:
            self.Session = session
            
    def DeleteDataSource(self, sourceId, serviceId):
        url = f'{self.Environment}{self.AppUrl}/{serviceId}/datasource/{sourceId}'
        response = DeserializeResponse(self.Session.delete(url))
        return response