import json
from itertools import chain

from django.contrib.auth import get_user_model
from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView

from accounts.api.serializers import UserSerializer
from accounts.models import User
from appointments.models import Appointment
from user_profile.models import Doctor, Patient


def admin_search_view(request):

    context = {}


    if request.GET:
        query = request.GET.get('q', None)
        print(query)
        if query is not None:
            user_result = User.objects.search(query)

            queryset_chain = chain(user_result,)

            qs = sorted(queryset_chain, key=lambda instance: instance.pk,reverse=True)
            context['qs'] = qs

    return render(request, 'search/admin_search_view.html', context)


class AdminSearchView(ListView):
    template_name = 'search/admin_search_view.html'
    paginate_by = 20
    count = 0

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['count'] = self.count or 0
        context['query'] = self.request.GET.get('q')
        return context

    def get_queryset(self):
        request = self.request
        query = request.GET.get('q', None)

        if query is not None:
            doctor_results = Doctor.objects.search(query)
            patient_results = Patient.objects.search(query)

            appointment_results = Appointment.objects.search(query)


            # combine querysets
            queryset_chain = chain(
                doctor_results,
                patient_results,
                appointment_results
            )
            qs = sorted(queryset_chain,
                        key=lambda instance: instance.pk,
                        reverse=True)
            self.count = len(qs)  # since qs is actually a list
            return qs
        return User.objects.none()  # just an empty queryset as default

@csrf_exempt
def admin_search_ajax(request):
    payload = {}
    user = request.user


    if request.POST:
        try:
            query = request.POST.get("q")


            if query is not None:
                if query is not "" and query is not " ":
                    user = User.objects.search(query)


                    user_serializer = UserSerializer(user, many=True)

                    q_chain = chain(user_serializer.data,)
                    new_l = list(q_chain)

                    new_l.sort(key=lambda x: x['id'], reverse=False)

                    payload['response'] = 'Successful'
                    payload['data'] = new_l
                    print(new_l)
                else:
                    payload['response'] = 'Error'
                    payload['error_message'] = "Enter a text"

        except Exception as e:
            print("exception: " + str(e))
            payload['result'] = "error"
            payload['exception'] = str(e)

    return HttpResponse(json.dumps(payload), content_type="application/json")