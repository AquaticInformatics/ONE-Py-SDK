import requests
import json
from datetime import datetime, time, timedelta
from shared.helpers.protobuf import DeserializeResponse
from one_interfaces import user_pb2 as User
import google
 
class AuthenticationApi:
	def __init__(self, env):
		self.Environment = env
		self.Token = Token()
		self.UserName = ""
		self.Password = ""
		self.User:User =User.User()
		self.IsAuthenticated =False
	         

	def GetToken(self, user, password):
		data ={'username': user, 'password':password, 'grant_type':'password', 'scope':'FFAccessAPI openid', 'client_id':'VSTestClient', 'client_secret':'0CCBB786-9412-4088-BC16-78D3A10158B7'}
		headers = {'Accept': 'application/json', 'Content-Type': 'application/x-www-form-urlencoded'}
		url = self.Environment+"/connect/token"
		response= requests.post(url, headers=headers, data=data)
		if (response.status_code !=200):
			return False
		token = Token()
		token.created =datetime.now() 				
		responseJson=json.loads(response.content)
		self.IsAuthenticated= True
		self.UserName =user
		self.Password = password
		token.token_type = responseJson['token_type']
		token.scope = responseJson['scope']
		token.access_token = token.token_type+" "+ responseJson['access_token']		
		token.expires_in =token.created +timedelta(seconds = responseJson['expires_in'])
		self.Token =token  		
		return True

	def GetUserInfo(self):
		headers = {'Accept': 'application/json', "Authorization": self.Token.access_token}
		url = self.Environment+"/connect/userinfo"
		response= requests.get(url, headers=headers)
		print(response.content)
		user = User.User()
		jResponse = json.loads(response.content)	
		#user.firstName.value=jResponse.get('givenName')

		#self.User.CopyFrom(response.content.Users.items[0])

		return response.content

class Token:
    def __init__(self):
        self.access_token:str 
        self.expires_in:float
        self.token_type:str
        self.scope:str
        self.created:datetime
    def __repr__(self):
        return "Access token: %s, Created on: %s, Expires in: %s, Token Type: %s, Scope: %s  " %(self.access_token, self.created, self.expires_in, self.token_type, self.scope)