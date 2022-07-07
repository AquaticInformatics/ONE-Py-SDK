from one_interfaces import *
from one_interfaces import apiresponse_pb2 as apiResponse

def DeserializeResponse(response):        
      pbResponse = apiResponse.ApiResponse()         
      pbResponse.ParseFromString(response.content)                 
      return pbResponse
    
      
    