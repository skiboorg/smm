from rest_framework import serializers
from .models import *

class ServiceSerializer(serializers.ModelSerializer):
    price = serializers.DecimalField(source='get_low_price',read_only=True,decimal_places=2,max_digits=5,required=False)
    price_w_discount = serializers.DecimalField(source='get_discount',read_only=True,decimal_places=2,max_digits=5,required=False)
    tarif_id = serializers.IntegerField(source='get_tarif_id',read_only=True,required=False)
    class Meta:
        model = Service
        fields = [
            'id',
            'name',
            'price',
            'price_w_discount',
            'tarif_id'
        ]


class NetworksSerializer(serializers.ModelSerializer):
    services = ServiceSerializer(many=True)
    class Meta:
        model = SocialNetwork
        fields = [
            'id',
            'discount',
            'name',
            'icon',
            'slogan',
            'created_at',
            'services',
        ]

class TafifSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tarif
        fields = '__all__'

class ServicesSerializer(serializers.ModelSerializer):
    tarifs = TafifSerializer(many=True)
    class Meta:
        model = Service
        fields = [
            'id',
            'name',
            'tarifs'
        ]

class NetworkSerializer(serializers.ModelSerializer):
    services = ServicesSerializer(many=True)
    class Meta:
        model = SocialNetwork
        fields = [
            'id',
            'discount',
            'name',
            'icon',
            'slogan',
            'created_at',
            'services',
        ]









