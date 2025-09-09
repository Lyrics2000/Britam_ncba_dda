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

# class HTTPRequest:
#     def __init__(self,base_url):
#         self.base_url = base_url

#     def login(self):
#         """
#         Perform a login request to the API.
#         """
#         # first check if auth token exists and is valid
#         try:
#             auth_token = AuthToken.objects.latest('created_at')
#             if auth_token.expires_at > timezone.now():
#                 return {
#                     "status": 200,
#                     "data": {
#                         "access_token": auth_token.token
#                     }
#                 } 
#         except AuthToken.DoesNotExist:
#             logger.info("No valid auth token found, proceeding with login.")
#             url = f"{APIS['BASE_URL']}{APIS['LOGIN']}"
#             payload = {
#                 "username": USERNAME,
#                 "password": PASSWORD
#             }
#             headers = {
#             'Content-Type': 'application/json'
#             }
   
#             response = requests.post(url, json=payload, headers=headers, verify=False, timeout=20)
#             if response.status_code == 200:
#                 data = response.json()
#                 access_token = data.get("access_token")
#                 if access_token:
#                     # Save the token to the database
#                     # delete all previous tokens
#                     AuthToken.objects.all().delete()
#                     AuthToken.objects.create(token=access_token, expires_at= data.get("expires_at"))
#                     return {
#                         "status": 200,
#                         "data": {
#                             "access_token": access_token
#                         }
#                     }
#                 else:
#                     logger.error("Access token not found in login response.")
#                     return {
#                         "status": 400,
#                         "message": "Access token not found in login response."
#                     }
#             else:
#                 logger.error(f"Login failed with status code {response.status_code}.")
#                 return {
#                     "status": response.status_code,
#                     "message": "Login failed."
#                 }
        
        
       

        
        
        

#     def is_connection_live(self):
#         try:
#             response = requests.get(self.base_url,verify=False,timeout=20)
#             js_data  =  response.text
      
#             return True
#         except requests.exceptions.RequestException as e:
#             logger.error(f"The http error is {e}")
#             return False
 
#     def send_get_with_body(self,url,data,role,request):

    
#         logger.info("The url is {endpoint}")
#         dddata = {
#                             "role": role,
#                             "successfull": True,
#                             "message": f"Began processing request with Body {data}",
#                             "endpoint": url
#                         }
#         kk = make_api_request_log_request(request,dddata)

#         logger.info(f"The data sent is {data}")
#         if not self.is_connection_live():
#             logger.info("Connection is not live.")
#             print("Connection is not live.")
#             dddata = {
#                             "role": role,
#                             "successfull": False,
#                             "message": f"The connection is not LIVE",
#                             "endpoint": url
#                         }
#             kk = make_api_request_log_request(request,dddata)
#             return None
        
#         login =  self.login()
#         # this noe returns a dict with status and data
#         if login['status'] != 200:
#             logger.error("Login failed, cannot proceed with request.")
#             return None
#         logger.info(f"Login successful, proceeding with request to {url}")
   
#         response = login.json()
#         access_token = response.get("data", {}).get("access_token", None)
#         if not access_token:
#             logger.error("Access token not found in login response.")
#             return None 
#         headers = {
#             'Content-Type': 'application/json',
#             'Authorization': f'Bearer {access_token}'
#         }
#         payload =  None
       

#         url = url

#         payload = json.dumps(data)
        

#         response = requests.request("GET", url, headers=headers, data=payload,verify=False,timeout=20)
#         try:
#             dddata = {
#                             "role": role,
#                             "successfull": True,
#                             "message": f"The response was successfull",
#                             "endpoint": url
#                         }
#             kk = make_api_request_log_request(request,dddata)
#             logger.info(f"the post response is {response.json()}")
#         except:
#             dddata = {
#                             "role": role,
#                             "successfull": False,
#                             "message": f"The response was not successfull",
#                             "endpoint": url
#                         }
#             kk = make_api_request_log_request(request,dddata)
#             logger.info(f"the post response is {response.text}")
#         return response


