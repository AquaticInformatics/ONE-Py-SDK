import json
from ClientSdk import ClientSdk
from enterprise.twin import DigitalTwinApi
from shared.constants import env 
from enterprise.authentication import AuthenticationApi
import uuid

client =ClientSdk(env.get("feature"))
if (client.Authentication.getToken("dfeature", "Password3637**")): #Supply username and password here
    print("Authenticated successfully")
else:
    print("Authentication failed")
#print (client.Auth.getUserInfo())
client.DigitalTwins.getTwinMeasurementsByRefId("660b2705-11ea-42a2-a9c5-2c7fece821a4")
# ids =client.Spreadsheet.getColumnIdsForWorksheet("d401d639-38d0-4625-b4ab-c505fe0f50f4", 4) #Supply plant Id and WSStype here
# test = client.DigitalTwins.findTelemetryPath(ids[4])
# print(test)
# twinData = [print(client.DigitalTwins.getTwinMeasurementsByRefId(id)) for id in ids]
# paths = [client.Twin.findTelemetryPath(id) for id in ids]
# print(paths)
# twinData = [client.DigitalTwins.getTwinMeasurementsByRefId(id) for id in ids]
# print(twinData)
