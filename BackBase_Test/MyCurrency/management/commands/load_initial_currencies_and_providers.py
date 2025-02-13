from django.core.management.base import BaseCommand
from MyCurrency.models import Currency, Provider


class Command(BaseCommand):
    """
    Django management command to run the asynchronous task for loading historical exchange rate data.
    """
    help = "Loads the initial currencies and providers into the database."

    def handle(self, *args, **kwargs):
        # Load currencies
        currencies = [
            {"code": "EUR", "name": "Euro", "symbol": "€"},
            {"code": "CHF", "name": "Swiss Franc", "symbol": "CHF"},
            {"code": "USD", "name": "US Dollar", "symbol": "$"},
            {"code": "GBP", "name": "British Pound", "symbol": "£"},
        ]

        for currency in currencies:
            Currency.objects.update_or_create(code=currency["code"], defaults=currency)

        self.stdout.write(self.style.SUCCESS("Currencies loaded successfully."))

        # Load providers
        providers = [
            {"name": "CurrencyBeacon", "priority": 1, "active": True},
            {"name": "Mock", "priority": 2, "active": True},
        ]

        for provider in providers:
            Provider.objects.update_or_create(name=provider["name"], defaults=provider)

        self.stdout.write(self.style.SUCCESS("Providers loaded successfully."))