#     def send_get_request(self, url,body=None, params=None, headers=None,role= None,request = None,fileType = None):
#         logger.info(f"The url is {url}")
#         dddata = {
#                             "role": role,
#                             "successfull": True,
#                             "message": f"Began Proccessing request",
#                             "endpoint": url
#                         }
#         kk = make_api_request_log_request(request,dddata)

#         logger.info(f"The data sent is {body}")
#         if not self.is_connection_live():
#             logger.info("Connection is not live.")
#             print("Connection is not live.")
#             dddata = {
#                             "role": role,
#                             "successfull": True,
#                             "message": f"The connection is not Live",
#                             "endpoint": url
#                         }
#             kk = make_api_request_log_request(request,dddata)
#             return None
#         login =  self.login()
#         if login['status'] != 200:  
#             logger.error("Login failed, cannot proceed with request.")
#             return None
#         logger.info(f"Login successful, proceeding with request to {url}")
#         response = login.json()
#         access_token = response.get("data", {}).get("access_token", None)
#         if not access_token:
#             logger.error("Access token not found in login response.")
#             return None
#         headers = {
#             'Content-Type': 'application/json',
#             'Authorization': f'Bearer {access_token}',
#             'FileType': fileType if fileType else 'application/json'
#         }
#         payload =  None

#         if body:
#             payload = json.dumps(body)

#         logger.info(f"The payload is : {payload} ")
#         url1 =  None
#         if None in [params]:
#             url1 = self.base_url + url
#         else:
#             url1 = self.base_url + url + "?" + urlencode(params, safe='" ')
#         logger.info(f"The get url is {url1}")
#         logger.info(f"the query params are {params}")
#         response = requests.get(url1,data=payload,headers=headers,verify=False,timeout=20)
#         try:
#             dddata = {
#                             "role": role,
#                             "successfull": True,
#                             "message": f"The response was successfull",
#                             "endpoint": url
#                         }
#             kk = make_api_request_log_request(request,dddata)
#             logger.info(f"the post response is {response.json()}")
#         except:
#             dddata = {
#                             "role": role,
#                             "successfull": False,
#                             "message": f"The response was not successfull",
#                             "endpoint": url
#                         }
#             kk = make_api_request_log_request(request,dddata)
#             logger.info(f"the post response is {response.text}")
#         return response
    
    
#     def send_put_request(self, url,body=None, params=None, headers=None,role=None,request=None,fileType=None):
#         logger.info(f"The url is {url}")
#         dddata = {
#                             "role": role,
#                             "successfull": True,
#                             "message": f"Began Proccessing Request",
#                             "endpoint": url
#                         }
#         kk = make_api_request_log_request(request,dddata)

#         logger.info(f"The data sent is {body}")
#         if not self.is_connection_live():
#             logger.info("Connection is not live.")
#             print("Connection is not live.")
#             dddata = {
#                             "role": role,
#                             "successfull": True,
#                             "message": f"Connection Is not Live",
#                             "endpoint": url
#                         }
#             kk = make_api_request_log_request(request,dddata)
#             return None
#         login =  self.login()
#         if login['status'] != 200:
#             logger.error("Login failed, cannot proceed with request.")
#             return None
#         logger.info(f"Login successful, proceeding with request to {url}")
#         response = login.json()
#         access_token = response.get("data", {}).get("access_token", None)
#         if not access_token:
#             logger.error("Access token not found in login response.")
#             return None
#         headers = {
#             'Content-Type': 'application/json',
#             'Authorization': f'Bearer {access_token}',
#             'FileType': fileType if fileType else 'application/json'
#         }
#         payload =  None

#         if body:
#             payload = json.dumps(body)

#         logger.info(f"The payload is : {payload} ")
       
