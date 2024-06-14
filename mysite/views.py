from django.shortcuts import render


def welcome_page(request):
    context = {}

    return render(request, 'welcome_page.html', context)