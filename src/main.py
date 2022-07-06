import json
from clientSDK import ClientSdk
from enterprise.twin import DigitalTwinApi
from shared.constants import env 
from enterprise.authentication import AuthenticationApi

print(env.get("feature"))
client =ClientSdk(env.get("feature"))
print(client.Auth.getToken("", "")) #Supply username and password here


ids =client.Spreadsheet.getColumnIdsForWorksheet("", 4) #Supply plant Id and WSStype here
print(ids)
paths = [client.Twin.findTelemetryPath(id) for id in ids]
print(paths)
twinData = [client.Twin.getTwinMeasurementsByRefId(id) for id in ids]
print(twinData)
