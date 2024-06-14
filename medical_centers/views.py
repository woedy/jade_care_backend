from django.shortcuts import render


def medical_centers_view(request):
    context = {}

    return render(request, 'medical_centers/medical_centers.html', context)