#         url1 = self.base_url + url + "?" + urlencode(params, safe='" ')
#         logger.info(f"The get url is {url1}")
#         logger.info(f"the query params are {params}")
#         response = requests.put(url1,data=payload,headers=headers,verify=False,timeout=20)
#         try:
#             dddata = {
#                             "role": role,
#                             "successfull": True,
#                             "message": f"The response was successfull",
#                             "endpoint": url
#                         }
#             kk = make_api_request_log_request(request,dddata)
#             logger.info(f"the post response is {response.json()}")
#         except:
#             dddata = {
#                             "role": role,
#                             "successfull": False,
#                             "message": f"The response was not successfull",
#                             "endpoint": url
#                         }
#             kk = make_api_request_log_request(request,dddata)
#             logger.info(f"the post response is {response.text}")
#         return response
    
#     def send_post_request(self, url, params=None, data=None,role=None,request = None, fileType=None):
#         logger.info("The url is {endpoint}")
#         dddata = {
#                             "role": role,
#                             "successfull": True,
#                             "message": f"Began processing successful",
#                             "endpoint": url
#                         }
#         kk = make_api_request_log_request(request,dddata)
#         if not self.is_connection_live():
#             logger.info("Connection is not live.")
#             print("Connection is not live.")
#             dddata = {
#                             "role": role,
#                             "successfull": False,
#                             "message": f"Connection is Not Live",
#                             "endpoint": url
#                         }
#             kk = make_api_request_log_request(request,dddata)
#             return None
#         login =  self.login()
#         if login['status'] != 200:   
#             logger.error("Login failed, cannot proceed with request.")
#             return None
#         logger.info(f"Login successful, proceeding with request to {url}")
#         response = login.json()
#         access_token = response.get("data", {}).get("access_token", None)
#         if not access_token:
#             logger.error("Access token not found in login response.")
#             return None
#         headers = {
#             'Content-Type': 'application/json',
#             'Authorization': f'Bearer {access_token}',
#             'FileType': fileType if fileType else 'application/json'
#         }
#         logger.info(f"the request data is {data}")
        
#         url = self.base_url + url
        
#         print("the url is ", url)
#         logger.info(f"the data us {data}")
#         payload = json.dumps(data)
       

#         response = requests.request("POST", url, headers=headers, data=payload,verify=False,timeout=20)

#         try:
#             dddata = {
#                             "role": role,
#                             "successfull": True,
#                             "message": f"Response was successfull",
#                             "endpoint": url
#                         }
#             kk = make_api_request_log_request(request,dddata)
#             logger.info(f"the post response is {response.json()}")
#         except:
#             dddata = {
#                             "role": role,
#                             "successfull": False,
#                             "message": f"Response was Not successfull",
#                             "endpoint": url
#                         }
#             kk = make_api_request_log_request(request,dddata)
#             logger.info(f"the post response is {response.text}")
#         return response

      

import requests
from urllib.parse import urlencode
import logging
import json
from datetime import timedelta
from django.utils import timezone
from requests.auth import HTTPBasicAuth

from home.models import AuthToken
from utils.logs import make_api_request_log_request
from config.settings import USERNAME, PASSWORD, APIS  # USERNAME=client_id, PASSWORD=client_secret

logger = logging.getLogger(__name__)

