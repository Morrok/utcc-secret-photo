from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
# from django.contrib.auth import authenticate, login
from .models import User
from .serializers import UserSerializer
from rest_framework.decorators import api_view
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse

def homepage(request):
    context = {

    }
    print('test')
    return render(
        request, 'secret_photo/homepage.html', context)

def index_tonhom(request):
    return render(request, 'index_tonhom.html')

def index_kim(request):
    return render(request, 'index_kim.html')

def index_best(request):
    return render(request, 'index_best.html')

def authen_function(request):
    return render(request, 'index_best.html')


# def register_get(request):
#     if request.method == 'GET':
#          return render(request, 'register.html')
    

# def register(request):
#     if request.method == 'POST':
#         username = request.POST.get('username')
#         email = request.POST.get('email')
#         password1 = request.POST.get('password1')
#         password2 = request.POST.get('password2')

#         if password1 != password2:
#             messages.error(request, 'Passwords do not match.')
#             return redirect('register')

#         # Check if the username is already taken
#         if User.objects.filter(username=username).exists():
#             messages.error(request, 'Username is already taken.')
#             return redirect('register')

#         # Check if the email is already in use
#         if User.objects.filter(email=email).exists():
#             messages.error(request, 'Email is already in use.')
#             return redirect('register')

#         # Create the user account
#         user = User.objects.create_user(username=username, email=email, password=password1)
#         user.save()
#         messages.success(request, 'Account created successfully. You can now log in.')
#         return redirect('login')
    
#     return render(request, 'register.html')




@api_view(['GET', 'POST'])
def register(request):
    # print("Hello")
    if request.method == 'POST':
        serializer = UserSerializer(data=request.POST)
        if serializer.is_valid():
            serializer.save()
            return redirect('/login')
        else:
            return JsonResponse({'error': 'Internal Error'}, status=500)
    
    return render(request, 'register.html')
