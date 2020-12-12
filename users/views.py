
"""
 ******************************************************************************
 *  Purpose: will save user details after registrations
 *
 *  @author  Shubham Kumar
 *  @version 3.8.5
 *  @since   12/10/2020
 ******************************************************************************
"""

import json
import jwt
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.models import User, auth
from fundoo.settings import EMAIL_HOST_USER, file_handler
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.http import HttpResponse
from django.shortcuts import redirect
from django.urls import reverse
from jwt import ExpiredSignatureError
from rest_framework.exceptions import ValidationError
from rest_framework.generics import GenericAPIView
from users.serializers import RegistrationSerializer,LoginSerializer,EmailSerializer,ResetSerializer
from django.core.validators import validate_email
from django_short_url.views import get_surl
from django_short_url.models import ShortURL
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.authtoken.models import Token
# from rest_framework.permissions import IsAuthenticated
import logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.addHandler(file_handler)

class Registrations(GenericAPIView):
   
    # permission_classes = (permissions.IsAuthenticated,)
    serializer_class = RegistrationSerializer

    def post(self, request):

        username = request.data['username']
        email = request.data['email']
        password = request.data['password']


        smd = {
            'success': False,
            'message': "not registered yet",
            'data': [],
        }

        try:
            validate_email(email)
        except Exception as e:
            smd['message'] = "please enter vaild email address"
            logger.error("error: %s while as email entered was not a vaild email address", str(e))
            return HttpResponse(json.dumps(smd), status=400)
            #return Response(smd, status=status.HTTP_400_BAD_REQUEST)

        # user input is checked
        if username == "" or email == "" or password == "":
            smd['message'] = "one of the details missing"
            logger.error("one of the details missing logging in")
            return HttpResponse(json.dumps(smd), status=400)
            #return Response(smd, status=status.HTTP_400_BAD_REQUEST)

        # if email exists it will show error message
        elif User.objects.filter(email=email).exists():
            smd['message'] = "email address is already registered "
            logger.error("email address is already registered  while logging in")
            return HttpResponse(json.dumps(smd), status=400)
            #return Response(smd, status=status.HTTP_400_BAD_REQUEST)

        else:
            try:
                user_created = User.objects.create_user(username=username, email=email, password=password,is_active=True)
                user_created.save()
                # user is unique then we will send token to his/her email for validation
                if user_created is not None:
                    token = Token(username, password)
                    url = str(token)
                    surl = get_surl(url)
                    z = surl.split("/")

                    mail_subject = "Activate your account by clicking below link"
                    mail_message ={
                        'user': user_created.username,
                        'domain': get_current_site(request).domain,
                        'surl': z[2]
                    }
                    recipient_email = user_created.email
                    email = EmailMessage(mail_subject, mail_message, to=[recipient_email])
                    email.send()
                    smd = {
                        'success': True,
                        'message': 'please check the mail and click on the link  for validation',
                        'data': [token],
                    }
                    logger.error("email was sent to %s email address ", username)
                    return HttpResponse(json.dumps(smd), status=201)
            except Exception as e:
                smd["success"] = False
                smd["message"] = "username already taken"
                logger.error("error: %s while loging in ", str(e))
                return HttpResponse(json.dumps(smd), status=400)
                #return Response(smd, status=status.HTTP_400_BAD_REQUEST)


class Login(GenericAPIView):
    """
    :param APIView: user request is made from the user
    :return: will check the credentials and will user
    """
    serializer_class = LoginSerializer

    def post(self, request):

        smd = {
            'success': False,
            'message': "not logged in ",
            'data': []
        }
        try:
            username = request.data['username']
            password = request.data['password']
            # validation is done
            if username == "" or password == "":
                smd['message'] = 'one or more fields is empty'
                return HttpResponse(json.dumps(smd), status=400)

        except Exception as e:
            smd['message'] = 'invaild credentials'
            logger.error("error: %s while loging in ", str(e))
            return HttpResponse(json.dumps(smd), status=400)

class Logout(GenericAPIView):
    serializer_class = LoginSerializer

    def get(self, request):
        """
        :param request: logout request is made
        :return: we will delete the token which was stored in redis
        """
        smd = {"success": False, "message": "not a vaild user", "data": []}
        try:
            user = request.user
            User.delete(user.username)
            smd = {"success": True, "message": " logged out", "data": []}
            logger.error("%s looged out succesfully ", user)
            return HttpResponse(json.dumps(smd), status=200)
        except Exception:
            logger.error("something went wrong while logging out")
            return HttpResponse(json.dumps(smd), status=400)


