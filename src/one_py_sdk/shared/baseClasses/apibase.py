import requests

class ApiBase:
    def __init__(self, env, auth, appUrl, session: requests.Session=None):
        self.AppUrl = appUrl
        self.Environment = env
        self.Authentication = auth
        if not session:
            self.Session = requests.Session()
            self.Session.headers = {"Content-Type": "application/x-protobuf", "Accept": "application/x-protobuf"}            
        else:
            self.Session = session
