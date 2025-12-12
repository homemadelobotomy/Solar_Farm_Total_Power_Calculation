from rest_framework import serializers

class PanelCalculationSerializer(serializers.Serializer):
    area = serializers.FloatField(required=True)
    power = serializers.FloatField(required=True)
    height = serializers.IntegerField(required=True)
    width = serializers.IntegerField(required=True)

class CalculationRequestSerializer(serializers.Serializer):
    panels = PanelCalculationSerializer(many=True, required=True)
    insolation = serializers.FloatField(required=True)