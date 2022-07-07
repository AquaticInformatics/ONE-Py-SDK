import json
from clientsdk import ClientSdk
from enterprise.twin import DigitalTwinApi
from shared.constants import env 
from enterprise.authentication import AuthenticationApi
import uuid

client =ClientSdk(env.get("feature"))
if (client.Authentication.GetToken("", "")): #Supply username and password here
    print("Authenticated successfully")
else:
    print("Authentication failed")
print (client.Authentication.GetUserInfo())
client.DigitalTwin.getTwinMeasurementsByRefId("")
ids =client.Spreadsheet.getColumnIdsForWorksheet("", 4) #Supply plant Id and WSStype here
test = client.DigitalTwin.findTelemetryPath(ids[4])
print(test)
twinDatas = [client.DigitalTwin.getTwinMeasurementsByRefId(id) for id in ids]
print(twinDatas)
paths = [client.DigitalTwin.findTelemetryPath(id) for id in ids]
print(paths)

