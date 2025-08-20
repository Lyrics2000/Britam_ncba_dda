# urls.py
from django.urls import path
from .views import (
    # Amali (Bank)
    AmaliTokenApiView,
    AmaliAccountValidationApiView,
    AmaliNewMandateApiView,
    AmaliAmendMandateApiView,
    AmaliCancelMandateApiView,
    AmaliDirectDebitCollectionApiView,
    # Originator (Your ERP)
    OriginatorOutwardDDPostingApiView,
    OriginatorOutwardDDUnpaidPostingApiView,
    OriginatorDDLogApiView,
    OriginatorDDOutwardDirectDebitPostingApiView,
    OriginatorOutwardDDsUnpaidPostingApiView,
)

app_name = "home"

urlpatterns = [
    path(
        "dd/v1/amali/token/",
        AmaliTokenApiView.as_view(),
        name="amali-token",
    ),
    path(
        "dd/v1/amali/account-validation/",
        AmaliAccountValidationApiView.as_view(),
        name="amali-account-validation",
    ),
    path(
        "dd/v1/amali/mandates/new/",
        AmaliNewMandateApiView.as_view(),
        name="amali-new-mandate",
    ),
    path(
        "dd/v1/amali/mandates/amend/",
        AmaliAmendMandateApiView.as_view(),
        name="amali-amend-mandate",
    ),
    path(
        "dd/v1/amali/mandates/cancel/",
        AmaliCancelMandateApiView.as_view(),
        name="amali-cancel-mandate",
    ),
    path(
        "dd/v1/amali/collections/initiate/",
        AmaliDirectDebitCollectionApiView.as_view(),
        name="amali-dd-collection",
    ),

    # =========================
    # ORIGINATOR (ERP) endpoints
    # =========================
    # Bank → ERP (paid posting)
    path(
        "dd/v1/originator/outward/posting/",
        OriginatorOutwardDDPostingApiView.as_view(),
        name="originator-outward-posting",
    ),
    # Bank → ERP (unpaid posting)
    path(
        "dd/v1/originator/outward/unpaid/",
        OriginatorOutwardDDUnpaidPostingApiView.as_view(),
        name="originator-outward-unpaid",
    ),
    # Optional: DD log (if you expose it)
    path(
        "dd/v1/originator/log/",
        OriginatorDDLogApiView.as_view(),
        name="originator-dd-log",
    ),
    # Optional: alternate posting paths mentioned in summary
    path(
        "dd/v1/originator/outward/posting-alt/",
        OriginatorDDOutwardDirectDebitPostingApiView.as_view(),
        name="originator-outward-posting-alt",
    ),
    path(
        "dd/v1/originator/outward/unpaid-alt/",
        OriginatorOutwardDDsUnpaidPostingApiView.as_view(),
        name="originator-outward-unpaid-alt",
    ),
]
