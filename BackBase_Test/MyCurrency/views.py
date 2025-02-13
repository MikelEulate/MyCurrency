from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Currency, CurrencyExchangeRate, Provider
from .serializers import CurrencySerializer, CurrencyExchangeRateSerializer, ProviderSerializer
from .providers import get_exchange_rate_data


class CurrencyViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing CRUD operations for Currency model.
    """
    queryset = Currency.objects.all()
    serializer_class = CurrencySerializer

class ProviderViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing CRUD operations for Provider model.
    """
    queryset = Provider.objects.all()
    serializer_class = ProviderSerializer


class CurrencyExchangeRateViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for listing currency exchange rates within a specified time period.
    """
    queryset = CurrencyExchangeRate.objects.all()
    serializer_class = CurrencyExchangeRateSerializer

    def list(self, request):
        """
        Lists exchange rates for a given source currency and date range.

        Parameters:
        -----------
        request : Request
            The HTTP request object containing query parameters.

        Returns:
        --------
        Response
            The HTTP response containing serialized exchange rate data or an error message.
        """
        source_currency = request.query_params.get('source_currency')
        date_from = request.query_params.get('date_from')
        date_to = request.query_params.get('date_to')

        if not source_currency or not date_from or not date_to:
            return Response({"error": "Missing parameters"}, status=400)

        rates = CurrencyExchangeRate.objects.filter(
            source_currency__code=source_currency,
            valuation_date__range=[date_from, date_to]
        )

        serializer = self.get_serializer(rates, many=True)
        return Response(serializer.data)


class ConvertCurrencyViewSet(viewsets.ViewSet):
    """
    ViewSet for converting amounts between currencies.
    """
    @action(detail=False, methods=['get'])
    def convert(self, request):
        """
        Converts an amount from one currency to another.

        Parameters:
        -----------
        request : Request
            The HTTP request object containing query parameters.

        Returns:
        --------
        Response
            The HTTP response containing the converted amount or an error message.
        """
        source_currency = request.query_params.get('source_currency')
        exchanged_currency = request.query_params.get('exchanged_currency')
        amount = request.query_params.get('amount')
        date = request.query_params.get('date', None)

        if not source_currency or not exchanged_currency or not amount:
            return Response({"error": "Missing parameters"}, status=400)

        try:
            amount = float(amount)
        except ValueError:
            return Response({"error": "Invalid amount"}, status=400)

        rate = get_exchange_rate_data(source_currency, exchanged_currency, date)

        if rate is None:
            return Response({"error": "Exchange rate not available"}, status=404)

        converted_amount = amount * rate
        return Response({
            "source_currency": source_currency,
            "exchanged_currency": exchanged_currency,
            "rate": rate,
            "converted_amount": converted_amount
        })
