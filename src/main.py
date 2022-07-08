import json
from clientsdk import ClientSdk
from enterprise.twin import DigitalTwinApi
from shared.constants import env 
from enterprise.authentication import AuthenticationApi
import uuid
from shared.creds import *

client =ClientSdk(env.get("feature"))
if (client.Authentication.GetToken(userName, password)): #Supply username and password here
    print("Authenticated successfully")
else:
    print("Authentication failed")
client.Authentication.UserName
print(client.Authentication.Token)
print (client.Authentication.GetUserInfo())

# ids =client.Spreadsheet.GetColumnIdsForWorksheet("", 4) #Supply plant Id and WSStype here
# test = client.DigitalTwin.findTelemetryPath(ids[4])
# print(test)
# twinDatas = [client.DigitalTwin.GetTwinMeasurementsByRefId(id) for id in ids]
# print(twinDatas)
# paths = [client.DigitalTwin.findTelemetryPath(id) for id in ids]
# print(paths)

