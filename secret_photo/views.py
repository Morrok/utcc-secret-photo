from django.shortcuts import render
# from django.http import JsonResponse
# from django.contrib.auth import authenticate, login
# from django.views.decorators.csrf import csrf_exempt
# from rest_framework.authtoken.models import Token
# from django.contrib.auth.mixins import LoginRequiredMixin
# # from django.views import View
# from rest_framework.views import APIView


def index(request):
    return render(request, 'index.html')