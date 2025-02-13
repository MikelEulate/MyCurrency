import random
import requests
import os

from django.conf import settings

from .models import Provider


class BaseProvider:
    """Base class for exchange rate providers."""

    def get_exchange_rate(self, source_currency, exchanged_currency, valuation_date, provider):
        """
        Abstract method to get the exchange rate between two currencies.

        Parameters:
        -----------
        source_currency : str
            The source currency code.
        exchanged_currency : str
            The exchanged currency code.
        valuation_date : datetime or None
            The date for which the exchange rate is needed.
        provider : str
            The name of the provider.

        Returns:
        --------
        float
            The exchange rate between the source and exchanged currencies.
        """
        raise NotImplementedError("This method should be implemented by subclasses.")


class CurrencyBeaconProvider(BaseProvider):
    """Real provider that fetches data from the CurrencyBeacon API."""

    BASE_URL_LATEST = os.getenv('CURRENCYBEACON_BASE_URL_LATEST')
    BASE_URL_HISTORICAL = os.getenv('CURRENCYBEACON_BASE_URL_HISTORICAL')
    API_KEY = os.getenv('CURRENCYBEACON_API_KEY')

    if not API_KEY:
        raise ValueError("CurrencyBeacon API Key is missing in settings.")

    def get_exchange_rate(self, source_currency, exchanged_currency, valuation_date=None, provider='CurrencyBeacon'):
        """
        Fetches the exchange rate from the CurrencyBeacon API.

        Parameters:
        -----------
        source_currency : str
            The source currency code.
        exchanged_currency : str
            The exchanged currency code.
        valuation_date : datetime or None
            The date for which the exchange rate is needed. If None, fetches the latest rate.
        provider : str
            The name of the provider.

        Returns:
        --------
        float or None
            The exchange rate if the request is successful, otherwise None.
        """
        params = {
            "base": source_currency,
            "symbols": exchanged_currency,
            "api_key": self.API_KEY,
        }
        if valuation_date is None:
            BASE_URL = self.BASE_URL_LATEST
        else:
            params["date"] = valuation_date
            BASE_URL = self.BASE_URL_HISTORICAL
        response = requests.get(BASE_URL, params=params)

        if response.status_code == 200:
            data = response.json()
            rates = data.get("rates", [])
            if rates:
                return rates.get(exchanged_currency)
            else:
                return None
        return None


class MockProvider(BaseProvider):
    """Mock provider that generates random exchange rates."""

    def get_exchange_rate(self, source_currency, exchanged_currency, valuation_date=None, provider='Mock'):
        """
        Generates a random exchange rate between two currencies.

        Parameters:
        -----------
        source_currency : str
            The source currency code.
        exchanged_currency : str
            The exchanged currency code.
        valuation_date : datetime or None
            The date for which the exchange rate is needed.
        provider : str
            The name of the provider.

        Returns:
        --------
        float
            A random exchange rate between 0.5 and 1.5.
        """
        return round(random.uniform(0.5, 1.5), 6)


# Dictionary of available providers
AVAILABLE_PROVIDERS = {
    "CurrencyBeacon": CurrencyBeaconProvider(),
    "Mock": MockProvider(),
}


def get_exchange_rate_data(source_currency, exchanged_currency, valuation_date):
    """
    Gets the exchange rate from providers according to their priority
    and availability.

    Parameters:
    -----------
    source_currency : str
        The source currency code.
    exchanged_currency : str
        The exchanged currency code.
    valuation_date : datetime or None
        The date for which the exchange rate is needed.

    Returns:
    --------
    float or None
        The exchange rate if a provider returns a valid rate, otherwise None.
    """
    providers = Provider.objects.filter(active=True).order_by("priority")

    for provider in providers:
        provider_instance = AVAILABLE_PROVIDERS.get(provider.name)
        if provider_instance:
            rate = AVAILABLE_PROVIDERS[provider.name].get_exchange_rate(source_currency,
                                                                        exchanged_currency,
                                                                        valuation_date,
                                                                        provider.name)
            if rate is not None:
                return rate

    return None  # If all providers fail
