from django.contrib.auth import get_user_model, authenticate, logout
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.api.serializers import PatientRegistrationSerializer, DocRegistrationSerializer
from accounts.models import EmailActivation
from recent_activities.models import RecentActivity
from user_profile.models import PersonalInfo, Doctor

User = get_user_model()


@api_view(['POST', ])
@permission_classes([])
@authentication_classes([])
def doc_registration_view(request):
    if request.method == 'POST':
        payload = {}
        data = {}
        email = request.data.get('email', '0').lower()
        if validate_email(email) != None:
            payload['error_message'] = 'That email is already in use.'
            payload['response'] = 'Error'
            return Response(payload)

        username = request.data.get('username', '0')
        if validate_username(username) != None:
            payload['error_message'] = 'That username is already in use.'
            payload['response'] = 'Error'
            return Response(payload)

        serializer = DocRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            payload['response'] = 'Successful'
            data['username'] = user.username
            data['email'] = user.email
            data['last_name'] = user.last_name
            data['first_name'] = user.first_name
            token = Token.objects.get(user=user).key
            data['token'] = token

            payload['data'] = data
        else:
            payload = serializer.errors
        return Response(payload)




def validate_email(email):
    user = None
    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        return None
    if user != None:
        return email


def validate_username(username):
    user = None
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        return None
    if user != None:
        return username




class ObtainDocAuthTokenView(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        payload = {}
        data = {}

        email = request.data.get('email', '0')
        password = request.data.get('password', '0')

        qs = User.objects.filter(email=email)

        if qs.exists():
            not_active = qs.filter(is_active=False)
            if not_active.exists():
                reconfirm_msg = "resend confirmation email"
                confirm_email = EmailActivation.objects.filter(email=email)
                is_confirmable = confirm_email.confirmable().exists()
                if is_confirmable:
                    msg1 = "Please check your email to confirm your account or " + reconfirm_msg.lower()
                    payload['response'] = "Error"
                    payload['error_message'] = msg1
                    return Response(payload)
                email_confirm_exists = EmailActivation.objects.email_exists(email).exists()
                if email_confirm_exists:
                    msg2 = "Email not confirmed. " + reconfirm_msg
                    payload['response'] = "Error"
                    payload['error_message'] = msg2
                    return Response(payload)
                if not is_confirmable and not email_confirm_exists:
                    payload['response'] = "Error"
                    payload['error_message'] = "This user is inactive."
                    return Response(payload)

            try:
                doc = Doctor.objects.get(user=qs.first())
            except Doctor.DoesNotExist:
                payload['response'] = "Error"
                payload['error_message'] = "You are not a doctor"
                return Response(payload)

            print("######## THE DOC #######")
            print(doc)



        print(email, password)
        user = authenticate(email=email, password=password)
        RecentActivity.objects.create(
            user=user,
            subject="Doctor login - Mobile",
            verb="You logged in on mobile"
        )
        if user:
            try:
                token = Token.objects.get(user=user)
            except Token.DoesNotExist:
                token = Token.objects.create(user=user)

            try:
                personal_info = PersonalInfo.objects.get(user=user)
            except PersonalInfo.DoesNotExist:
                personal_info = PersonalInfo.objects.create(user=user)

            payload['response'] = 'Successful'
            data['id'] = user.pk
            data['username'] = user.username
            data['email'] = user.email
            data['last_name'] = user.last_name
            data['first_name'] = user.first_name
            data['photo'] = personal_info.photo.url
            data['active'] = personal_info.active
            data['token'] = token.key
            payload['data'] = data
            print(payload)
        else:
            payload['response'] = 'Error'
            payload['error_message'] = 'Invalid credentials'
            print(payload)
        return Response(payload)




@api_view(['GET', ])
@permission_classes((IsAuthenticated, ))
@authentication_classes((TokenAuthentication,))
def logout_doc_view_api(request):
    payload = {}
    data = {}
    user = request.user
    if request.method == 'GET':
        request.user.auth_token.delete()
        logout(request)

        RecentActivity.objects.create(
            user=user,
            subject="Patient logout - Mobile",
            verb="You Logged out on mobile"
        )
        payload['response'] = 'Successful'
    return Response(payload)


