import requests
import json
from logging import Logger
from one_py_sdk.shared.helpers.protobufhelper import DeserializeResponse
from one_py_sdk.shared.baseClasses import apibase

class ActivityApi(apibase("/common/activity/v1/")):
    def __init__(self, env, auth, session: requests.Session = None):
        self.AppUrl = "/common/activity/v1/"
        self.Environment = env
        self.Authentication = auth
        if not session:
            self.Session = requests.Session()
            self.Session.headers = {
                "Content-Type": "application/x-protobuf", "Accept": "application/x-protobuf"}
        else:
            self.Session = session

    def DeleteActivity(self, activityId, includeDescendants=True):
        url = f"{self.Environment}{self.AppUrl}{activityId}?includeDescendants={includeDescendants}"
        response = DeserializeResponse(self.Session.delete(url))
        if response.errors:
            return response
        return response.statusCode
