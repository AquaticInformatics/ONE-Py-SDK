import requests
import json

from datetime import time

class AuthenticationApi:
	def __init__(self, env):
		self.Environment =env
		self.Token=""

	def getToken(self, user, password):
		data ={'username': user, 'password':password, 'grant_type':'password', 'scope':'FFAccessAPI openid', 'client_id':'VSTestClient', 'client_secret':'0CCBB786-9412-4088-BC16-78D3A10158B7'}
		headers = {'Accept': 'application/json', 'Content-Type': 'application/x-www-form-urlencoded'}
		url = self.Environment+"/connect/token"
		response= requests.post(url, headers=headers, data=data)
		if (response.status_code !=200):
			return False#, "Authentication failed."+" "+str(json.loads(response.content))
		responseJson=json.loads(response.content)
		self.User =user
		self.Password = password
		self.Token = "Bearer "+ responseJson['access_token']
		return True#, "Successfully authenticated, token value is :" +responseJson['access_token']+ " and can be accessed looking using the client's Auth.Token field"
