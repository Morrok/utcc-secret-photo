from django.shortcuts import render, redirect
from rest_framework.views import APIView
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
    UserProfile,
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


class Home(APIView):
    form_class = RegisterForm
    template_name = 'secret_photo/homepage.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})


class Register(APIView):
    form_class = RegisterForm
    template_name = 'secret_photo/register.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})


class RegisterCreate(Register):
    # authentication_classes = [TokenAuthentication]
    # permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        tz = pytz.timezone('Asia/Bangkok')
        image = request.FILES['img_photo']
        print(request.FILES)
        data = request.POST
        print(data)
        form = self.form_class(request.POST)
        email = data['email']
        coordinates = json.loads(data['coordinates'])
        print(coordinates)
        sorted_data = sorted(
            coordinates, key=lambda item: (item[0], item[1]))
        coordinates = json.dumps(sorted_data)
        print(coordinates)

        try:
            if form.is_valid():
                number_of_click = int(form.cleaned_data['number_of_click'])
                profile = UserProfile.objects.filter(email=email)
                if not profile:
                    profile = UserProfile()
                    profile.email = email
                    profile.image_data = profile.encrypt_image_data(
                        image, settings.AUTHEN_SECRET_KEY.encode('utf-8'))
                    profile.click_coordinates_hash = \
                        profile.get_click_coordinates_hash(coordinates)
                    profile.number_of_click = number_of_click
                    profile.date_registered = datetime.datetime.now(tz)
                    profile.save()
                    return JsonResponse({
                        'status': 'success',
                        'message': 'Coordinates registered successfully!'})
                else:
                    return JsonResponse({
                        'status': 'Error',
                        'message': 'Already Created.'})
            else:
                return JsonResponse({
                    'status': 'Error',
                    'message': 'Someting Error.'})
        except Exception as e:
            return JsonResponse({
                'status': 'Error',
                'message': e})


class Login(APIView):
    form_class = LoginForm
    template_name = 'secret_photo/login.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})


@api_view(['GET'])
def get_img_preview(request):
    encrypted_image = UserProfile.objects.get(id=1)
    print(encrypted_image.image_data)
    decrypted_data = UserProfile.decrypt_image_data(
        encrypted_image.image_data,
        settings.AUTHEN_SECRET_KEY.encode('utf-8'))
    # directory = os.getcwd()
    # image_path = f'{directory}/order_reserve/static/assets/img/suite.png'
    # with open(image_path, "rb") as image_file:
    #     encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
    # print(decrypted_data)
    context = {
        'img64': base64.b64encode(decrypted_data).decode('utf-8'),
        'number_of_click': 4
    }
    # return render(request, 'secret_photo/homepage.html', context)
    return JsonResponse(context)


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
def authenticate(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data.get('username')
        # password = data.get('password')
        coordinates = data.get('coordinates')
        # First, authenticate the user using Django's built-in authentication
        # user = authenticate(request, username=username)
        profile = UserProfile.objects.get(username=username)
        if username is not None:
            # If the user is authenticated, compare the click coordinates hash
            # profile = UserProfile.objects.get(user=user)
            if profile.check_click_coordinates(coordinates):
                response = {'status': 'success',
                            'message': 'Authentication successful!'}
            else:
                response = {'status': 'failed',
                            'message': 'Click coordinates do not match!'}
        else:
            response = {'status': 'failed',
                        'message': 'Invalid username or password!'}

        return JsonResponse(response)

    else:
        return JsonResponse({'status': 'failed',
                             'message': 'Invalid request method!'})


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
            form.save()
            return redirect('gallery/')
    else:
        form = PictureDescriptionForm()
    # Check the template name here
    return render(request, 'secret_photo/picture_description.html', {'form': form})


def gallery(request):
    all_data = PictureDescription.objects.all()

    return render(request, 'secret_photo/gallery.html', {'data': all_data})
