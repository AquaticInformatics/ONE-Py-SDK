import requests
import json
from enterprise.authentication import AuthenticationApi
from shared.helpers.protobuf import DeserializeResponse


class CoreApi:
    def __init__(self, env, auth:AuthenticationApi):
        self.AppUrl = "/enterprise/core/v1/"
        self.Environment = env
        self.Authentication = auth
    
    