class ForgotPassword(GenericAPIView):
    """
    :param request: request is made for resetting password
    :return:  will return email where password reset link will be attached
    """
    serializer_class = EmailSerializer

    def post(self, request):

        global response
        email = request.data["email"]
        response = {
            'success': False,
            'message': "not a vaild email ",
            'data': []
        }
        # email validation is done here

        if email == "":
            response['message'] = 'email field is empty please provide vaild input'
            return HttpResponse(json.dumps(response), status=400)
        else:

            try:
                validate_email(email)
            except Exception:
                return HttpResponse(json.dumps(response) ,status=400)
            try:
                user = User.objects.filter(email=email)
                useremail = user.values()[0]["email"]
                username = user.values()[0]["username"]
                id = user.values()[0]["id"]

                #  here user is not none then token is generated
                if useremail is not None:
                    token = Token(username, id)
                    url = str(token)
                    surl = get_surl(url)
                    z = surl.split("/")

                    # email is generated  where it is sent the email address entered in the form
                    mail_subject = "Activate your account by clicking below link"
                    mail_message = {
                        'user': username,
                        'domain': get_current_site(request).domain,
                        'surl': z[2]
                    }

                    recipientemail = email

                    email=EmailMessage('send_email', recipientemail, mail_message,mail_subject)
                    email.send()
                    response = {
                        'success': True,
                        'message': "check email for vaildation ",
                        'data': []
                    }
                    # here email is sent to user
                    return HttpResponse(json.dumps(response), status=201)
            except Exception as e:
                print(e)
                response['message'] = "something went wrong"
                return HttpResponse(json.dumps(response), status=400)


def activate(request, surl):
    """
    :param request: request is made by the used
    :param token:  token is fetched from url
    :return: will register the account
    """
    try:
        # decode is done for the JWT token where username is fetched

        tokenobject = ShortURL.objects.get(surl=surl)
        token = tokenobject.lurl
        decode = jwt.decode(token, settings.SECRET_KEY)
        username = decode['username']
        user = User.objects.get(username=username)

        # if user is not none then user account willed be activated
        if user is not None:
            user.is_active = True
            user.save()
            messages.info(request, "your account is active now")
            return redirect('/api/login')
        else:
            messages.info(request, 'was not able to sent the email')
            return redirect('/api/registration')
    except KeyError:
        messages.info(request, 'was not able to sent the email')
        return redirect('/api/registration')
    except ExpiredSignatureError:
        messages.info(request, 'activation link expired')
        return redirect('/api/registration')
    except Exception:
        messages.info(request, 'activation link expired')
        return redirect('/api/registration')


def reset_password(request, surl):
    """
    :param surl:  token is again send to the user
    :param request:  user will request for resetting password
    :return: will reset the password
    """
    try:
        # here decode is done with jwt

        tokenobject = ShortURL.objects.get(surl=surl)
        token = tokenobject.lurl
        decode = jwt.decode(token, settings.SECRET_KEY)
        username = decode['username']
        user = User.objects.get(username=username)

        # if user is not none then we will fetch the data and redirect to the reset password page
        if user is not None:
            context = {'userReset': user.username}
            print(context)
            return redirect('/api/resetpassword/' + str(user))
        else:
            messages.info(request, 'was not able to sent the email')
            return redirect('/api/forgotpassword')
    except KeyError:
        messages.info(request, 'was not able to sent the email')
        return redirect('/api/forgotpassword')
    except Exception as e:
        print(e)
        messages.info(request, 'activation link expired')
        return redirect('/api/forgotpassword')

class ResetPassword(GenericAPIView):
    """
    :param user_reset: username is fetched
    :param request:  user will request for resetting password
    :return: will chnage the password
    """
    serializer_class = ResetSerializer

    def post(self, request, user_reset):
        password = request.data['password']

        smd = {
            'success': False,
            'message': 'password reset not done',
            'data': [],
        }
        # password validation is done in this form
        if user_reset is None:
            smd['message'] = 'not a vaild user'
            return HttpResponse(json.dumps(smd), status=404)

        elif password == "":
            smd['message'] = 'one of the fields are empty'
            return HttpResponse(json.dumps(smd), status=400)

        elif len(password) <= 4:
            smd['message'] = 'password should be 4 or  more than 4 character'
            return HttpResponse(json.dumps(smd), status=400)

        else:
            try:

                user = User.objects.get(username=user_reset)
                user.set_password(password)
                # here we will save the user password in the database
                user.save()

                smd = {
                    'success': True,
                    'message': 'password reset done',
                    'data': [],
                }
                return HttpResponse(json.dumps(smd), status=201)
            except user.DoesNotExist:
                smd['message'] = 'not a vaild user '
                return HttpResponse(json.dumps(smd), status=400)
