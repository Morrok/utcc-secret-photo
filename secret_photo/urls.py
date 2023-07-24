from django.urls import path
# from .views import index, index2,
from secret_photo import views
# from .views import ContactWizard
# from django.conf import settings

app_name = 'secret_photo'

urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('register/', views.register, name='register'),
    path('authenticate/', views.authenticate, name='authenticate'),
    # path('contact/', views.ContactWizard.as_view(), name='contact'),
    # path('secret-photo/tonhom', views.index_tonhom),
    # path('secret-photo/kim', views.index_kim),
    # path('secret-photo/best', views.index_best),
    # path('secret-photo/authenticate/', views.authen_function),
    # path('secret-photo/register_page', views.register, name='register')
    # path('test2', views.index2),
    # path('api/login', views.LoginApiView.as_view(), name='login')
]
