# serializers.py
from rest_framework import serializers
from .models import Table3View

class Table3Serializer(serializers.ModelSerializer):
    class Meta:
        model = Table3View
        fields = '__all__'


from .models import Table4

class Table4Serializer(serializers.ModelSerializer):
    class Meta:
        model = Table4
        fields = '__all__'


from .models import Table7

class Table7Serializer(serializers.ModelSerializer):
    class Meta:
        model = Table7
        fields = '__all__'
