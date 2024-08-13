#--------------------------------------
# Imports.
#--------------------------------------

from commons.models import Search
from rest_framework import serializers

#--------------------------------------
# Serializers.
#--------------------------------------

# Create Search Serializer.
class SearchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Search
        fields = ('area', 'prompt')

# Create Query Serializer.
class QuerySerializer(serializers.Serializer):
    prompt = serializers.CharField(max_length=322)

# Create Knowledge Updater Serializer.
class KUpdateSerializer(serializers.Serializer):
    document = serializers.CharField(max_length=1500000)