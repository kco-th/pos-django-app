# myapp/serializers.py
from rest_framework import serializers
from .models import Product
#To convert model data to JSON data
class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product

        fields = [
            'id',
            'name',
            'category',
            'unit',
            'price',
            'stock',
            'description',
            'is_active',
        ]