

import requests
import logging
logger = logging.getLogger(__name__)


def log_api_request(log_type, api_url, request_data, response_data, status_code, log_message):
   
    # Log to the standard logger
    if log_type == 'INFO':
        logger.info(f"Request to {api_url}: {log_message} - Status: {status_code}")
        logger.info(f"Request Data: {request_data}")
        logger.info(f"Response Data: {response_data}")
    elif log_type == 'ERROR':
        logger.error(f"Request to {api_url} failed: {log_message}")
        logger.error(f"Request Data: {request_data}")
        logger.error(f"Error Details: {response_data}")
    
    # Log to the database using the Logs model
    # res =  Logs.objects.create(
    #     log_type=log_type,
    #     api_url=api_url,
    #     request_data=request_data,
    #     response_data=response_data,
    #     status_code=status_code,
    #     log_message=log_message
    # )

    return None



