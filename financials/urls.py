from django.urls import path

from financials.views import invoice_page, payments_page

app_name = "financials"

urlpatterns = [
    path("invoice_page/", invoice_page, name="invoice_page"),
    path("payments_page/", payments_page, name="payments_page"),


]
