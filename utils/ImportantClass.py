from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .Middleware import (
    MicrosoftValidation
)
from .HTTPRequest import (
    HTTPRequest
)
import logging

from .logs import (
    make_api_request_log_request
)
logger = logging.getLogger(__name__)

class BaseAPIView(APIView):
    role: str = None
    endpoint: str = None
    has_body: bool = True
    has_params: bool = True
    base_url:str = ""
    method: str = "GET"  # Default HTTP method
    file_type: str = ""  # Default file type

    def perform_request(self, request):
        """
        Determines the appropriate HTTP method and sends the request.
        """
        app1 = self.authenticate_and_authorize(request)
        print(f"the api is {app1}")
        logger.info(f"the api is {app1}")
        if app1['status'] ==  False:
            logger.info(f"the api11211 is {app1}")
            
            inf = {"status": "Failed", "message":app1['message']}
            dddata = {
                            "role": self.role,
                            "successfull": False,
                            "message": f"{inf}",
                            "endpoint": self.endpoint
                        }
            kk = make_api_request_log_request(request,dddata)
            logger.error(f"the info is {inf}")
            return Response(
                {"status": "Failed", "message":app1['message']},
                status=401,
            )
        body, params = self.process_request(request)
        logger.info(f"Body: {body}, Params:{params}")
        logger.info(f"HasBody: {self.has_body}")
        http_client = HTTPRequest(self.base_url)
        rol = self.role
        if self.method == "GET":            
            return http_client.send_get_request(f"{self.endpoint}",body=body,params=params,role  = self.role,request=request,fileType = self.file_type)
        elif self.method == "POST":
            return http_client.send_post_request(f"{self.endpoint}", data=body,role  = self.role,request=request,fileType = self.file_type)
        elif self.method == "PUT":
            return http_client.send_put_request(f"{self.endpoint}", body=body,params=params,role  = self.role,request=request,fileType = self.file_type)
        elif self.method == "PATCH":
            return http_client.send_patch_request(f"{self.endpoint}", data=body,role  = self.role,request=request,fileType = self.file_type)
        elif self.method == "DELETE":
            return http_client.send_delete_request(f"{self.endpoint}", params=params,role  = self.role,request=request,fileType = self.file_type)
        elif self.method == "SEND_AS_GET":
            return http_client.send_get_request(f"{self.endpoint}",body=body,params=params,role  = self.role,request=request,fileType = self.file_type)
        else:
            dddata = {
                            "role": self.role,
                            "successfull": False,
                            "message": f"Unsupported HTTP method: {self.method}",
                            "endpoint": self.endpoint
                        }
            kk = make_api_request_log_request(request,dddata)
            raise ValueError(f"Unsupported HTTP method: {self.method}")

    def process_request(self, request):
        """
        Prepares the request data based on class attributes and method.
        Handles scenarios where a GET request may have a body, params, both, or neither.
        """
        body = request.data if self.has_body else None
        params = request.query_params.dict() if self.has_params else None

        return body, params
    


    
    def authenticate_and_authorize(self, request):
        view_name = self.__class__.__name__
        app = MicrosoftValidation(request).verify()
        mm = {}
        
        if app['code'] ==  401:
            dddata = {
                            "role": self.role,
                            "successfull": False,
                            "message": f"Unauthorized access attempt",
                            "endpoint": self.endpoint
                        }
            kk = make_api_request_log_request(request,dddata)
            # log_view_request(view_name, request, "Unauthorized access attempt", level="warning")
            mm =  app
            return app
        else:
            roles = app.get("data", {}).get("data",{}).get("roles", [])
            logger.info(f"the error is logss qj {roles}")
            if self.role not in roles:
                dddata = {
                            "role": self.role,
                            "successfull": False,
                            "message": f"Access denied: Insufficient roles",
                            "endpoint": self.endpoint
                        }
                kk = make_api_request_log_request(request,dddata)
                # log_view_request(view_name, request, "Access denied: Insufficient roles", level="warning")
                mm =  {
                    "status":False,
                    "message":"You have no rights to access this request"
                }
            dddata = {
                            "role": self.role,
                            "successfull": True,
                            "message": f"Authentication and authorization successful",
                            "endpoint": self.endpoint
                        }
            kk = make_api_request_log_request(request,dddata)
            # log_view_request(view_name, request, "Authentication and authorization successful")
            return {
                "status":True
                
            }

    def handle_request(self, request):
        """
        Core method that handles incoming requests.
        """
        response = self.perform_request(request)
        return self.handle_response(request, response)
    
    def handle_response(self, request, response):
        """Handles the response returned by HTTPRequest.
        """
        if response is None:
            dddata = {
                            "role": self.role,
                            "successfull": False,
                            "message": f"Server connection issue  {response}",
                            "endpoint": self.endpoint
                        }
            kk = make_api_request_log_request(request,dddata)
            return Response(
                {"status": "Failed", "message": "Connection issue with the server"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
        try:
            return Response(
                response.json(),
            status=response.status_code)
        
        except Exception as e:
            
            try:
                return response
            except Exception as e:
                dddata = {
                            "role": self.role,
                            "successfull": True,
                            "message": f"Invalid response Format",
                            "endpoint": self.endpoint
                        }
                kk = make_api_request_log_request(request,dddata)
                return Response(
                {"status": "Failed", "message": "Invalid response format"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def get(self, request):
        """
        Handles GET requests.
        """
        return self.handle_request(request)

    def post(self, request):
        """
        Handles POST requests.
        """
        return self.handle_request(request)

    def put(self, request):
        """
        Handles PUT requests.
        """
        return self.handle_request(request)

    def patch(self, request):
        """
        Handles PATCH requests.
        """
        return self.handle_request(request)

    def delete(self, request):
        """
        Handles DELETE requests.
        """
        return self.handle_request(request)
    