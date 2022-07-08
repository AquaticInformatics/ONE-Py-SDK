import requests
import json
from logging import Logger


class LibraryApi:
    def __init__(self, env, auth):
        self.appUrl = "/common/library/v1"
        self.environment = env
        self.auth = auth
    
    def getUnit(self, unitId):
        pass
    
    def getParameter(self, parameterId):
        pass
    
    def getParameters(self):
        pass