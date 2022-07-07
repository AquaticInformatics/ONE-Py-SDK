import requests
from Operations.Spreadsheet import SpreadsheetApi
from Common.Library import LibraryApi
from Shared.Constants import *
from datetime import time
import json
from Enterprise.Twin  import DigitalTwinApi


from Enterprise.Authentication import AuthenticationApi

class ClientSdk:
	def __init__(self, env):
		self.Environment = env
		self.Initialize()
	
	def Initialize(self):
		self.Authentication= AuthenticationApi(self.Environment)
		self.DigitalTwins = DigitalTwinApi(self.Environment, self.Authentication)
		self.Spreadsheet = SpreadsheetApi(self.Environment, self.Authentication)
		self.Library = LibraryApi(self.Environment, self.Authentication)
  

  

	
 