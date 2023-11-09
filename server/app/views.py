from django.shortcuts import render
from .models import Data
from django.conf import settings
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
