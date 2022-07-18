import csv
import json
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
           
    def ExportWorksheet(self, filename, plantId, startDate, endDate, wsType=None): 
        with open(filename, mode='w', newline='', encoding="utf-8") as file:        
            fieldnames = ['Worksheet Type', 'Time', 'ColumnName','ColumnId','RowNumber', 'Value', 'StringValue', 'DateEntered']                
            worksheetWriter =csv.DictWriter(file,fieldnames=fieldnames)
            worksheetWriter.writeheader()
            if not wsType:                    
                wsTypes = range(1,5)
                for wsType in wsTypes:
                    try: 
                         self.__mapAndWriteRowsAndColumns(worksheetWriter, plantId, wsType, startDate, endDate)                    
                    except:
                        print("error")
                        continue                    
            else:
                self.__mapAndWriteRowsAndColumns(worksheetWriter, plantId, wsType, startDate, endDate)                                           
    
    def __mapAndWriteRowsAndColumns(self, worksheetWriter, plantId, wsType, startDate, endDate):
        wsVal =self.ConvertWSTypeToStringValue(wsType)    
        print(wsVal)                
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
        print(rowValues)       
        
        rowDict ={}
        for num in rowNumbers:
            rowDict[num]= str(GetDateFromRowNumber(num, ws.enumWorksheet))
        
        numberMapping = {}
        for column in ws.columns:
            numberMapping[column.columnNumber] = [column.name, column.columnId]  
        for vals in rows.values():            
            for cell in vals.cells:                                                        
                try: 
                    worksheetWriter.writerow({'Worksheet Type': wsVal, 'Time': rowDict[vals.rowNumber],'ColumnName':numberMapping[cell.columnNumber][0],
                                              'ColumnId':numberMapping[cell.columnNumber][1],'Value': (cell.cellDatas[0].value.value),
                                            'RowNumber':vals.rowNumber, 'StringValue':cell.cellDatas[0].stringValue.value, 
                                            'DateEntered':cell.cellDatas[0].auditEvents[-1].timeStamp.jsonDateTime.value})
                except(IndexError):
                    print (IndexError)
                    pass
                                                                    
    def ExportWorksheetByType(self, filename, plantId, startDate, endDate, wsType=4):               
            wsVal =self.ConvertWSTypeToStringValue(wsType)  
            with open(filename, mode='w', newline='', encoding="utf-8") as file:        
                fieldnames = ['Worksheet Type', 'Time', 'ColumnName','ColumnId','RowNumber', 'Value', 'StringValue', 'DateEntered']                
                worksheetWriter =csv.DictWriter(file,fieldnames=fieldnames)
                worksheetWriter.writeheader()                                       
                self.__mapAndWriteRowsAndColumns(worksheetWriter, plantId, wsType, startDate, endDate)

    def ExportColumnDetails(self, filename, plantId, wsType =None):                    
        unitDict, paramDict = self.__mapUnitsAndParams()
        with open(filename, mode='w', newline='', encoding="utf-8") as file:
            fieldnames = ['Worksheet Type','ColumnNumber', 'Name', 'ParameterId', 'Path', 'ParameterTranslation','ColumnId','LocationId', 'UnitId', 'UnitName','UnitTranslation','LastPopulatedDate', 'Limits' ]        
            worksheetWriter =csv.DictWriter(file, fieldnames=fieldnames)
            worksheetWriter.writeheader()
            if not wsType:
                wsTypes = range(1,5)
                for wsType in wsTypes:
                    try:
                        self.__mapAndWriteColumns(plantId, wsType, unitDict, paramDict, worksheetWriter)
                    except: 
                        continue
            else: 
                self.__mapAndWriteColumns(plantId, wsType, unitDict, paramDict, worksheetWriter)
              
    
    def __mapAndWriteColumns(self, plantId, wsType, unitDict, paramDict, worksheetWriter):
        wsVal = self.ConvertWSTypeToStringValue(wsType)
        try:
            ws=self.Spreadsheet.GetWorksheetDefinition(plantId, wsType)[0]                              
        except:
            return print("No worksheet definition found")
        if not ws.columns:
            return print("No columns found")             
        
        columnDict = {}
        for column in ws.columns:                    
            columnDict[column.columnNumber] = [column.name,  column.columnId, column.parameterId,  column.displayUnitId, column.lastRowNumberWithData, column.locationId, column.limits]       
        limitDict ={}
        for column in columnDict.values():
            for limit in column[6]:
                limitDict[column[1]+limit.name]= [limit.name, limit.enumLimit, limit.lowValue.value, limit.highValue.value, limit.timeWindow.startTime.jsonDateTime.value, limit.timeWindow.endTime.jsonDateTime.value ]
                print(limitDict[column[1]+limit.name])
        twinDict =self.PathFinder(plantId, columnDict)
        for key in columnDict.keys():
                                
            worksheetWriter.writerow({ 'ColumnNumber': key, 'Name':columnDict[key][0], 'ColumnId': columnDict[key][1], 'Worksheet Type':wsVal,
                                        'ParameterId':columnDict[key][2],'UnitId': columnDict[key][3],  'LastPopulatedDate': GetDateFromRowNumber(columnDict[key][4], wsType),
                                        'UnitTranslation':unitDict[columnDict[key][3]][2],'LocationId':columnDict[key][5],
                                            'ParameterTranslation':paramDict[columnDict[key][2]][1], "Path": twinDict[columnDict[key][1]][2],
                                            'Limits' :  columnDict[key][6]                                             
                                        })
    def __mapUnitsAndParams(self):
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
        return unitDict, paramDict
    
    def ExportColumnDetailsByType(self, filename, plantId, wsType=4):         
        unitDict, paramDict = self.__mapUnitsAndParams()
        with open(filename, mode='w', newline='', encoding="utf-8") as file:
            fieldnames = ['Worksheet Type','ColumnNumber', 'Name', 'ParameterId', 'Path', 'ParameterTranslation','ColumnId','LocationId', 'UnitId', 'UnitName','UnitTranslation','LastPopulatedDate', 'Limits' ]        
            worksheetWriter =csv.DictWriter(file, fieldnames=fieldnames)
            worksheetWriter.writeheader()
            self.__mapAndWriteColumns(plantId, wsType, unitDict, paramDict, worksheetWriter)
                             
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
    
    def ConvertWSTypeToStringValue(self, wsType):
        if wsType ==1:
            return "Fifteen Minute"
        elif wsType ==2:
            return "Hourly"   
        elif wsType ==3:
            return "Four Hour"                                  
        elif wsType ==4:
            return "Daily"            
        else: 
             return print("Enter valid worksheet type value (1= Fifteen minute, 2=Hourly, 3=FourHour, 4=Daily)") 
                
   
          
            
        