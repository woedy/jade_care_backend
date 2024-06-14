from django.shortcuts import render

def prescriptions_view(request):
    context = {}

    return render(request, 'prescriptions/prescriptions.html', context)
