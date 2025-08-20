
from django.http import JsonResponse

import requests
import logging
from config.settings import (
    AZURE_BASE_URL
)
logger = logging.getLogger(__name__)

class MicrosoftValidation:
    def __init__(self,request):
        print(request.META)
        self.sub_key = request.META.get('HTTP_OCP_APIM_SUBSCRIPTION_KEY', None)
        self.token = request.META.get('HTTP_AUTHORIZATION', None)
        self.baseUrl = AZURE_BASE_URL


        
    def verify(self):
        
        if None in [self.sub_key, self.token]:
            return  {"status":False,
                     "message": "fill all required headeer"
                     }
                              
                            
        url = f"{self.baseUrl}/api/auth/verify/"
        
        headers = {
            'Ocp-Apim-Subscription-Key': self.sub_key,
            'Authorization': f'{self.token}'
            }

        response = requests.get(url, headers=headers,verify=False)
        
        
        # print("the response is that ", response.text)
        # logger.error(f"the response is that {response.text} -  {response.status_code}")
        print("the response is that ", response.json(), response.status_code)
        logger.error(f"the response is that {response.json()} -  {response.status_code}")
        if response.status_code ==  401:
            return {
                "status":False,
                "message":response.json()['description'],
                "data":response.json(),
                "api_status":response.status_code
            }
        
        else:
        
            return {
                "status":True,
                "message":"Authorized",
                "data":response.json(),
                "api_status":response.status_code
            }
       