from django.utils import timezone
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import TariffCalculationSerializer
from .models import CalculationLog
import math

from django.core.cache import cache

class TariffCalculatorView(APIView):
    def post(self, request):
        serializer = TariffCalculationSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data

            tariff_unit = data['TariffUnit']
            tariff_unit_price = float(data['TariffUnitPrice'])
            started_at = data['Started_at']
            last_payment_time = data.get('LastPaymentTime', started_at)
            deposit = float(data['Deposit'])

            cache_key = f"{tariff_unit}_{tariff_unit_price}_{started_at}_{last_payment_time}_{deposit}"
            result = cache.get(cache_key)

            if not result:
                current_time = timezone.now()
                session_time = max(current_time, last_payment_time) - started_at
                session_duration = session_time.total_seconds()

                duration_units = {
                    'Минута': math.ceil(session_duration / 60),
                    'Час': math.ceil(session_duration / 3600),
                    'День': math.ceil(session_duration / 86400),
                    'Неделя': math.ceil(session_duration / 604800)
                }.get(tariff_unit, 0)

                cost = deposit - (duration_units * tariff_unit_price)
                unpaid_duration = max(0, (duration_units * {
                    'Минута': 60,
                    'Час': 3600,
                    'День': 86400,
                    'Неделя': 604800
                }.get(tariff_unit, 0)) - session_duration)

                log_entry = CalculationLog.objects.create(
                    tariff_unit=tariff_unit,
                    tariff_unit_price=tariff_unit_price,
                    started_at=started_at,
                    last_payment_time=last_payment_time,
                    deposit=deposit,
                    duration=int(session_duration),
                    unpaid_duration=int(unpaid_duration),
                    cost=cost
                )

                result = {
                    'Duration': int(session_duration),
                    'UnpaidDuration': int(unpaid_duration),
                    'Cost': cost
                }

                cache.set(cache_key, result, timeout=60 * 15)

            return Response(result, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)