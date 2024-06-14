from django.shortcuts import render

from appointments.models import Payment
from financials.models import Invoice


def invoice_page(request):
    context = {}

    all_invoices = Invoice.objects.all().order_by('-created_at')

    context['all_invoices'] = all_invoices



    return render(request, 'financials/invoice_page.html', context)


def payments_page(request):
    context = {}

    all_payments = Payment.objects.all().order_by('-created_at')

    context['all_payments'] = all_payments



    return render(request, 'financials/payments_page.html', context)