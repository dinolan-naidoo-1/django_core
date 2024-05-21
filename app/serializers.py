from rest_framework import serializers
from .models import TransactionData

class TransactionSerializer(serializers.Serializer):
    file = serializers.FileField()