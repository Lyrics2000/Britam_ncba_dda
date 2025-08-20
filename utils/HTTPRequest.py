import requests
from urllib.parse import urlencode
import logging
import json
from home.models import (    AuthToken
)
# import timezoen
from django.utils import timezone
from requests.auth import HTTPBasicAuth
logger = logging.getLogger(__name__)
from utils.logs import (
    make_api_request_log_request
)
from config.settings import (
    USERNAME,   
    PASSWORD,
    APIS
)
import json

class HTTPRequest:
    def __init__(self,base_url):
        self.base_url = base_url

    def login(self):
        """
        Perform a login request to the API.
        """
        # first check if auth token exists and is valid
        try:
            auth_token = AuthToken.objects.latest('created_at')
            if auth_token.expires_at > timezone.now():
                return {
                    "status": 200,
                    "data": {
                        "access_token": auth_token.token
                    }
                } 
        except AuthToken.DoesNotExist:
            logger.info("No valid auth token found, proceeding with login.")
            url = f"{APIS['BASE_URL']}{APIS['LOGIN']}"
            payload = {
                "username": USERNAME,
                "password": PASSWORD
            }
            headers = {
            'Content-Type': 'application/json'
            }
   
            response = requests.post(url, json=payload, headers=headers, verify=False, timeout=20)
            if response.status_code == 200:
                data = response.json()
                access_token = data.get("access_token")
                if access_token:
                    # Save the token to the database
                    # delete all previous tokens
                    AuthToken.objects.all().delete()
                    AuthToken.objects.create(token=access_token, expires_at= data.get("expires_at"))
                    return {
                        "status": 200,
                        "data": {
                            "access_token": access_token
                        }
                    }
                else:
                    logger.error("Access token not found in login response.")
                    return {
                        "status": 400,
                        "message": "Access token not found in login response."
                    }
            else:
                logger.error(f"Login failed with status code {response.status_code}.")
                return {
                    "status": response.status_code,
                    "message": "Login failed."
                }
        
        
       

        
        
        

    def is_connection_live(self):
        try:
            response = requests.get(self.base_url,verify=False,timeout=20)
            js_data  =  response.text
      
            return True
        except requests.exceptions.RequestException as e:
            logger.error(f"The http error is {e}")
            return False
 
    def send_get_with_body(self,url,data,role,request):

    
        logger.info("The url is {endpoint}")
        dddata = {
                            "role": role,
                            "successfull": True,
                            "message": f"Began processing request with Body {data}",
                            "endpoint": url
                        }
        kk = make_api_request_log_request(request,dddata)

        logger.info(f"The data sent is {data}")
        if not self.is_connection_live():
            logger.info("Connection is not live.")
            print("Connection is not live.")
            dddata = {
                            "role": role,
                            "successfull": False,
                            "message": f"The connection is not LIVE",
                            "endpoint": url
                        }
            kk = make_api_request_log_request(request,dddata)
            return None
        
        login =  self.login()
        # this noe returns a dict with status and data
        if login['status'] != 200:
            logger.error("Login failed, cannot proceed with request.")
            return None
        logger.info(f"Login successful, proceeding with request to {url}")
   
        response = login.json()
        access_token = response.get("data", {}).get("access_token", None)
        if not access_token:
            logger.error("Access token not found in login response.")
            return None 
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {access_token}'
        }
        payload =  None
       

        url = url

        payload = json.dumps(data)
        

        response = requests.request("GET", url, headers=headers, data=payload,verify=False,timeout=20)
        try:
            dddata = {
                            "role": role,
                            "successfull": True,
                            "message": f"The response was successfull",
                            "endpoint": url
                        }
            kk = make_api_request_log_request(request,dddata)
            logger.info(f"the post response is {response.json()}")
        except:
            dddata = {
                            "role": role,
                            "successfull": False,
                            "message": f"The response was not successfull",
                            "endpoint": url
                        }
            kk = make_api_request_log_request(request,dddata)
            logger.info(f"the post response is {response.text}")
        return response


    def send_get_request(self, url,body=None, params=None, headers=None,role= None,request = None,fileType = None):
        logger.info(f"The url is {url}")
        dddata = {
                            "role": role,
                            "successfull": True,
                            "message": f"Began Proccessing request",
                            "endpoint": url
                        }
        kk = make_api_request_log_request(request,dddata)

        logger.info(f"The data sent is {body}")
        if not self.is_connection_live():
            logger.info("Connection is not live.")
            print("Connection is not live.")
            dddata = {
                            "role": role,
                            "successfull": True,
                            "message": f"The connection is not Live",
                            "endpoint": url
                        }
            kk = make_api_request_log_request(request,dddata)
            return None
        login =  self.login()
        if login['status'] != 200:  
            logger.error("Login failed, cannot proceed with request.")
            return None
        logger.info(f"Login successful, proceeding with request to {url}")
        response = login.json()
        access_token = response.get("data", {}).get("access_token", None)
        if not access_token:
            logger.error("Access token not found in login response.")
            return None
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {access_token}',
            'FileType': fileType if fileType else 'application/json'
        }
        payload =  None

        if body:
            payload = json.dumps(body)

        logger.info(f"The payload is : {payload} ")
        url1 =  None
        if None in [params]:
            url1 = self.base_url + url
        else:
            url1 = self.base_url + url + "?" + urlencode(params, safe='" ')
        logger.info(f"The get url is {url1}")
        logger.info(f"the query params are {params}")
        response = requests.get(url1,data=payload,headers=headers,verify=False,timeout=20)
        try:
            dddata = {
                            "role": role,
                            "successfull": True,
                            "message": f"The response was successfull",
                            "endpoint": url
                        }
            kk = make_api_request_log_request(request,dddata)
            logger.info(f"the post response is {response.json()}")
        except:
            dddata = {
                            "role": role,
                            "successfull": False,
                            "message": f"The response was not successfull",
                            "endpoint": url
                        }
            kk = make_api_request_log_request(request,dddata)
            logger.info(f"the post response is {response.text}")
        return response
    
    
    def send_put_request(self, url,body=None, params=None, headers=None,role=None,request=None,fileType=None):
        logger.info(f"The url is {url}")
        dddata = {
                            "role": role,
                            "successfull": True,
                            "message": f"Began Proccessing Request",
                            "endpoint": url
                        }
        kk = make_api_request_log_request(request,dddata)

        logger.info(f"The data sent is {body}")
        if not self.is_connection_live():
            logger.info("Connection is not live.")
            print("Connection is not live.")
            dddata = {
                            "role": role,
                            "successfull": True,
                            "message": f"Connection Is not Live",
                            "endpoint": url
                        }
            kk = make_api_request_log_request(request,dddata)
            return None
        login =  self.login()
        if login['status'] != 200:
            logger.error("Login failed, cannot proceed with request.")
            return None
        logger.info(f"Login successful, proceeding with request to {url}")
        response = login.json()
        access_token = response.get("data", {}).get("access_token", None)
        if not access_token:
            logger.error("Access token not found in login response.")
            return None
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {access_token}',
            'FileType': fileType if fileType else 'application/json'
        }
        payload =  None

        if body:
            payload = json.dumps(body)

        logger.info(f"The payload is : {payload} ")
       
        url1 = self.base_url + url + "?" + urlencode(params, safe='" ')
        logger.info(f"The get url is {url1}")
        logger.info(f"the query params are {params}")
        response = requests.put(url1,data=payload,headers=headers,verify=False,timeout=20)
        try:
            dddata = {
                            "role": role,
                            "successfull": True,
                            "message": f"The response was successfull",
                            "endpoint": url
                        }
            kk = make_api_request_log_request(request,dddata)
            logger.info(f"the post response is {response.json()}")
        except:
            dddata = {
                            "role": role,
                            "successfull": False,
                            "message": f"The response was not successfull",
                            "endpoint": url
                        }
            kk = make_api_request_log_request(request,dddata)
            logger.info(f"the post response is {response.text}")
        return response
    
    def send_post_request(self, url, params=None, data=None,role=None,request = None, fileType=None):
        logger.info("The url is {endpoint}")
        dddata = {
                            "role": role,
                            "successfull": True,
                            "message": f"Began processing successful",
                            "endpoint": url
                        }
        kk = make_api_request_log_request(request,dddata)
        if not self.is_connection_live():
            logger.info("Connection is not live.")
            print("Connection is not live.")
            dddata = {
                            "role": role,
                            "successfull": False,
                            "message": f"Connection is Not Live",
                            "endpoint": url
                        }
            kk = make_api_request_log_request(request,dddata)
            return None
        login =  self.login()
        if login['status'] != 200:   
            logger.error("Login failed, cannot proceed with request.")
            return None
        logger.info(f"Login successful, proceeding with request to {url}")
        response = login.json()
        access_token = response.get("data", {}).get("access_token", None)
        if not access_token:
            logger.error("Access token not found in login response.")
            return None
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {access_token}',
            'FileType': fileType if fileType else 'application/json'
        }
        logger.info(f"the request data is {data}")
        
        url = self.base_url + url
        
        print("the url is ", url)
        logger.info(f"the data us {data}")
        payload = json.dumps(data)
       

        response = requests.request("POST", url, headers=headers, data=payload,verify=False,timeout=20)

        try:
            dddata = {
                            "role": role,
                            "successfull": True,
                            "message": f"Response was successfull",
                            "endpoint": url
                        }
            kk = make_api_request_log_request(request,dddata)
            logger.info(f"the post response is {response.json()}")
        except:
            dddata = {
                            "role": role,
                            "successfull": False,
                            "message": f"Response was Not successfull",
                            "endpoint": url
                        }
            kk = make_api_request_log_request(request,dddata)
            logger.info(f"the post response is {response.text}")
        return response

      