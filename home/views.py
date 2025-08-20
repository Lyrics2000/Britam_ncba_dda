from django.shortcuts import render

from utils.ImportantClass import (
    BaseAPIView
)
from django.conf import settings

class AmaliTokenApiView(BaseAPIView):
    """
    OAuth2 Client Credentials (as per doc). Spec only gives endpoint.
    """
    role = settings.AMALI_TOKEN_ROLE
    endpoint = settings.APIS['LOGIN']  # https://api.AmaliDDs.com:1824/AmaliWebAPI/token
    method = "POST"
    has_body = True
    base_url = settings.APIS['BASE_URL']
    # Optionally, your BaseAPIView could look for this:
    auth_type = "none"

class AmaliAccountValidationApiView(BaseAPIView):
    """
    InHouse Bank Account Validation
    """
    role = settings.ROLES['BANK_ACCOUNT_VALIDATION']
    endpoint = settings.APIS['BANK_ACCOUNT_VALIDATION']
    method = "POST"
    has_body = True
    base_url = settings.APIS['BASE_URL']
    auth_type = "basic"  # spec shows Basic in sample; adjust if your BaseAPIView handles this

class AmaliNewMandateApiView(BaseAPIView):
    """
    NEW MANDATES - MRF
    """
    role = settings.ROLES['NEW_MANDATES']
    endpoint = settings.APIS['NEW_MANDATES']
    method = "POST"
    has_body = True
    base_url = settings.APIS['BASE_URL']
    auth_type = "basic"
    file_type = "MRF"  # to be sent as header FileType: MRF

class AmaliAmendMandateApiView(BaseAPIView):
    """
    AMEND MANDATES - AMF
    """
    role = settings.ROLES['AMMEND_MANDATES']
    endpoint = settings.APIS['AMMEND_MANDATES']
    method = "POST"
    has_body = True
    base_url = settings.APIS['BASE_URL']
    auth_type = "basic"
    file_type = "AMF"

class AmaliCancelMandateApiView(BaseAPIView):
    """
    CANCEL MANDATES - CMF
    """
    role = settings.ROLES['CANCEL_MANDATES']
    endpoint = settings.APIS['CANCEL_MANDATES']
    method = "POST"
    has_body = True
    base_url = settings.APIS['BASE_URL']
    auth_type = "basic"
    file_type = "CMF"

class AmaliDirectDebitCollectionApiView(BaseAPIView):
    """
    INITIATE DD COLLECTION - DDL
    """
    role = settings.ROLES['INITIATE_DD_COLLECTION']
    endpoint = settings.APIS['INITIATE_DD_COLLECTION']
    method = "POST"
    has_body = True
    base_url = settings.APIS['BASE_URL']
    auth_type = "basic"
    file_type = "DDL"

# ===============================
# ORIGINATOR (Your ERP) – Bank callbacks into you
# Base URL expected in: settings.APIS['BASE_URL']
# ===============================

class OriginatorOutwardDDPostingApiView(BaseAPIView):
    """
    Outward Direct Debit Posting (PAID)
    """
    role = settings.ROLES['OUTWARD_DIRECT_DEBIT_POSTING']
    endpoint = settings.APIS['OUTWARD_DIRECT_DEBIT_POSTING']  # https://api.Originator.com:8021/OutwardDDs
    method = "POST"
    has_body = True
    base_url = settings.APIS['BASE_URL']
    auth_type = "basic"

class OriginatorOutwardDDUnpaidPostingApiView(BaseAPIView):
    """
    Outward Direct Debit Unpaid Posting (UNPAID)
    """
    role = settings.ROLES['OUTWARD_DIRECT_DEBIT_UNPAID_POSTING']
    endpoint = settings.APIS['OUTWARD_DIRECT_DEBIT_UNPAID_POSTING']  # https://api.Originator.com:8021/OutwardDDsUnpaid
    method = "POST"
    has_body = True
    base_url = settings.APIS['BASE_URL']
    auth_type = "basic"

# ---- Optional: endpoints listed in the summary block of the spec ----

class OriginatorDDLogApiView(BaseAPIView):
    """
    OutDirectDebitsDataEndpoint (DD log)
    """
    role = settings.ORIGINATOR_DD_LOG_ROLE
    endpoint = "DD_log"  # https://api.originator.com:8021/DD_log
    method = "GET"
    has_params = True
    base_url = settings.APIS['BASE_URL']
    auth_type = "basic"

class OriginatorDDOutwardDirectDebitPostingApiView(BaseAPIView):
    """
    Alternate posting path mentioned in summary (if your infra exposes it)
    """
    role = settings.ORIGINATOR_OUTWARD_DIRECT_DEBIT_POSTING_ROLE
    endpoint = "DD_OutwardDirectDebitPosting"  # https://api.originator.com:8794/DD_OutwardDirectDebitPosting
    method = "POST"
    has_body = True
    base_url = settings.APIS['BASE_URL']
    auth_type = "basic"

class OriginatorOutwardDDsUnpaidPostingApiView(BaseAPIView):
    """
    Alternate unpaid posting path mentioned in summary
    """
    role = settings.ORIGINATOR_OUTWARD_DDS_UNPAID_POSTING_ROLE
    endpoint = "OutwardDDsUnpaidPosting"  # https://api.originator.com:8021/OutwardDDsUnpaidPosting
    method = "POST"
    has_body = True
    base_url = settings.APIS['BASE_URL']
    auth_type = "basic"
