from rest_framework import serializers
from .models import SoldHouse


class SoldHouseSerializer(serializers.ModelSerializer):
    price_paid = serializers.IntegerField()
    property_type = serializers.CharField(max_length=250)
    tx_date = serializers.DateField()

    class Meta:
        model = SoldHouse
        fields = [
            'price_paid',
            'property_type',
            'tx_date',
        ]
