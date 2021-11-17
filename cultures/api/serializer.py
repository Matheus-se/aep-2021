from cultures.models import Culture, UserCultures
from rest_framework import serializers

class CultureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Culture
        fields = ['id', 'name', 'basal_sup', 'basal_inf', 'thermal_constant']
        
class UserCultureSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = UserCultures
        fields = ['id', 'accumulated_degrees']

class VinculatedUserCultureSerializer(serializers.ModelSerializer):
    
    culture = CultureSerializer()
    
    class Meta:
        model = UserCultures
        fields = ['id', 'accumulated_degrees', 'culture']
