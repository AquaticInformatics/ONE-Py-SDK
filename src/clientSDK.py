import requests
from operations.spreadsheet import SpreadsheetApi
from common.library import LibraryApi
from enterprise.twin  import DigitalTwinApi
from shared.constants import *
from datetime import time
import json



from enterprise.authentication import AuthenticationApi

class ClientSdk:
	def __init__(self, env):
		self.Environment = env
		self.Initialize()
	
	def Initialize(self):
		self.Authentication= AuthenticationApi(self.Environment)
		self.DigitalTwin = DigitalTwinApi(self.Environment, self.Authentication)
		self.Spreadsheet = SpreadsheetApi(self.Environment, self.Authentication)
		self.Library = LibraryApi(self.Environment, self.Authentication)
  

  

	
 