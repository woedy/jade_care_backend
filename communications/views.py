import json

from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from communications.api.serializers.appointment_message_serializer import PrivateChatRoomMessageSerializer, \
    PrivateChatRoomSerializer
from communications.models import PrivateChatRoom, PrivateRoomChatMessage


def text_message_page_pat(request):
    context = {}



    return render(request, 'communications/text_message_pat.html', context)

def video_call_page(request):
    context = {}

    return render(request, 'communications/video_call_page.html', context)



def chat_page_admin(request):
    context = {}

    return render(request, 'communications/chat_page_admin.html', context)

def chat_page_patient(request):
    context = {}

    return render(request, 'communications/chat_page_patient.html', context)

def chat_page_doctor(request):
    context = {}

    return render(request, 'communications/chat_page_doctor.html', context)


@csrf_exempt
def all_chat_users_admin(request, *args, **kwargs):
    payload = {}

    if request.POST:
        try:
            user_id = request.POST.get('user_id')
            rooms = PrivateChatRoom.objects.all().filter(Q(user1=request.user) | Q(user2=request.user))
            serializers = PrivateChatRoomSerializer(rooms, many=True)
            if serializers:
                data = serializers.data

                print(user_id)
                print(rooms)
                payload['result'] = "success"
                payload['rooms'] = data



        except Exception as e:
            print("exception: " + str(e))
            payload['result'] = "error"
            payload['exception'] = str(e)

    return HttpResponse(json.dumps(payload), content_type="application/json")

@csrf_exempt
def all_chat_users_patient(request, *args, **kwargs):
    payload = {}

    if request.POST:
        try:
            user_id = request.POST.get('user_id')
            rooms = PrivateChatRoom.objects.all().filter(Q(user1=request.user) | Q(user2=request.user))
            serializers = PrivateChatRoomSerializer(rooms, many=True)
            if serializers:
                data = serializers.data

                print(user_id)
                print(rooms)
                payload['result'] = "success"
                payload['rooms'] = data



        except Exception as e:
            print("exception: " + str(e))
            payload['result'] = "error"
            payload['exception'] = str(e)

    return HttpResponse(json.dumps(payload), content_type="application/json")




@csrf_exempt
def all_chat_messages_admin(request, *args, **kwargs):
    payload = {}

    if request.POST:
        try:
            user_id = request.POST.get('user_id')
            room_id = request.POST.get('room_id')

            room_messages = PrivateRoomChatMessage.objects.by_room(room_id).order_by('timestamp')

            serializers = PrivateChatRoomMessageSerializer(room_messages, many=True)
            if serializers:
                data = serializers.data
                payload['result'] = "success"
                payload['messages'] = data



        except Exception as e:
            print("exception: " + str(e))
            payload['result'] = "error"
            payload['exception'] = str(e)

    return HttpResponse(json.dumps(payload), content_type="application/json")


@csrf_exempt
def all_chat_messages_patient(request, *args, **kwargs):
    payload = {}

    if request.POST:
        try:
            user_id = request.POST.get('user_id')
            room_id = request.POST.get('room_id')

            room_messages = PrivateRoomChatMessage.objects.by_room(room_id).order_by('timestamp')

            serializers = PrivateChatRoomMessageSerializer(room_messages, many=True)
            if serializers:
                data = serializers.data
                payload['result'] = "success"
                payload['messages'] = data



        except Exception as e:
            print("exception: " + str(e))
            payload['result'] = "error"
            payload['exception'] = str(e)

    return HttpResponse(json.dumps(payload), content_type="application/json")