from rest_framework import serializers, status
from rest_framework.authtoken.models import Token
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.generics import ListAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes

from farmer.models import Farmer

from .api.serializer import AccountSerializer, FarmerSerializer

@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def farmer_account_view(request):
    try: 
        farmer = request.user
    except Farmer.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)    
    
    if request.method == 'GET':
        serializer = AccountSerializer(farmer)
        return Response(serializer.data)

@api_view(['GET', ])
@permission_classes(())
def list_farmers_view(request, id):
    
    try: 
        farmer = Farmer.objects.get(id=id)
    except Farmer.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        serializer = FarmerSerializer(farmer)
        return Response(serializer.data, status=status.HTTP_200_OK)

class FarmerListView(ListAPIView):
    queryset = Farmer.objects.all()
    serializer_class = FarmerSerializer
    pagination_class = PageNumberPagination
    authentication_classes = ()
    permission_classes = ()
    filter_backends = (SearchFilter, OrderingFilter)
    search_fields = ('username', 'email', 'cpf')

@api_view(['POST', ])
@permission_classes(())
def register_farmer_view(request):
    
    if request.method == "POST":
        serializer = FarmerSerializer(data=request.data)
        data = {}
        if serializer.is_valid():
            user = serializer.save()
            data['email'] = user.email
            data['username'] = user.username
            data['token'] = Token.objects.get(user=user).key
            return Response(data, status=status.HTTP_201_CREATED)
        data['error'] = serializer.errors
        return Response(data, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['PUT', ])
@permission_classes((IsAuthenticated,))
def update_farmer_view(request):
    
    try:
        farmer = request.user
    except Farmer.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if request.method == "PUT":
        serializer = AccountSerializer(farmer, data=request.data)
        data = {}
        if serializer.is_valid():
            serializer.save()            
            data['message'] = 'Updated success'
            return Response(data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['DELETE', ])
@permission_classes((IsAuthenticated,))
def delete_farmer_view(request):
    
    try: 
        farmer = request.user
    except Farmer.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'DELETE':
        deleted = farmer.delete(); 
        data = {}
        if deleted:
            data['message'] = "vendor deleted"
            return Response(data=data, status=status.HTTP_200_OK)
        data['error'] = "Delete failed"
        return Response(status=status.HTTP_400_BAD_REQUEST)