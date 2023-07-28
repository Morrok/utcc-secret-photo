from django.shortcuts import render, redirect, get_object_or_404
from rest_framework.views import APIView, View
from django.urls import reverse
from django.contrib import messages
from rest_framework.decorators import (
    api_view,
    permission_classes,
    authentication_classes
)
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
import json
from .models import (
    CustomUser,
    CookieConsent,
    PictureDescription
)
import datetime
import pytz
from django.db import transaction
from django.db.models import Q
import os
import base64
from django.conf import settings
from formtools.wizard.views import SessionWizardView
from .forms import (
    RegisterForm,
    LoginForm,
    ForgotPasswordForm,
    number_of_click_choice,
    PictureDescriptionForm
)
from django.core.files.storage import FileSystemStorage
from django.contrib import messages
from django.views.decorators.csrf import csrf_protect, ensure_csrf_cookie
from rest_framework.permissions import AllowAny
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
import uuid
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import get_user_model
from secret_photo import serializers


# def base_html(request):
#     context = {
#         'user': request.user
#     }
#     print(context)
#     return context
# return JsonResponse({'user': request.user})


class Home(View):
    template_name = 'secret_photo/homepage.html'

    def get(self, request, *args, **kwargs):
        context = {

        }
        return render(request, self.template_name, context)


class Register(View):
    form_class = RegisterForm
    template_name = 'secret_photo/register.html'

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('/')
        form = self.form_class()
        return render(request, self.template_name, {'form': form})


class RegisterCreate(APIView):
    form_class = RegisterForm
    # authentication_classes = [TokenAuthentication]
    # permission_classes = [IsAuthenticated]

    # @csrf_exempt
    def post(self, request, *args, **kwargs):
        custom_user = get_user_model()
        print(request.POST)
        form = self.form_class(request.POST)

        try:
            if form.is_valid():
                data = request.POST
                print(data)
                coordinates = json.loads(data['coordinates'])
                print(coordinates)
                sorted_data = sorted(
                    coordinates, key=lambda item: (item[0], item[1]))
                coordinates = json.dumps(sorted_data)
                print(coordinates)
                data_dict = {
                    'email': data['email'],
                    'number_of_click': int(
                        form.cleaned_data['number_of_click']),
                    'image_data': request.FILES['img_photo']
                }
                serializer = serializers.CustomUserSerializer(
                    data=data_dict)
                serializer.is_valid(raise_exception=True)
                # data = serializers.validate_and_enrich(serializer.data)
                user = custom_user.objects.filter(
                    email=serializer.validated_data.get('email'))
                if not user:
                    profile = CustomUser()
                    profile.user_key = uuid.uuid4().hex
                    profile.email = serializer.validated_data.get('email')
                    profile.password = \
                        CustomUser().get_click_coordinates_hash(coordinates)
                    profile.image_data = CustomUser().encrypt_image_data(
                        serializer.validated_data.get('image_data'),
                        settings.AUTHEN_SECRET_KEY.encode('utf-8'))
                    profile.number_of_click = serializer.validated_data.get(
                        'number_of_click')
                    profile.save()
                    return JsonResponse({
                        'status': 'success',
                        'message': 'Registered successfully.'})
                else:
                    return JsonResponse({
                        'status': 'Error',
                        'message': f'Email already registered.'})
            else:
                return JsonResponse({
                    'status': 'Error',
                    'message': 'Invalid Form.'})
        except Exception as e:
            print(e)
            return JsonResponse({
                'status': 'Error',
                'message': str(e)},  status=400)


class Login(View):
    form_class = LoginForm
    template_name = 'secret_photo/login.html'

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('/')
        form = self.form_class()
        return render(request, self.template_name, {'form': form})


class Logout(View):

    def get(self, request, *args, **kwargs):
        logout(request)
        return HttpResponseRedirect('/')


class LoginAuthenticate(APIView):
    form_class = LoginForm
    # authentication_classes = [TokenAuthentication]
    # permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        custom_user = get_user_model()
        form = self.form_class(request.POST)
        data = request.POST
        print(data)
        if form.is_valid():
            try:
                coordinates = json.loads(data['coordinates'])
                print(coordinates)
                sorted_data = sorted(
                    coordinates, key=lambda item: (item[0], item[1]))
                coordinates = json.dumps(sorted_data)
                print(coordinates)
                password = CustomUser().get_click_coordinates_hash(coordinates)
                user = custom_user.objects.get(
                    email=data['email'], password=password)
                if user is not None:
                    login(request, user)
                    return JsonResponse({
                        'status': 'success',
                        'message': 'User logged in.'})
            except CustomUser.DoesNotExist as e:
                return JsonResponse({
                    'status': 'Error',
                    'message': 'Invalid Email or Coordinates.'},
                    status=401)

        else:
            return JsonResponse({
                'status': 'Error',
                'message': 'Invalid Form.'}, status=400)


# def logout_view(request):
#     logout(request)
#     print(request.user.is_authenticated)
#     return HttpResponseRedirect('/')


class ImgPreview(View):
    form_class = LoginForm

    def get(self, request, *args, **kwargs):
        form = self.form_class(request.GET)
        if form.is_valid():
            try:
                profile = CustomUser.objects.get(email=request.GET['email'])
                decrypted_data = CustomUser.decrypt_image_data(
                    profile.image_data,
                    settings.AUTHEN_SECRET_KEY.encode('utf-8'))
                context = {
                    'img64': base64.b64encode(decrypted_data).decode('utf-8'),
                    'number_of_click': profile.number_of_click
                }
                return JsonResponse(context)
            except CustomUser.DoesNotExist as e:
                return JsonResponse({
                    'status': 'Error',
                    'message': 'Invalid Email'},
                    status=401)
        else:
            return JsonResponse({
                'status': 'Error',
                'message': 'Invalid Form.'}, status=400)


