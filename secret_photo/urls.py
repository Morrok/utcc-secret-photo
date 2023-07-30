from django.urls import path
from secret_photo import views

app_name = 'secret_photo'

urlpatterns = [
    path('', views.HomeView.as_view(), name='homepage'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('register/create/', views.RegisterCreate.as_view(),
         name='register_create'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.Logout.as_view(), name='logout'),
    path('login/authenticate/', views.LoginAuthenticate.as_view(),
         name='authenticate'),
    path('login/img_preview/', views.ImgPreviewView.as_view(),
         name='img_preview'),
    path('login/forgot_password/',
         views.ForgotPasswordView.as_view(), name='forget_password'),
    path('login/forgot_password/reset_password',
         views.ResetPassword.as_view(), name='reset_password'),
    path('login/forgot_password/reset_password_view/' +
         '<str:uidb64>/<str:token>',
         views.ResetPasswordView.as_view(), name='reset_password_view'),
    path('login/forgot_password/reset_password_confirm/' +
         '<str:uidb64>/<str:token>',
         views.ResetPasswordConfirm.as_view(), name='reset_password_confirm'),
    path('popup/', views.cookie_popup, name='popup'),
    path('give_consent/', views.give_consent, name='give_consent'),
    path('upload/', views.upload_photo,
         name='upload'),
    path('gallery/', views.gallery, name='gallery'),
    path('detail/<int:pk>/', views.photo_detail, name='details'),
]
