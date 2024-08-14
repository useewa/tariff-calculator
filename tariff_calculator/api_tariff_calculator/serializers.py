from rest_framework import serializers

class TariffCalculationSerializer(serializers.Serializer):
    TariffUnit = serializers.ChoiceField(choices=['Минута', 'Час', 'День', 'Неделя'])
    TariffUnitPrice = serializers.DecimalField(max_digits=10, decimal_places=2)
    Started_at = serializers.DateTimeField()
    LastPaymentTime = serializers.DateTimeField(required=False, allow_null=True)
    Deposit = serializers.DecimalField(max_digits=10, decimal_places=2)