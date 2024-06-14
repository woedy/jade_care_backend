from django.shortcuts import render

def general_checkup_view(request):
    context = {}

    return render(request, 'general_checkup/general_checkup.html', context)