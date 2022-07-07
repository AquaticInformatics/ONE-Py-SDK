import requests
from Operations.Spreadsheet import SpreadsheetApi
from Common.Library import LibraryApi
from Enterprise.Twin  import DigitalTwinApi
from Shared.Constants import *
from datetime import time
import json



from Enterprise.Authentication import AuthenticationApi

class ClientSdk:
	def __init__(self, env):
		self.Environment = env
		self.Initialize()
	
	def Initialize(self):
		self.Authentication= AuthenticationApi(self.Environment)
		self.DigitalTwin = DigitalTwinApi(self.Environment, self.Authentication)
		self.Spreadsheet = SpreadsheetApi(self.Environment, self.Authentication)
		self.Library = LibraryApi(self.Environment, self.Authentication)
  

  

	
 