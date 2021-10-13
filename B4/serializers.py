from rest_framework.serializers import ModelSerializer
from . import models


class DefaultDeductionsModelSerializer(ModelSerializer):
    class Meta:
        model = models.DefaultDeductions
        fields = ['house', 'travel', 'phone', 'food']
