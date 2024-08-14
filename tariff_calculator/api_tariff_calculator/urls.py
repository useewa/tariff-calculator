from django.urls import path
from .views import TariffCalculatorView

urlpatterns = [
    path('calc/', TariffCalculatorView.as_view(), name='tariff_calculator'),
]