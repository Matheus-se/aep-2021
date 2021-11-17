from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.generics import ListAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.permissions import IsAuthenticated


from cultures.models import Culture, UserCultures
from .api.serializer import CultureSerializer, UserCultureSerializer, VinculatedUserCultureSerializer

@api_view(['GET', ])
@permission_classes(())
def get_culture_view(request, id):
    
    try: 
        culture = Culture.objects.get(id=id)
    except Culture.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        serializer = CultureSerializer(culture)
        return Response(serializer.data, status=status.HTTP_200_OK)

class CultureListView(ListAPIView):
    queryset = Culture.objects.get_queryset().order_by('id')
    serializer_class = CultureSerializer
    pagination_class = PageNumberPagination
    authentication_classes = ()
    permission_classes = ()
    filter_backends = (SearchFilter, OrderingFilter)
    search_fields = ('name', 'basal_inf', 'basal_sup', 'id', 'thermal_constant')
    
    class Meta:
        ordering = ['-id']

@api_view(['PUT', ])
@permission_classes((IsAuthenticated,))
def update_culture_view(request, id):
    
    try: 
        culture = Culture.objects.get(id=id)
    except Culture.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    user = request.user
    if not user.is_superuser or not user.is_staff:
        return Response({'error': "You don't have permission to edit this culture"})
    
    if request.method == 'PUT':
        serializer = CultureSerializer(culture, data=request.data)
        data = {}
        if serializer.is_valid():
            serializer.save()
            data['message'] = "culture updated"
            return Response(data=data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['DELETE', ])
@permission_classes((IsAuthenticated,))
def delete_culture_view(request, id):
    
    try: 
        culture = Culture.objects.get(id=id)
    except Culture.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    user = request.user
    if not user.is_superuser or not user.is_staff:
        return Response({'error': "You don't have permission to delete this culture"})
    
    if request.method == 'DELETE':
        deleted = culture.delete(); 
        data = {}
        if deleted:
            data['message'] = "culture deleted"
            return Response(data=data, status=status.HTTP_200_OK)
        data['error'] = "Delete failed"
        return Response(status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['POST', ])
@permission_classes((IsAuthenticated,))
def post_culture_view(request):
    
    user = request.user
        
    if not user.is_superuser or not user.is_staff:
        return Response({'error': "You don't have permission to create this culture"})

    culture = Culture()
    
    if request.method == 'POST':
        serializer = CultureSerializer(culture, data=request.data)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST', ])
@permission_classes((IsAuthenticated,))
def vinculate_culture_view(request):
    
    user = request.user
    
    params = request.data

    if not params['cultureId']:
        return Response({'error': 'cultureId required'}, status=status.HTTP_400_BAD_REQUEST)
    
    try: 
        culture = Culture.objects.get(id=params['cultureId'])
    except Culture.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    userCulture = UserCultures(farmer=user, culture=culture)
    
    if request.method == 'POST':
        serializer = VinculatedUserCultureSerializer(userCulture, data=request.data)
        
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "culture successfully vinculated", 'data': serializer.data}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT', ])
@permission_classes((IsAuthenticated,))
def update_degrees_view(request, id):

    
    try:
        degrees = request.data['accumulated_degrees']
    except:
        return Response({'error': 'accumulated_degrees is required'}, status=status.HTTP_200_OK)
        
    try: 
        culture = UserCultures.objects.get(id=id)
    except UserCultures.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    user = request.user
    if culture.farmer != user:
        return Response({'error': "You don't have permission to update this user culture"}) 
    
    data = {'accumulated_degrees': degrees}
    
    if request.method == 'PUT':
        serializer = UserCultureSerializer(culture, data=data, partial=True)
        data = {}
        if serializer.is_valid():
            serializer.save()
            data['message'] = "accumulated degrees updated"
            return Response(data=data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)