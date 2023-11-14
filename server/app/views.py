from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from .models import Data
import os

# Create your views here.


def view(request):
    data_list = Data.objects.order_by('-id')
    context = {'data_list': data_list}
    return render(request, 'view.html', context)


def detail(request, user_id):
    data = Data.objects.get(user_id=user_id)
    context = {'data': data}
    return render(request, 'detail.html', context)


@csrf_exempt
def register(request):
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
