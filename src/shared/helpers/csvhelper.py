import csv
from one_interfaces import worksheet_definition_pb2 as wsDef
from one_interfaces import row_pb2 as Row
from operations.spreadsheet import SpreadsheetApi
from shared.helpers.datetimehelper import *
from datetime import datetime, timedelta
class Exporter:
    def __init__(self, env, auth):
        self.Environment = env
        self.Authentication = auth
        self.Spreadsheet = SpreadsheetApi(env, auth)
           
    def ExportWorksheet(self, filename, plantId, startDate, endDate):                   
            
            with open(filename, mode='w', newline='') as file:        
                fieldnames = ['Worksheet Type', 'Time', 'ColumnName','RowNumber', 'Value', 'StringValue', 'DateEntered']                
                worksheetWriter =csv.DictWriter(file,fieldnames=fieldnames)
                worksheetWriter.writeheader()
                wsTypes = range(1,5)
                for wsType in wsTypes:
                    if wsType ==1:
                        wsVal="Fifteen Minute"
                    elif wsType ==2:
                        wsVal="Hourly"   
                    elif wsType ==3:
                        wsVal="Four Hour"                                  
                    elif wsType == 4:
                        wsVal ="Daily"
                    wsd=self.Spreadsheet.GetWorksheetDefinition(plantId, wsType)                    
                    try:
                        ws=wsd[0] 
                    except:
                        continue
                    
                    if not ws.columns:
                        continue
                    rows =self.Spreadsheet.GetRowsForTimeRange(plantId, wsType, startDate, endDate)                                  
                    rowNumbers = rows.keys()
                    rowValues = rows.values()
                    rowValues
                    rowDict ={}
                    for num in rowNumbers:
                        rowDict[num]= str(GetDateFromRowNumber(num, ws.enumWorksheet))
                    columnNames = [col.name for col in ws.columns]
                    numberMapping = {}
                    for column in ws.columns:
                        numberMapping[column.columnNumber] = column.name  
                    for vals in rows.values():            
                        for cell in vals.cells:                        
                            try:                    
                                worksheetWriter.writerow({'Worksheet Type': wsVal, 'Time': rowDict[vals.rowNumber],'ColumnName':numberMapping[cell.columnNumber], 'Value': (cell.cellDatas[0].value.value),
                                                        'RowNumber':vals.rowNumber, 'StringValue':cell.cellDatas[0].stringValue.value, 
                                                        'DateEntered':cell.cellDatas[0].auditEvents[-1].timeStamp.jsonDateTime.value})
                            except(IndexError):
                                pass                                                                         

    def ExportColumnDetails(self, filename, plantId):               
        with open(filename, mode='w', newline='') as file:
            fieldnames = ['Worksheet Type','ColumnNumber', 'Name', 'ParameterId', 'ColumnId', 'UnitId', 'LastPopulatedRow' ]        
            worksheetWriter =csv.DictWriter(file, fieldnames=fieldnames)
            worksheetWriter.writeheader()
            wsTypes = range(1,5)
            for wsType in wsTypes:
                if wsType ==1:
                    wsVal="Fifteen Minute"
                elif wsType ==2:
                    wsVal="Hourly"   
                elif wsType ==3:
                    wsVal="Four Hour"                                  
                elif wsType == 4:
                    wsVal ="Daily"
                try:
                    ws=self.Spreadsheet.GetWorksheetDefinition(plantId, wsType)[0]                              
                except:
                    continue
                if not ws.columns:
                    continue
                numberMapping = {}
                for column in ws.columns:                    
                    numberMapping[column.columnNumber] = [column.name,  column.columnId, column.parameterId,  column.displayUnitId, column.lastRowNumberWithData]       
                
                for key in numberMapping.keys():
                    worksheetWriter.writerow({ 'ColumnNumber': key, 'Name':numberMapping[key][0], 'ColumnId': numberMapping[key][1], 'Worksheet Type':wsVal,
                                                'ParameterId':numberMapping[key][2],'UnitId': numberMapping[key][3],  'LastPopulatedRow': numberMapping[key][4]})