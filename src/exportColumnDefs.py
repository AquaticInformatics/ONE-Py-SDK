from datetime import datetime, timedelta
from clientsdk import ClientSdk
from shared.constants import Environment 
from shared.creds import userName, password
from shared.helpers.csvhelper import *

client =ClientSdk()
if (client.Authentication.GetToken(userName, password)):  # Supply username and password here
    print("Authenticated successfully")
else:
    print("Authentication failed")
plantId="d401d639-38d0-4625-b4ab-c505fe0f50f4"
client.Exporter.ExportColumnDetails("ExportAllColumnInfo.csv", plantId)
print(f"Completed export of column information for all worksheet types for plant {plantId}")