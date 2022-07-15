import csv
import json
from one_interfaces import worksheet_definition_pb2 as wsDef
from one_interfaces import row_pb2 as Row
from operations.spreadsheet import SpreadsheetApi
from common.library import LibraryApi
from enterprise.twin import DigitalTwinApi
from shared.helpers.datetimehelper import *
from datetime import datetime, timedelta
class Exporter:
    def __init__(self, env, auth):
        self.Environment = env
        self.Authentication = auth
        self.Spreadsheet = SpreadsheetApi(env, auth)
        self.Library = LibraryApi(env, auth)
        self.DigitalTwin = DigitalTwinApi(env, auth)
           
    def ExportWorksheet(self, filename, plantId, startDate, endDate):               
            with open(filename, mode='w', newline='') as file:        
                fieldnames = ['Worksheet Type', 'Time', 'ColumnName','ColumnId','RowNumber', 'Value', 'StringValue', 'DateEntered']                
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
                    try:
                        ws=self.Spreadsheet.GetWorksheetDefinition(plantId, wsType)[0]                  
                    except:
                        continue                    
                    if not ws.columns:
                        continue
                    rows =self.Spreadsheet.GetRowsForTimeRange(plantId, wsType, startDate, endDate)
                    try:
                        rowNumbers = rows.keys()
                        rowValues = rows.values()  
                    except(AttributeError):
                        continue            
                    
                    rowDict ={}
                    for num in rowNumbers:
                        rowDict[num]= str(GetDateFromRowNumber(num, ws.enumWorksheet))
                    columnNames = [col.name for col in ws.columns]
                    numberMapping = {}
                    for column in ws.columns:
                        numberMapping[column.columnNumber] = [column.name, column.columnId]  
                    for vals in rows.values():            
                        for cell in vals.cells:                        
                            try:                    
                                worksheetWriter.writerow({'Worksheet Type': wsVal, 'Time': rowDict[vals.rowNumber],'ColumnName':numberMapping[cell.columnNumber][0], 'ColumnId':numberMapping[cell.columnNumber][1],'Value': (cell.cellDatas[0].value.value),
                                                        'RowNumber':vals.rowNumber, 'StringValue':cell.cellDatas[0].stringValue.value, 
                                                        'DateEntered':cell.cellDatas[0].auditEvents[-1].timeStamp.jsonDateTime.value})
                            except(IndexError):
                                pass                                                                         

    def ExportWorksheetByType(self, filename, plantId, startDate, endDate, wsType=4):               
            if wsType ==1:
                    wsVal="Fifteen Minute"
            elif wsType ==2:
                wsVal="Hourly"   
            elif wsType ==3:
                wsVal="Four Hour"                                  
            elif wsType == 4:
                wsVal ="Daily" 
            else:
                return print("Enter valid worksheet type value (1= Fifteen minute, 2=Hourly, 3=FourHour, 4=Daily)")   
            with open(filename, mode='w', newline='') as file:        
                fieldnames = ['Worksheet Type', 'Time', 'ColumnName','ColumnId','RowNumber', 'Value', 'StringValue', 'DateEntered']                
                worksheetWriter =csv.DictWriter(file,fieldnames=fieldnames)
                worksheetWriter.writeheader()
            
                            
                try:
                    ws=self.Spreadsheet.GetWorksheetDefinition(plantId, wsType)[0]                  
                except:
                    return print("No worksheet definition found")
                if not ws.columns:
                    return print("No columns found")
                rows =self.Spreadsheet.GetRowsForTimeRange(plantId, wsType, startDate, endDate)
                try:
                    rowNumbers = rows.keys()
                    rowValues = rows.values()  
                except(AttributeError):
                    return print("No rows found")            
                
                rowDict ={}
                for num in rowNumbers:
                    rowDict[num]= str(GetDateFromRowNumber(num, ws.enumWorksheet))
                columnNames = [col.name for col in ws.columns]
                numberMapping = {}
                for column in ws.columns:
                    numberMapping[column.columnNumber] = [column.name, column.columnId]
                for vals in rows.values():            
                    for cell in vals.cells:                        
                        try:                    
                            worksheetWriter.writerow({'Worksheet Type': wsVal, 'Time': rowDict[vals.rowNumber],'ColumnName':numberMapping[cell.columnNumber][0],  'ColumnId':numberMapping[cell.columnNumber][1], 'Value': (cell.cellDatas[0].value.value),
                                                    'RowNumber':vals.rowNumber, 'StringValue':cell.cellDatas[0].stringValue.value, 
                                                    'DateEntered':cell.cellDatas[0].auditEvents[-1].timeStamp.jsonDateTime.value})
                        except(IndexError):
                            pass                                                                         

    def ExportColumnDetails(self, filename, plantId): 
        units = self.Library.GetUnits()  
        parameters = self.Library.GetParameters()       
        i18N = self.Library.Geti18nKeys("AQI_FOUNDATION_LIBRARY")[0].get("AQI_FOUNDATION_LIBRARY")
        i18NUnits= i18N.get("UnitType").get("LONG")
        i18NParams= i18N.get("Parameter").get("LONG")  
     
        paramDict = {}
        for param in parameters:
            try:
                paramDict[param.IntId]= [param.i18nKey, i18NParams[param.i18nKey]]
            except: 
                paramDict[param.IntId]= [param.i18nKey, None]                     
        unitDict = {}
        for unit in units:
            try:
                unitDict[unit.IntId]= [unit.i18nKey, unit.unitName, i18NUnits[unit.i18nKey]]
            except:
                unitDict[unit.IntId]= [unit.i18nKey, unit.unitName, None]           
        
        with open(filename, mode='w', newline='') as file:
            fieldnames = ['Worksheet Type','ColumnNumber', 'Name', 'ParameterId', 'ParameterI18NKey', 'Path', 'ParameterTranslation','ColumnId', 'UnitId', 'UnitName', 'UnitI18NKey','UnitTranslation','LastPopulatedRow' ]        
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
                elif wsType ==4:
                    wsVal ="Daily"
                try:
                    ws=self.Spreadsheet.GetWorksheetDefinition(plantId, wsType)[0]                              
                except:
                    continue
                if not ws.columns:
                    continue                
                columnDict = {}
                for column in ws.columns:                    
                    columnDict[column.columnNumber] = [column.name,  column.columnId, column.parameterId,  column.displayUnitId, column.lastRowNumberWithData]       
                twinDict =self.PathFinder(plantId, columnDict)
                for key in columnDict.keys():                    
                    worksheetWriter.writerow({ 'ColumnNumber': key, 'Name':columnDict[key][0], 'ColumnId': columnDict[key][1], 'Worksheet Type':wsVal,
                                                'ParameterId':columnDict[key][2],'UnitId': columnDict[key][3],  'LastPopulatedRow': columnDict[key][4],
                                                'UnitName': unitDict[columnDict[key][3]][1], "UnitI18NKey":unitDict[columnDict[key][3]][0],'UnitTranslation':unitDict[columnDict[key][3]][2],
                                                'ParameterI18NKey': paramDict[columnDict[key][2]][0], 'ParameterTranslation':paramDict[columnDict[key][2]][1], "Path": twinDict[columnDict[key][1]][2]                                               
                                                })
    
    def ExportColumnDetailsByType(self, filename, plantId, wsType=4):         
        if wsType ==1:
            wsVal="Fifteen Minute"
        elif wsType ==2:
            wsVal="Hourly"   
        elif wsType ==3:
            wsVal="Four Hour"                                  
        elif wsType ==4:
            wsVal ="Daily"
        else: 
             return print("Enter valid worksheet type value (1= Fifteen minute, 2=Hourly, 3=FourHour, 4=Daily)") 
        try:
            ws=self.Spreadsheet.GetWorksheetDefinition(plantId, wsType)[0]                              
        except:
            return print("No worksheet definition found")
        if not ws.columns:
            return print("No columns found")             
        columnDict = {}
        for column in ws.columns:                    
            columnDict[column.columnNumber] = [column.name,  column.columnId, column.parameterId,  column.displayUnitId, column.lastRowNumberWithData]       
        twinDict =self.PathFinder(plantId, columnDict)
        units = self.Library.GetUnits()  
        parameters = self.Library.GetParameters()       
        i18N = self.Library.Geti18nKeys("AQI_FOUNDATION_LIBRARY")[0].get("AQI_FOUNDATION_LIBRARY")
        i18NUnits= i18N.get("UnitType").get("LONG")
        i18NParams= i18N.get("Parameter").get("LONG")  
     
        paramDict = {}
        for param in parameters:
            try:
                paramDict[param.IntId]= [param.i18nKey, i18NParams[param.i18nKey]]
            except: 
                paramDict[param.IntId]= [param.i18nKey, None]                     
        unitDict = {}
        for unit in units:
            try:
                unitDict[unit.IntId]= [unit.i18nKey, unit.unitName, i18NUnits[unit.i18nKey]]
            except:
                unitDict[unit.IntId]= [unit.i18nKey, unit.unitName, None]           
        
        with open(filename, mode='w', newline='') as file:
            fieldnames = ['Worksheet Type','ColumnNumber', 'Name', 'ParameterId', 'ParameterI18NKey', 'Path', 'ParameterTranslation','ColumnId', 'UnitId', 'UnitName', 'UnitI18NKey','UnitTranslation','LastPopulatedRow' ]        
            worksheetWriter =csv.DictWriter(file, fieldnames=fieldnames)
            worksheetWriter.writeheader()        
            for key in columnDict.keys():                    
                worksheetWriter.writerow({ 'ColumnNumber': key, 'Name':columnDict[key][0], 'ColumnId': columnDict[key][1], 'Worksheet Type':wsVal,
                                            'ParameterId':columnDict[key][2],'UnitId': columnDict[key][3],  'LastPopulatedRow': columnDict[key][4],
                                            'UnitName': unitDict[columnDict[key][3]][1], "UnitI18NKey":unitDict[columnDict[key][3]][0],'UnitTranslation':unitDict[columnDict[key][3]][2],
                                            'ParameterI18NKey': paramDict[columnDict[key][2]][0], 'ParameterTranslation':paramDict[columnDict[key][2]][1], "Path": twinDict[columnDict[key][1]][2]                                               
                                            })
    
    
    def PathFinder(self, plantId, columnDict):
        twins = self.DigitalTwin.GetDescendants(plantId)
        twinDict ={}
        for twin in twins:
            twinDict[twin.twinReferenceId.value]=[twin.parentTwinReferenceId.value, twin.name.value, None]                
        for key in columnDict.keys():
            twinId=columnDict[key][1]
            path =[]
            pathString=""
            while (twinId!=plantId):             
                path.append(twinDict[twinId][1])
                twinId =twinDict[twinId][0]                                
            path.append(twinDict[twinId][1])
            while (path):
                pathString= f'{pathString}/{path.pop()}'
            twinDict[columnDict[key][1]][2]=pathString
        return twinDict
                
                
            
        
            
        