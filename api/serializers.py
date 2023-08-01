from rest_framework import serializers
from .models import elevator,Person
class ElevatorSerializer(serializers.ModelSerializer):
    class Meta:
        model=elevator
        fields='__all__'
class PersonSerializer(serializers.ModelSerializer):
    class Meta:
        model=Person
        fields='__all__'
        