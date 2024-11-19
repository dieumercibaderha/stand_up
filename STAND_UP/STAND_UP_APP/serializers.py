from rest_framework import serializers
from .models import *

class AlerteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Alerte
        fields = '__all__'
        
class MaladieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Maladie
        fields = '__all__'
        
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
