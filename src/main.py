from datetime import datetime, timedelta
from clientsdk import ClientSdk
from shared.constants import env 
from shared.creds import userName, password
from shared.helpers.csvhelper import *

client =ClientSdk(env.get("feature"))

if (client.Authentication.GetToken(userName, password)):  # Supply username and password here
    print("Authenticated successfully")
else:
    print("Authentication failed")
print(client.Authentication.UserName)
print(client.Authentication.Token)
plantId="d401d639-38d0-4625-b4ab-c505fe0f50f4"
startDate =datetime(2022,7,1,20,13,1,0,timezone.utc)
endDate =datetime.now(timezone.utc)
client.Exporter.ExportWorksheet("ExportWSTest.csv", plantId, startDate, endDate)
client.Exporter.ExportColumnDetails("ExportColumnsTest.csv", plantId)