# client.py
import requests
from django.conf import settings
from urllib.parse import urljoin
from django.core.cache import cache
import logging

logger = logging.getLogger(__name__)
class ConfigClient:
    def __init__(self, base_url=None):
        self.base_url = base_url or settings.CONFIG_SERVICE['BASE_URL']
        self.timeout = getattr(settings, 'CONFIG_SERVICE', {}).get('DEFAULT_TIMEOUT', 15)
        self.retry_attempts = getattr(settings, 'CONFIG_SERVICE', {}).get('RETRY_ATTEMPTS', 5)
        self.auth_token = getattr(settings, 'CONFIG_SERVICE', {}).get('AUTH_TOKEN')
        self.headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
        if self.auth_token:
            self.headers['Authorization'] = f'Bearer {self.auth_token}'

    def _make_request(self, method, path='', **kwargs):
        url = urljoin(self.base_url, path)
        logger.info(f"the base url is {url}")
        kwargs.setdefault('timeout', self.timeout)
        kwargs.setdefault('headers', self.headers)
        
        for attempt in range(self.retry_attempts):
            try:
                response = requests.request(method, url, **kwargs)
                response.raise_for_status()

                return response
            except requests.exceptions.RequestException as e:
                logger.warning(f"Attempt {attempt + 1} failed: {str(e)}")
                if attempt == self.retry_attempts - 1:
                    logger.error(f"All {self.retry_attempts} attempts failed")
                    raise

    def get(self, key, use_cache=True):
        cache_key = f'config_service_{key}'
        
        if use_cache:
            cached_value = cache.get(cache_key)
            if cached_value is not None:
                return cached_value
        
        try:
            response = self._make_request('GET', key)
            if response.status_code == 200:
                value = response.json().get(key)
                cache.set(cache_key, value, settings.CONFIG_SERVICE.get('CACHE_TIMEOUT', 300))
                return value
        except Exception as e:
            logger.error(f"Failed to get config {key}: {str(e)}")
            return None
    def get_all(self):
        try:
            response = self._make_request('GET')
            js_res = response.json()
            logger.info(f"The response is {js_res}")
            return js_res if response.status_code == 200 else {}
        except Exception as e:
            logger.error(f"Failed to get all configs: {str(e)}")
            return {}

    def set(self, key, value, description=""):
        try:
            response = self._make_request(
                'POST',
                json={'key': key, 'value': value, 'description': description}
            )
            if response.status_code == 201:
                cache.delete(f'config_service_{key}')  # Invalidate cache
                return True
            return False
        except Exception as e:
            logger.error(f"Failed to set config {key}: {str(e)}")
            return False