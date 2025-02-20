from rest_framework import serializers
from .models import Rating



class RateSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Rating
        fields = ['user','recipe','stars']
        extra_kwargs = {
            'user':{'read_only':True}, 
            'recipe':{'read_only':True}, 

        }


   