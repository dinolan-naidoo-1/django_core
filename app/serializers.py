from rest_framework import serializers
from .models import TransactionData

# This serializer class is primitive at the moment, but can be expanded if more complexity is introduced

class TransactionSerializer(serializers.Serializer):
    file = serializers.FileField()