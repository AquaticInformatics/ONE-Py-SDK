import requests
import json
from enterprise.authentication import AuthenticationApi
from Shared.Helpers.ProtobufHelper import DeserializeResponse


class CoreApi:
    def __init__(self, env, auth:AuthenticationApi):
        self.AppUrl = "/enterprise/core/v1/"
        self.Environment = env
        self.Auth = auth
    
    