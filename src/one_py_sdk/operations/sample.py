from collections import OrderedDict
from datetime import datetime

from requests import Session
from one_py_sdk.enterprise.authentication import AuthenticationApi
from one_py_sdk.shared.helpers.protobufhelper import DeserializeResponse
from one_py_sdk.shared.helpers.datetimehelper import *

class SampleApi:
    def __init__(self, env: str, auth: AuthenticationApi, session: Session = None):
        self.Environment = env
        self.Auth = auth
        self.AppUrl = "/operations/sample/v1/"
        if not session:
            self.Session = Session()
            self.Session.headers = {
                "Content-Type": "application/x-protobuf", "Accept": "application/x-protobuf"}
        else:
            self.Session = session

    def DeleteImportProfile(self, profileId):
        url = f'{self.Environment}{self.AppUrl}importProfile/{profileId}'
        response = DeserializeResponse(self.Session.delete(url))
        return response
