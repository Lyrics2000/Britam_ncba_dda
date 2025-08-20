
from django.http import JsonResponse

import requests
import logging

logger = logging.getLogger(__name__)


import logging
import time
from typing import Optional, Dict, Any

import requests
from requests.exceptions import RequestException
from jose import jwt
from jose.exceptions import JWTError, ExpiredSignatureError, JWTClaimsError, JWKError
from config.settings import AUDIENCE, ISSUER_ID
logger = logging.getLogger(__name__)


class ValidateToken:
    """
    Verifies a JWT issued by Azure AD using the tenant JWKS.
    Logs important steps with sanitized data (never logs the token itself).
    """

    def __init__(self, token: str, audience: str, tenant_id: str, *, request_id: Optional[str] = None):
        self.token = token
        self.audience = audience
        self.tenant_id = tenant_id
        self.request_id = request_id or "-"
        self.jwks_uri = f"https://login.microsoftonline.com/{self.tenant_id}/discovery/v2.0/keys"
        self.issuer = f"https://sts.windows.net/{self.tenant_id}/"

        logger.debug(
            "ValidateToken initialized [rid=%s, tenant=%s, aud=%s]",
            self.request_id, self.tenant_id, self.audience
        )

    def _safe_claims(self, claims: Dict[str, Any]) -> Dict[str, Any]:
        # Only log non-sensitive, high-level claims
        allow = {"sub", "aud", "iss", "tid", "appid", "oid", "upn", "unique_name", "exp", "iat", "nbf"}
        return {k: claims[k] for k in allow if k in claims}

    def decode_and_verify_token(self) -> Dict[str, Any]:
        started = time.perf_counter()
        logger.info(
            "Starting token verification [rid=%s, tenant=%s]", self.request_id, self.tenant_id
        )

        # 1) Fetch JWKS
        try:
            logger.debug("Fetching JWKS [rid=%s, url=%s]", self.request_id, self.jwks_uri)
            keys_response = requests.get(self.jwks_uri, timeout=10)
            logger.debug(
                "JWKS HTTP response [rid=%s, status=%s]", self.request_id, keys_response.status_code
            )
            keys_response.raise_for_status()
            keys_data = keys_response.json()
            if "keys" not in keys_data or not keys_data["keys"]:
                logger.error("JWKS payload missing 'keys' or empty [rid=%s]", self.request_id)
                return {
                    "code": 500,
                    "message": "JWKS missing keys",
                    "data": {"status": "Failed", "message": "Key set unavailable"},
                }
        except RequestException as err:
            logger.exception("Network error fetching JWKS [rid=%s]: %s", self.request_id, err)
            return {
                "code": 500,
                "message": "Internal verification error occurred",
                "data": {"status": "Failed", "message": "Network error during verification"},
            }
        except ValueError as err:
            logger.exception("Invalid JWKS JSON [rid=%s]: %s", self.request_id, err)
            return {
                "code": 500,
                "message": "Internal verification error occurred",
                "data": {"status": "Failed", "message": "Invalid JWKS response"},
            }

        # 2) Extract KID from token header (no signature verification yet)
        try:
            unverified_header = jwt.get_unverified_header(self.token)
            kid = unverified_header.get("kid")
            logger.debug("Unverified header parsed [rid=%s, kid=%s, alg=%s]",
                         self.request_id, kid, unverified_header.get("alg"))
        except JWTError as err:
            logger.warning("Invalid token header [rid=%s]: %s", self.request_id, err, exc_info=True)
            return {
                "code": 401,
                "message": "Invalid token header",
                "data": {"status": "Failed", "message": "Could not parse token header"},
            }

        if not kid:
            logger.warning("Token header missing 'kid' [rid=%s]", self.request_id)
            return {
                "code": 401,
                "message": "",
                "data": {"status": "Failed", "message": "Key ID (kid) not found in token header"},
            }

        # 3) Find matching key
        rsa_key = {}
        for key in keys_data["keys"]:
            if key.get("kid") == kid:
                rsa_key = {
                    "kty": key.get("kty"),
                    "kid": key.get("kid"),
                    "use": key.get("use"),
                    "n": key.get("n"),
                    "e": key.get("e"),
                }
                break

        if not rsa_key:
            logger.warning("No matching JWK for kid [rid=%s, kid=%s]", self.request_id, kid)
            return {
                "code": 401,
                "message": "Verification unsuccessful",
                "data": {"status": "Failed", "message": "Signing key not found for token"},
            }

        # 4) Verify token
        try:
            logger.debug(
                "Decoding token [rid=%s, kid=%s, issuer=%s, audience=%s]",
                self.request_id, kid, self.issuer, self.audience
            )
            decoded_token = jwt.decode(
                self.token,
                key=rsa_key,
                algorithms=["RS256"],
                audience=self.audience,
                issuer=self.issuer,
                options={"verify_signature": True},
            )

            elapsed_ms = int((time.perf_counter() - started) * 1000)
            logger.info(
                "Token verified [rid=%s, ms=%d, claims=%s]",
                self.request_id,
                elapsed_ms,
                self._safe_claims(decoded_token),
            )
            return {"code": 200, "message": "Successfully verified", "data": decoded_token}

        except ExpiredSignatureError:
            logger.info("Expired token [rid=%s]", self.request_id, exc_info=True)
            return {
                "code": 401,
                "message": "Token expired",
                "data": {"status": "Failed", "message": "Token has expired"},
            }
        except JWTClaimsError as e:
            logger.warning("Claims validation failed [rid=%s]: %s", self.request_id, e, exc_info=True)
            return {
                "code": 401,
                "message": "Invalid token claims",
                "data": {"status": "Failed", "message": "Audience/issuer/claims invalid"},
            }
        except (JWKError, JWTError) as e:
            logger.error("JWT error during verification [rid=%s]: %s", self.request_id, e, exc_info=True)
            return {
                "code": 401,
                "message": "Verification unsuccessful",
                "data": {"status": "Failed", "message": "Authentication error occurred"},
            }
        except Exception as e:
            logger.exception("Unexpected error during verification [rid=%s]: %s", self.request_id, e)
            return {
                "code": 500,
                "message": "Internal verification error occurred",
                "data": {"status": "Failed", "message": "Unexpected error during verification"},
            }



