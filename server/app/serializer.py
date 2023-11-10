from rest_framework import serializers
from .models import Data


class DataSerializer(serializers.ModelSerializer):
    class Meta:
        model = Data  # 모델 설정
        fields = '__all__'  # 필드 설정
