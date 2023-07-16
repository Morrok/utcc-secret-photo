from django.urls import path
# from .views import index, index2,
from secret_photo import views

urlpatterns = [
    path('', views.index),
    # path('test2', views.index2),
    # path('api/login', views.LoginApiView.as_view(), name='login')
]
