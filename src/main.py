from datetime import datetime, timedelta, timezone
from clientsdk import ClientSdk
from shared.constants import Environment 
from shared.creds import userName, password


client =ClientSdk(Environment.get("feature"))
if (client.Authentication.GetToken(userName, password)):  # Supply username and password here
    print("Authenticated successfully")
else:
    print("Authentication failed")
print(client.Authentication.UserName)
print(client.Authentication.Token)
plantId="d401d639-38d0-4625-b4ab-c505fe0f50f4"
startDate =datetime(2022,7,1,20,13,1,0,timezone.utc)
endDate =datetime(2022,7,16,20,13,1,0,timezone.utc)
client.Exporter.ExportColumnDetails("ColumnInfoAll.csv", plantId)
print(f"Completed export of column information for all worksheet types for plant {plantId}")

client.Exporter.ExportColumnDetailsByType("ColumnInfoDaily.csv", plantId)
print(f"Completed export of column information for daily worksheets for plant {plantId}")

client.Exporter.ExportColumnDetailsByType("ColumnInfoFourHour.csv", plantId, 3)
print(f"Completed export of column information for four hour worksheets for plant {plantId}")

client.Exporter.ExportColumnDetailsByType("ColumnInfoHourly.csv", plantId, 2)
print(f"Completed export of column information for hourly worksheets for plant {plantId}")

client.Exporter.ExportColumnDetailsByType("ColumnInfo15M.csv", plantId, 1)
print(f"Completed export of column information for fifteen minute worksheets for plant {plantId}")

client.Exporter.ExportWorksheet("ExportWSData.csv", plantId, startDate, endDate)
print(f"Completed export of all worksheet data from {startDate.date()} to {endDate.date()}")

client.Exporter.ExportWorksheetByType("ExportFourHour.csv", plantId, startDate, endDate, 4)
print(f"Completed export of daily worksheet data from {startDate.date()} to {endDate.date()}")

client.Exporter.ExportWorksheetByType("ExportFourHour.csv", plantId, startDate, endDate, 3)
print(f"Completed export of four hour worksheet data from {startDate.date()} to {endDate.date()}")

client.Exporter.ExportWorksheetByType("ExportHourly.csv", plantId, startDate, endDate, 2)
print(f"Completed export of hourly worksheet data from {startDate.date()} to {endDate.date()}")

client.Exporter.ExportWorksheetByType("ExportFifteenMinute.csv", plantId, startDate, endDate, 1)
print(f"Completed export of fifteen minute worksheet data from {startDate.date()} to {endDate.date()}")