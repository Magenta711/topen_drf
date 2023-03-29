from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from django.db import transaction
from api.utils import *
from api.serializers import *
from rest_framework.status import HTTP_200_OK,HTTP_500_INTERNAL_SERVER_ERROR
from datetime import datetime
from pytz import timezone
import traceback
from rest_framework import authentication
from rest_framework import exceptions
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, permission_classes
from django.contrib.auth import authenticate,logout
from rest_framework.authtoken.models import Token

def get_date_time():
    fmt = "%Y-%m-%d %H:%M:%S"
    zona = 'America/Bogota'
    fecha = datetime.now(timezone(zona))
    fecha_hora = fecha.strftime(fmt)
    return fecha_hora

# Create your views here.
@csrf_exempt
@api_view(["POST"])
@permission_classes((AllowAny,))
def Login(request):
    try:       
        username = request.data.get("username")
        password = request.data.get("password")        
        if username is None or password is None:
            return Response({'response': 'Please provide both username and password', 'msg' : -1}, status = HTTP_200_OK)
        user = authenticate(username = username, password = password)
        if not user:
            return Response({'response': 'Username or password incorrect', 'msg' : -1}, status = HTTP_200_OK)
        token, _ = Token.objects.get_or_create(user=user)   
        user_data = UserSerializer(user,  many = False).data
        
        return Response({'response': 'Success', 'msg' : 1, 'token': token.key, 'expiration_date': token.created , 'user' : user_data}, status = HTTP_200_OK)
    except:
        print(traceback.format_exc())
        return Response({'response': 'Error', 'msg' : -1}, status = HTTP_500_INTERNAL_SERVER_ERROR)
    
class LogoutView(APIView):
    def get(self, request):
        request.user.auth_token.delete()
        logout(request)
        return Response({'response': 'Success', 'msg' : 1}, status = HTTP_200_OK)
    
class ResetPasswordEmail(APIView):
    permission_classes = (AllowAny,)
    @transaction.atomic
    def post(self, request):
        try:   
            with transaction.atomic():
                token = Utils.reset_password_email(request,get_date_time())
                return Response({"response" : "Success", "msg" : 1, "token": token}, status = HTTP_200_OK)
        except User.DoesNotExist:
            status = "No se encontro el usuario, favor validar el correo"
            return Response({"response" : "Success - " + status, "msg" : -1}, status = HTTP_200_OK)
        except:    
            print(traceback.format_exc())
            return Response({'response': 'Error', "msg" : -1}, status = HTTP_500_INTERNAL_SERVER_ERROR)
        
class VerifyUserTokenEmail(APIView):
    permission_classes = (AllowAny,)
    @transaction.atomic
    def post(self, request):
        try:   
            with transaction.atomic():
                Utils.token_validation_email(request)
                return Response({"response" : "Success", "msg" : 1}, status = HTTP_200_OK)
        except PasswordResets.DoesNotExist:
            response = 'No se encontro token'
            return Response({"response" : response, "msg" : -1}, status = HTTP_200_OK)
        except:    
            print(traceback.format_exc())
            return Response({'response': 'Error', "msg" : -1}, status = HTTP_500_INTERNAL_SERVER_ERROR)

class ChangePasswordEmail(APIView):
    permission_classes = (AllowAny,)
    @transaction.atomic
    def post(self, request):
        try:   
            with transaction.atomic():
                Utils.change_password_email(request)
                return Response({"response": 'Success', "msg" : 1}, status = HTTP_200_OK)        
        except PasswordResets.DoesNotExist:
            response = 'No se encontro token'
            return Response({"response": response, "msg" : -1}, status = HTTP_200_OK)
        except:    
            print(traceback.format_exc())
            return Response({'response': 'Error', 'msg' : -1}, status = HTTP_500_INTERNAL_SERVER_ERROR)