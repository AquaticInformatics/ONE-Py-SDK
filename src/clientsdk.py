import requests
from enterprise.core import CoreApi
from historian.data import HistorianAPI
from operations.spreadsheet import SpreadsheetApi
from common.library import LibraryApi
from enterprise.twin  import DigitalTwinApi
from shared.constants import *
from datetime import time
import json


from enterprise.authentication import AuthenticationApi
from shared.helpers.csvhelper import Exporter

class ClientSdk:
	def __init__(self, env):
		self.Environment = env
		self.Initialize()
	
	def Initialize(self):
		self.Authentication= AuthenticationApi(self.Environment)
		self.DigitalTwin = DigitalTwinApi(self.Environment, self.Authentication)
		self.Spreadsheet = SpreadsheetApi(self.Environment, self.Authentication)
		self.Library = LibraryApi(self.Environment, self.Authentication)
		self.Core = CoreApi(self.Environment, self.Authentication)
		self.Historian = HistorianAPI(self.Environment, self.Authentication)
		self.Exporter = Exporter(self.Environment, self.Authentication)
	
	def LoadCurrentUser(self):
		if not self.Authentication.IsAuthenticated:
			print("Not authenticated. Authenticate and try again")
		if(self.Authentication.User.id != None):
			self.Authentication.GetUserInfo()
			self.Authentication.User.CopyFrom(self.Core.GetUser(self.Authentication.User.id))


  

	
 