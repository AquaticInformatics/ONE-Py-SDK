import datetime
from uuid import uuid4

class DataPoint:
    def __init__(self, stringValue: str, columnId, note: str ="", auditUserId:uuid4 ="", auditTimeStamp: datetime ="", isLocked: bool =False):
        self.stringValue = stringValue
        self.columnId = columnId
        self.note = note
        self.auditUserId = auditUserId
        self.auditTimeStamp = auditTimeStamp
        self.isLocked =isLocked
        
        
