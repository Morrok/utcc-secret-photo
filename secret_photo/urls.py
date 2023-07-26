from django.urls import path
# from .views import index, index2,
from secret_photo import views
# from .views import ContactWizard
# from django.conf import settings
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include


app_name = 'secret_photo'

urlpatterns = [
    path('', views.Home.as_view(), name='homepage'),
    path('register/', views.Register.as_view(), name='register'),
    path('register/create/', views.RegisterCreate.as_view(),
         name='register_create'),

    path('authenticate/', views.authenticate, name='authenticate'),
    # path('contact/', views.ContactWizard.as_view(), name='contact'),
    path('popup/', views.cookie_popup, name='popup'),
    path('give_consent/', views.give_consent, name='give_consent'),
    # path('secret-photo/tonhom', views.index_tonhom),
    # path('secret-photo/kim', views.index_kim),
    # path('secret-photo/best', views.index_best),
    # path('secret-photo/authenticate/', views.authen_function),
    # path('secret-photo/register_page', views.register, name='register')
    # path('test2', views.index2),
    # path('api/login', views.LoginApiView.as_view(), name='login'),
    path('picture_description/gallery/', views.gallery, name='gallery'),
    path('picture_description/', views.picture_description_view,
         name='picture_description'),
]
