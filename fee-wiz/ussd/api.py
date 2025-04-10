from rest_framework import generics
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.views.decorators.csrf import csrf_exempt
from .serializers import TransactionSerializer,StudentSerializer
from rest_framework.permissions import AllowAny
from rest_framework.decorators import permission_classes
from .models import Student,Transaction
from django.conf import settings
import re


@csrf_exempt
@api_view(["POST"])
def create_student(request):
    data = request.data
    serializer = StudentSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors)
@permission_classes([AllowAny])
@api_view()
def userProfile(request):
    user = request.user
    username = user.first_name
    return Response({
        'username': username
    })



def checkRegNo(regno):
    pattern = r'[A-Z][A-Z][A-Z]/[A-Z]/[0-9][0-9]-\d{5}/\d{4}'
    match = (re.match(pattern, regno))
    if match:
        return True
    else:
        return False
    
class TransactionView(generics.ListAPIView):
    serializer_class = TransactionSerializer
    queryset = Transaction.objects.exclude(mpesa_code__isnull=True).order_by('-created')
    permission_classes = [AllowAny]

class StudentsList(generics.ListAPIView):
    serializer_class = StudentSerializer
    queryset = Student.objects.all()
    permission_classes = [AllowAny]
