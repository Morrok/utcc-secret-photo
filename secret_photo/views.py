from django.shortcuts import render, redirect, get_object_or_404
from rest_framework.views import APIView, View
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
import json
from .models import (
    CustomUser,
    CookieConsent,
    PictureDescription,
    register_user,
    reset_password
)
import base64
from django.conf import settings
from .forms import (
    RegisterForm,
    LoginForm,
    ForgotPasswordForm,
    ResetPasswordConfirmForm,
    PictureDescriptionForm
)
# from rest_framework.authentication import TokenAuthentication
# from rest_framework.permissions import IsAuthenticated
import uuid
from django.http import HttpResponseRedirect
from django.contrib.auth import login, logout
from django.contrib.auth import get_user_model
from secret_photo import serializers
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.utils.encoding import force_str as force_text


class HomeView(View):
    template_name = 'secret_photo/homepage.html'

    def get(self, request, *args, **kwargs):
        context = {

        }
        return render(request, self.template_name, context)


class RegisterView(View):
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

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)

        try:
            if form.is_valid():
                data = request.POST
                data_dict = {
                    'email': data['email'],
                    'number_of_click': int(
                        form.cleaned_data['number_of_click']),
                    'image_data': request.FILES['img_photo']
                }
                serializer = serializers.CustomUserSerializer(
                    data=data_dict)
                serializer.is_valid(raise_exception=True)
                result = register_user(
                    serializer.validated_data, data['coordinates'])
                if result:
                    return JsonResponse({
                        'error_code': 'success',
                        'message': 'Registered successfully.'})
                else:
                    return JsonResponse({
                        'error_code': 'duplicate',
                        'message': f'Email already registered.'}, status=400)
            else:
                return JsonResponse({
                    'error_code': 'error',
                    'message': 'Invalid Form.'})
        except Exception as e:
            print(e)
            return JsonResponse({
                'error_code': 'error',
                'message': str(e)},  status=400)


class LoginView(View):
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
                        'error_code': 'error',
                        'message': 'User logged in.'})
            except CustomUser.DoesNotExist as e:
                return JsonResponse({
                    'error_code': 'error',
                    'message': 'Invalid Email or Coordinates.'},
                    status=401)

        else:
            return JsonResponse({
                'error_cdoe': 'error',
                'message': 'Invalid Form.'}, status=400)


class ImgPreviewView(View):
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
                    'error_code': 'error',
                    'message': 'Invalid Email'},
                    status=401)
        else:
            return JsonResponse({
                'error_code': 'error',
                'message': 'Invalid Form.'}, status=400)


class ForgotPasswordView(View):
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
                    print('test1')
                    subject = 'Password Reset for Cloaked Moments'
                    template_name = 'email_template/password_reset_email.html'
                    from_email = settings.EMAIL_HOST_USER
                    to_email = [data['email']]
                    context = {
                        'protocol': settings.WEB_PROTOCAL,
                        'domain': settings.WEB_DOMAIN_NAME,
                        'uid': urlsafe_base64_encode(
                            force_bytes(user.user_key)),
                        'token': default_token_generator.make_token(user),
                    }
                    email_content = render_to_string(template_name, context)
                    plain_message = strip_tags(email_content)

                    send_mail(subject, plain_message, from_email,
                              to_email, html_message=email_content)
                    print('test2')
                    return JsonResponse({
                        'error_code': 'success',
                        'message': 'Already send.'})
            except CustomUser.DoesNotExist as e:
                return JsonResponse({
                    'error_code': 'Error',
                    'message': 'Invalid Email.'},
                    status=401)

        else:
            return JsonResponse({
                'error_code': 'Error',
                'message': 'Invalid Form.'}, status=400)


class ResetPasswordView(View):
    form_class = ResetPasswordConfirmForm
    template_name = 'secret_photo/reset_password.html'

    def get(self, request, uidb64, token, *args, **kwargs):
        print('test')
        if request.user.is_authenticated:
            return redirect('/')

        try:
            uid = force_text(urlsafe_base64_decode(uidb64))
            print(uid)
            user = get_user_model().objects.get(user_key=uid)
        except (TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
            user = None

        user_dict = {
            'email': user.email
        }
        form = self.form_class(user_dict)
        if user is not None and \
                default_token_generator.check_token(user, token):
            return render(request, self.template_name,
                          {'form': form, 'uidb64': uidb64, 'token': token})
        else:
            return render(request, 'secret_photo/invalid_link.html')


class ResetPasswordConfirm(View):
    form_class = ResetPasswordConfirmForm

    def post(self, request, uidb64, token):
        # custom_user = get_user_model()
        print(request.POST)
        print(uidb64, token)
        try:
            uid = force_text(urlsafe_base64_decode(uidb64))
            user = get_user_model().objects.get(user_key=uid)
        except (TypeError, ValueError, OverflowError,
                CustomUser.DoesNotExist) as e:
            user = None
            return JsonResponse({
                'error_code': 'error',
                'message': str(e)},  status=400)

        if user is not None and default_token_generator.check_token(
                user, token):
            try:
                form = self.form_class(request.POST)
                if form.is_valid():
                    data = request.POST
                    data_dict = {
                        'email': data['email'],
                        'number_of_click': int(
                            form.cleaned_data['number_of_click']),
                        'image_data': request.FILES['img_photo']
                    }
                    serializer = serializers.CustomUserSerializer(
                        data=data_dict)
                    serializer.is_valid(raise_exception=True)
                    reset_password(user, serializer.validated_data,
                                   data['coordinates'])
                    # return redirect('password_reset_complete')
                    return JsonResponse({
                        'error_code': 'success',
                        'message': 'Reset password successfully.'})
                else:
                    return JsonResponse({
                        'error_code': 'Error',
                        'message': 'Invalid Form.'})
            except Exception as e:
                print(e)
                return JsonResponse({
                    'error_code': 'Error',
                    'message': str(e)},  status=400)

        return JsonResponse({
            'error_code': 'invalid_link',
            'message': f'The password reset link you used is invalid or' +
            f' has expired. Please try resetting your password again.'},
            status=400)


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
