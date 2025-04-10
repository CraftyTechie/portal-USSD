from rest_framework import serializers
from .models import Student,Transaction,Fees
from django.conf import settings

class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = "__all__"
        
class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = "__all__"
        
class FeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Fees
        fields = "__all__"

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = settings.AUTH_USER_MODEL
        fields = ['first_name','last_name']