class MicrosoftValidation:
    def __init__(self, request, *, request_id=None):
        self.request = request
        self.request_id = request_id or request.META.get("HTTP_X_REQUEST_ID") or "-"
        self.sub_key = request.META.get("HTTP_OCP_APIM_SUBSCRIPTION_KEY")
        self.raw_auth = request.META.get("HTTP_AUTHORIZATION")

    def _extract_bearer(self):
        if not self.raw_auth:
            return None
        parts = self.raw_auth.split(" ", 1)
        if len(parts) != 2 or parts[0].lower() != "bearer" or not parts[1].strip():
            logger.warning("Bad Authorization header format [rid=%s]", self.request_id)
            return None
        return parts[1].strip()

    def verify(self):
        logger.info("Starting MicrosoftValidation.verify [rid=%s]", self.request_id)

        if not self.sub_key:
            logger.warning("Missing subscription key [rid=%s]", self.request_id)
            return {
                "code": 401,
                "message": "Missing subscription key",
                "data": {"status": "Failed", "message": "Ocp-Apim-Subscription-Key header is required"},
            }

        token = self._extract_bearer()
        if not token:
            logger.warning("Missing/invalid Bearer token [rid=%s]", self.request_id)
            return {
                "code": 401,
                "message": "Missing/invalid Authorization header",
                "data": {"status": "Failed", "message": "Bearer token is required"},
            }

        app = ValidateToken(token, AUDIENCE, ISSUER_ID, request_id=self.request_id)
        res = app.decode_and_verify_token()  # {code, message, data}
        return res

    @staticmethod
    def has_permission(claims: dict, required: str) -> bool:
        # App roles
        roles = claims.get("roles", [])
        if isinstance(roles, list) and required in roles:
            return True
        # Delegated scopes
        scp = claims.get("scp") or claims.get("scope")
        if isinstance(scp, str) and required in scp.split():
            return True
        return False