import requests
from operations.spreadsheet import SpreadsheetApi
from common.library import LibraryApi
from shared.constants import *
from datetime import time
import json
from enterprise.twin import DigitalTwinApi


from enterprise.authentication import AuthenticationApi

class ClientSdk:
	def __init__(self, env):
		self.Environment = env
		self.Initialize()
	
	def Initialize(self):
		self.Auth= AuthenticationApi(self.Environment)
		self.Twin = DigitalTwinApi(self.Environment, self.Auth)
		self.Spreadsheet = SpreadsheetApi(self.Environment, self.Auth)
		self.Library = LibraryApi(self.Environment, self.Auth)
  

  

	
 