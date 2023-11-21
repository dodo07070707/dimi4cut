from django.http import JsonResponse, HttpRequest
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect
from .models import Data
import os

# Create your views here.


def index(request: HttpRequest):
    return render(request, 'index.html')


def get_input(request: HttpRequest):
    if request.method == 'POST':
        input_id = request.POST.get('user_id')
        input_pw = request.POST.get('password')

        try:
            data = Data.objects.get(user_id=int(input_id))
            if data.pw == input_pw:
                request.session['user_id'] = data.user_id
                return redirect('detail')
        except:
            pass
        return redirect('/')


def detail(request: HttpRequest):
    user_id = request.session.get('user_id')
    data = Data.objects.get(user_id=user_id)
    context = {'data': data}
    return render(request, 'image_show.html', context)


@csrf_exempt
def register(request: HttpRequest):
    print(request.method)
    if request.method == 'POST':
        try:
            received_data = request.POST.dict()

            user_id = received_data.get('user_id')
            pw = received_data.get('pw')
            image = request.FILES.get('image')

            data = Data(user_id=user_id, pw=pw, image=image)
            data.save()

            response_data = {'status': 'success', 'message': 'data saved'}
            return JsonResponse(response_data, status=200)
        except Exception as e:
            response_data = {'status': 'error', 'message': str(e)}
            return JsonResponse(response_data, status=400)
    elif request.method == 'GET':
        response_data = {'status': 'success', 'message': ''}
        return JsonResponse(response_data, status=200)
    else:
        response_data = {'status': 'error', 'message': 'wrong request method'}
        return JsonResponse(response_data, status=405)
