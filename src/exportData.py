from datetime import datetime, timezone
from clientsdk import ClientSdk
from shared.constants import Environment 
from shared.creds import userName, password

client =ClientSdk(Environment.get("feature"))
if (client.Authentication.GetToken(userName, password)):  # Supply username and password here
    print("Authenticated successfully")
else:
    print("Authentication failed")
plantId="d401d639-38d0-4625-b4ab-c505fe0f50f4"
startDate =datetime(2022,7,1,20,13,1,0,timezone.utc)
endDate =datetime(2022,7,16,20,13,1,0,timezone.utc)
client.Exporter.ExportWorksheet("ExportAllWSData.csv", plantId, startDate, endDate)
print(f"Completed export of all worksheet data from {startDate.date()} to {endDate.date()}")