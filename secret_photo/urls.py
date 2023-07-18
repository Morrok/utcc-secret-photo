from django.urls import path
# from .views import index, index2,
from secret_photo import views

urlpatterns = [
    path('secret-photo/tonhom', views.index_tonhom),
    path('secret-photo/kim', views.index_kim),
    path('secret-photo/best', views.index_best),
    path('secret-photo/authenticate/', views.authen_function),
    path('secret-photo/register_page', views.register, name='register')
    # path('test2', views.index2),
    # path('api/login', views.LoginApiView.as_view(), name='login')
]
