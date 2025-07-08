from requests import Session
import json
from one_interfaces import report_definition_pb2 as report
import logging
from one_py_sdk.enterprise.authentication import AuthenticationApi
from one_py_sdk.shared.helpers.protobufhelper import DeserializeResponse
from one_py_sdk.shared.helpers.helpers import IsValidGuid


class ReportApi:
    def __init__(self, env, auth: AuthenticationApi, session: Session = None):
        self.AppUrl = "/enterprise/report/v1/"
        self.AppUrlV2 = "/enterprise/report/v2/"
        self.Environment = env
        self.Authentication = auth
        if not session:
            self.Session = Session()
            self.Session.headers = {
                "Content-Type": "application/x-protobuf", "Accept": "application/x-protobuf"}
        else:
            self.Session = session

    def GetReportDefinitionsV2(self, plantId=None):
        url = f'{self.Environment}{self.AppUrlV2}definitions'
        if plantId and IsValidGuid(plantId):
            url = url+f"?plantId={plantId}"
        response = DeserializeResponse(self.Session.get(url))
        print(response)
        if response.errors:
            return response
        return response.content.ReportDefinitions.items

    def GetReportDefinitions(self, plantId=None):
        url = f'{self.Environment}{self.AppUrl}definitions'
        if plantId and IsValidGuid(plantId):
            url = url+f"?plantId={plantId}"
        # url2 = f'{self.Environment}{self.AppUrlV2}definitions'
        # if plantId and IsValidGuid(plantId):
        #     url2 = url2+f"?plantId={plantId}"
        response = DeserializeResponse(self.Session.get(url))
        # response2 = DeserializeResponse(self.Session.get(url2))

        response.content.ReportDefinitions.items
        if response.errors:
            return response
        return response.content.ReportDefinitions.items

    def GetColumnIdsByPlant(self, plantId):
        if not plantId:
            return []
        if not IsValidGuid(plantId):
            return logging.error(f"{plantId} is not a valid guid")
        reports = self.GetReportDefinitions(plantId)
        try:
            reportDefs = [json.loads(report.reportDefinitionJson.value)
                          for report in reports]
        except:
            return reports
        columns = [d.get('columns') for d in reportDefs]
        ids = []
        for colLst in columns:
            for col in colLst:
                ids.append(col.get('id'))
        uniqueIds = []
        for id in ids:
            if id not in uniqueIds:
                uniqueIds.append(id)
        return uniqueIds

    def GetReportDefinitionById(self, reportId):
        if not reportId:
            return []
        if not IsValidGuid(reportId):
            return logging.error(f"{reportId} is not a valid guid")
        url = f'{self.Environment}{self.AppUrl}definitions/{reportId}'
        response = DeserializeResponse(self.Session.get(url))
        if response.errors:
            return response
        elif response.statusCode == 404:
            return response
        return response.content.ReportDefinitions.items

    def GetColumnIdsByReportId(self, reportId):
        if not IsValidGuid(reportId):
            return logging.error(f"{reportId} is not a valid guid")
        reports = self.GetReportDefinitionById(reportId)
        try:
            reportDefs = [json.loads(report.reportDefinitionJson.value)
                          for report in reports]
        except:
            return reports
        columns = [d.get('columns') for d in reportDefs]
        ids = []
        for colLst in columns:
            for col in colLst:
                ids.append(col.get('id'))
        return ids

    def GetColumnIdsByReportName(self, reportName, plantId=None):
        if not reportName:
            return []
        if not plantId or not IsValidGuid(plantId):
            logging.warning(
                f"PlantId :{plantId} was either not supplied or invalid. Column Ids associated with all reports this user has access to with this name will be returned.")
        reports = self.GetReportDefinitions(plantId)
        try:
            reportDefs = [json.loads(report.reportDefinitionJson.value)
                          for report in reports if report.name.value == reportName]
        except:
            return reports
        columns = [d.get('columns') for d in reportDefs]
        ids = []
        for colLst in columns:
            for col in colLst:
                ids.append(col.get('id'))
        return ids