class ForgotPassword(View):
    form_class = ForgotPasswordForm
    template_name = 'secret_photo/forgot_password.html'

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('/')
        form = self.form_class()
        return render(request, self.template_name, {'form': form})


class ResetPassword(APIView):
    form_class = ForgotPasswordForm
    # authentication_classes = [TokenAuthentication]
    # permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        custom_user = get_user_model()
        form = self.form_class(request.POST)
        data = request.POST
        print(data)
        if form.is_valid():
            try:
                user = custom_user.objects.get(email=data['email'])
                if user is not None:

                    return JsonResponse({
                        'status': 'success',
                        'message': 'Already send.'})
            except CustomUser.DoesNotExist as e:
                return JsonResponse({
                    'status': 'Error',
                    'message': 'Invalid Email.'},
                    status=401)

        else:
            return JsonResponse({
                'status': 'Error',
                'message': 'Invalid Form.'}, status=400)

# @api_view(['GET'])
# def get_img_preview(request):
#     print(request.GET)
#     email = request.GET['email']
#     profile = CustomUser.objects.get(email=email)
#     decrypted_data = CustomUser.decrypt_image_data(
#         profile.image_data, settings.AUTHEN_SECRET_KEY.encode('utf-8'))

#     # directory = os.getcwd()
#     # image_path = f'{directory}/order_reserve/static/assets/img/suite.png'
#     # with open(image_path, "rb") as image_file:
#     #     encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
#     # print(decrypted_data)
#     context = {
#         'img64': base64.b64encode(decrypted_data).decode('utf-8'),
#         'number_of_click': profile.number_of_click
#     }
#     # return render(request, 'secret_photo/homepage.html', context)
#     return JsonResponse(context)


# @api_view(['GET', 'POST'])
# def login_page(request):
#     encrypted_image = UserProfile.objects.get(id=7)
#     print(encrypted_image.image_data)
#     decrypted_data = UserProfile.decrypt_image_data(
#         encrypted_image.image_data,
#         settings.AUTHEN_SECRET_KEY.encode('utf-8'))
#     # directory = os.getcwd()
#     # image_path = f'{directory}/order_reserve/static/assets/img/suite.png'
#     # with open(image_path, "rb") as image_file:
#     #     encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
#     # print(decrypted_data)
#     context = {
#         'img64': base64.b64encode(decrypted_data).decode('utf-8')
#     }
#     return render(request, 'secret_photo/homepage.html', context)

# @csrf_exempt
# @login_required
# def register_coordinates(request):
#     if request.method == 'POST':
#         data = json.loads(request.body)
#         coordinates = data.get('coordinates')

#         # Get the user's profile
#         profile, created = UserProfile.objects.get_or_create(
#             username=request.username)

#         # Set the click coordinates
#         profile.set_click_coordinates(coordinates)
#         profile.save()

#         return JsonResponse({
#             'status': 'success',
#             'message': 'Coordinates registered successfully!'})

#     else:
#         return JsonResponse({'status': 'failed',
#                              'message': 'Invalid request method!'})


# @csrf_exempt
# def authenticate(request):
#     if request.method == 'POST':
#         data = json.loads(request.body)
#         username = data.get('username')
#         # password = data.get('password')
#         coordinates = data.get('coordinates')
#         # First, authenticate the user using Django's built-in authentication
#         # user = authenticate(request, username=username)
#         profile = CustomUser.objects.get(username=username)
#         if username is not None:
#             # If the user is authenticated, compare the click coordinates hash
#             # profile = UserProfile.objects.get(user=user)
#             if profile.check_click_coordinates(coordinates):
#                 response = {'status': 'success',
#                             'message': 'Authentication successful!'}
#             else:
#                 response = {'status': 'failed',
#                             'message': 'Click coordinates do not match!'}
#         else:
#             response = {'status': 'failed',
#                         'message': 'Invalid username or password!'}

#         return JsonResponse(response)

#     else:
#         return JsonResponse({'status': 'failed',
#                              'message': 'Invalid request method!'})


def cookie_popup(request):
    if request.user.is_authenticated:
        try:
            consent = CookieConsent.objects.get(user=request.user)
        except CookieConsent.DoesNotExist:
            consent = None
    else:
        consent = None

    return render(request, 'cookie_popup.html', {'consent': consent})


def give_consent(request):
    if request.user.is_authenticated:
        try:
            consent = CookieConsent.objects.get(user=request.user)
            consent.consent_given = True
            consent.save()
        except CookieConsent.DoesNotExist:
            CookieConsent.objects.create(user=request.user, consent_given=True)

    return HttpResponse("Consent given successfully.")


def addphoto(request):
    return render(request, 'secret_photo/addphoto.html')


# def gallery(request):
#     return render(request, 'secret_photo/gallery.html')


def picture_description_view(request):
    if request.method == 'POST':
        form = PictureDescriptionForm(request.POST, request.FILES)
        if form.is_valid():
            image = form.cleaned_data['picture']
            description = form.cleaned_data['description']
            new_image = PictureDescription(
                picture=image, description=description)
            new_image.save()

            return HttpResponseRedirect('/gallery')
    else:
        form = PictureDescriptionForm()
    # Check the template name here
    return render(request, 'secret_photo/picture_description.html',
                  {'form': form})


def gallery(request):
    all_data = PictureDescription.objects.all().order_by('-id')
    return render(request, 'secret_photo/gallery.html', {'data': all_data})


def picture_detail(request, image_id):
    image = get_object_or_404(PictureDescription, pk=image_id)
    return render(request, 'secret_photo/details.html', {'image': image})
