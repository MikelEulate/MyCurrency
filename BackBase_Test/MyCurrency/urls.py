from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CurrencyViewSet, CurrencyExchangeRateViewSet, ConvertCurrencyViewSet, ProviderViewSet

# Router para los viewsets
router = DefaultRouter()
router.register(r'currencies', CurrencyViewSet, basename='currency')
router.register(r'providers', ProviderViewSet, basename='provider')
router.register(r'exchange-rates', CurrencyExchangeRateViewSet, basename='exchange-rate')

urlpatterns = [
    path('', include(router.urls)),  # Incluye las rutas generadas por el router
    path('convert/', ConvertCurrencyViewSet.as_view({'get': 'convert'}), name='convert-currency'),
]