class HTTPRequest:
    def __init__(self, base_url):
        self.base_url = base_url.rstrip("/")
        self.timeout = 20
        self.verify = False  # consider True in prod with proper CA
        self._access_token = None

    # ---------- AUTH ----------
    def _get_cached_token(self):
        try:
            tok = AuthToken.objects.latest("created_at")
        except AuthToken.DoesNotExist:
            return None
        if tok.expires_at and tok.expires_at > timezone.now():
            return tok.token
        return None  # expired

    def _cache_token(self, token: str, expires_in: int | None, expires_at_iso: str | None = None):
        # Clear old tokens
        AuthToken.objects.all().delete()
        if expires_at_iso:
            # If upstream provides an absolute timestamp
            expires_at = timezone.make_aware(timezone.datetime.fromisoformat(expires_at_iso)) \
                if "T" in expires_at_iso else timezone.now() + timedelta(seconds=3600)
        elif expires_in:
            expires_at = timezone.now() + timedelta(seconds=int(expires_in))
        else:
            # default 1 hour
            expires_at = timezone.now() + timedelta(hours=1)
        AuthToken.objects.create(token=token, expires_at=expires_at)

    def login(self):
        """
        OAuth2 Client Credentials:
        POST {BASE_URL}{/token}
        - Content-Type: application/x-www-form-urlencoded
        - Body: grant_type=client_credentials
        - Auth: HTTP Basic (client_id=USERNAME, client_secret=PASSWORD)
        Returns: {"status": 200, "data": {"access_token": "..."}}
        """
        # Serve from cache if valid
        cached = self._get_cached_token()
        if cached:
            self._access_token = cached
            return {"status": 200, "data": {"access_token": cached}}

        token_url = f"{APIS['BASE_URL'].rstrip('/')}{APIS['LOGIN']}"
        try:
            resp = requests.post(
                token_url,
                data={"grant_type": "client_credentials"},
                auth=HTTPBasicAuth(USERNAME, PASSWORD),
                headers={"Accept": "application/json",
                         "Content-Type": "application/x-www-form-urlencoded"},
                timeout=self.timeout,
                verify=self.verify,
            )
        except requests.RequestException as e:
            logger.exception("Token request failed (network): %s", e)
            return {"status": 502, "message": f"Token request failed: {e}"}

        ctype = (resp.headers.get("Content-Type") or "").lower()
        body_preview = (resp.text or "")[:500]

        if not resp.ok:
            logger.error("Token HTTP %s. CT=%s Body<=500: %s",
                         resp.status_code, ctype, body_preview)
            return {"status": resp.status_code, "message": "Login failed."}

        # Parse JSON defensively
        try:
            data = resp.json()
        except json.JSONDecodeError:
            logger.error("Token not JSON. CT=%s Body<=500: %s", ctype, body_preview)
            return {"status": 502, "message": "Token endpoint did not return valid JSON."}

        access_token = data.get("access_token")
        token_type = (data.get("token_type") or "").lower()
        expires_in = data.get("expires_in")
        expires_at = data.get("expires_at")  # if they provide absolute

        if not access_token:
            logger.error("Token payload missing access_token: %s", data)
            return {"status": 502, "message": "Access token missing in response."}

        if token_type and token_type != "bearer":
            logger.warning("Unexpected token_type: %s", token_type)

        self._access_token = access_token
        self._cache_token(access_token, expires_in, expires_at)

        return {"status": 200, "data": {"access_token": access_token}}

    def _auth_headers(self, fileType: str | None = None, extra: dict | None = None):
        if not self._access_token:
            login = self.login()
            if login.get("status") != 200:
                # Bubble up a clear error
                raise RuntimeError(login.get("message") or "Login failed")
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self._access_token}",
        }
        if fileType:
            headers["FileType"] = fileType
        if extra:
            headers.update(extra)
        return headers

    def is_connection_live(self):
        try:
            # HEAD is cheaper; fall back to GET if needed
            response = requests.head(self.base_url, verify=self.verify, timeout=self.timeout)
            return response.ok
        except requests.exceptions.RequestException as e:
            logger.error("Connectivity check failed: %s", e)
            return False

    # ---------- HELPERS ----------
    def _log_req(self, request, role, ok: bool, message: str, endpoint: str):
        try:
            make_api_request_log_request(request, {
                "role": role,
                "successfull": bool(ok),
                "message": message,
                "endpoint": endpoint
            })
        except Exception:
            # Avoid breaking the main flow due to logging issues
            logger.exception("Failed to write API request log")

    def _safe_json(self, resp):
        ctype = (resp.headers.get("Content-Type") or "").lower()
        if "application/json" in ctype:
            try:
                return resp.json()
            except json.JSONDecodeError:
                pass
        # fallback best effort
        try:
            return json.loads(resp.text)
        except Exception:
            return {"raw": resp.text, "content_type": ctype, "status": resp.status_code}

    # ---------- REQUESTS ----------
    def send_post_request(self, url, params=None, data=None, role=None, request=None, fileType=None):
        endpoint = f"{self.base_url}{url}"
        self._log_req(request, role, True, f"Began processing POST {endpoint}", endpoint)

        if not self.is_connection_live():
            self._log_req(request, role, False, "Connection is not live", endpoint)
            return None

        try:
            headers = self._auth_headers(fileType=fileType)
        except RuntimeError as e:
            logger.error("Login failed, cannot proceed with request: %s", e)
            return None

        # Prefer json= to set header and encode automatically
        try:
            resp = requests.post(
                endpoint,
                params=params or None,
                json=data if data is not None else None,
                headers=headers,
                verify=self.verify,
                timeout=self.timeout,
            )
        except requests.RequestException as e:
            self._log_req(request, role, False, f"POST failed: {e}", endpoint)
            logger.exception("POST failed: %s", e)
            return None

        ok = resp.ok
        self._log_req(request, role, ok, f"POST response {'OK' if ok else 'NOT OK'}", endpoint)

        if ok:
            try:
                logger.info("POST %s -> %s", endpoint, resp.json())
            except Exception:
                logger.info("POST %s -> %s", endpoint, resp.text)
        else:
            logger.error("POST %s -> HTTP %s Body<=1000: %s",
                         endpoint, resp.status_code, (resp.text or "")[:1000])

        return self._safe_json(resp)

    def send_get_request(self, url, body=None, params=None, headers=None, role=None, request=None, fileType=None):
        endpoint = f"{self.base_url}{url}"
        self._log_req(request, role, True, f"Began processing GET {endpoint}", endpoint)

        if not self.is_connection_live():
            self._log_req(request, role, False, "Connection is not live", endpoint)
            return None

        try:
            auth_headers = self._auth_headers(fileType=fileType)
        except RuntimeError as e:
            logger.error("Login failed, cannot proceed with request: %s", e)
            return None

        if headers:
            auth_headers.update(headers)

        # Do NOT send body with GET; move body to query if needed
        q = params.copy() if params else {}
        if isinstance(body, dict):
            q.update(body)

        try:
            resp = requests.get(
                endpoint,
                params=q or None,
                headers=auth_headers,
                verify=self.verify,
                timeout=self.timeout,
            )
        except requests.RequestException as e:
            self._log_req(request, role, False, f"GET failed: {e}", endpoint)
            logger.exception("GET failed: %s", e)
            return None

        ok = resp.ok
        self._log_req(request, role, ok, f"GET response {'OK' if ok else 'NOT OK'}", endpoint)
        return self._safe_json(resp)

    def send_put_request(self, url, body=None, params=None, headers=None, role=None, request=None, fileType=None):
        endpoint = f"{self.base_url}{url}"
        self._log_req(request, role, True, f"Began processing PUT {endpoint}", endpoint)

        if not self.is_connection_live():
            self._log_req(request, role, False, "Connection is not live", endpoint)
            return None

        try:
            auth_headers = self._auth_headers(fileType=fileType)
        except RuntimeError as e:
            logger.error("Login failed, cannot proceed with request: %s", e)
            return None

        if headers:
            auth_headers.update(headers)

        try:
            resp = requests.put(
                endpoint,
                params=params or None,
                json=body if body is not None else None,
                headers=auth_headers,
                verify=self.verify,
                timeout=self.timeout,
            )
        except requests.RequestException as e:
            self._log_req(request, role, False, f"PUT failed: {e}", endpoint)
            logger.exception("PUT failed: %s", e)
            return None

        ok = resp.ok
        self._log_req(request, role, ok, f"PUT response {'OK' if ok else 'NOT OK'}", endpoint)
        return self._safe_json(resp)

    # Optional: legacy helper (GET with explicit body) — redirect to send_get_request
    def send_get_with_body(self, url, data, role, request):
        return self.send_get_request(url=url, body=data, role=role, request=request)
