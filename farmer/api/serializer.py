from rest_framework import serializers
from farmer.models import Farmer

from cultures.api.serializer import VinculatedUserCultureSerializer

class FarmerSerializer(serializers.ModelSerializer):
    
    cultures = VinculatedUserCultureSerializer(many=True)
    
    class Meta:
        model = Farmer
        fields = ['id', 'username', 'email', 'password', 'cpf', 'cultures']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    #Needed for hash the password
    def create(self, validated_data):
        user = Farmer(
            email=validated_data['email'],
            username=validated_data['username'],
            cpf=validated_data['cpf'],
        )
        user.set_password(validated_data['password'])
        user.save()
            
        return user
    
class AccountSerializer(serializers.ModelSerializer):    
        
    class Meta:
        model = Farmer
        fields = ['id', 'username', 'email', 'cpf']