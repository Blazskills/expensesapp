from django.db.models import fields
from rest_framework import serializers
from .models import Income


class IncomeSerializer(serializers.ModelSerializer):
    # description = serializers.CharField(
    #     max_length=255, min_length=2)
    class Meta:
        model = Income
        fields = ['id','date', 'description', 'amount', 'source']
    # def validate(self, attrs):
    #     description = attrs.get('description', '')
    #     if len(description) < 2:
    #         raise serializers.ValidationError(
    #             'The username should be greater than 2') 
    #     return attrs