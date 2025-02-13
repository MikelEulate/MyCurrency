import random
from datetime import datetime, timedelta
import asyncio
from asgiref.sync import sync_to_async
from django.core.management.base import BaseCommand
from MyCurrency.models import Currency, CurrencyExchangeRate

DAYS_LOOKBACK = 30 # Load test data for the last selected days


async def generate_test_data():
    """
    Asynchronously generates test exchange rate data for the last DAYS_LOOKBACK days.

    Returns:
    --------
    str
        A message indicating the result of the data generation.
    """
    currencies = await sync_to_async(list)(Currency.objects.all())
    if not currencies:
        return "No currencies in the database. Make sure to load them first."

    historical_rates = []

    for i in range(DAYS_LOOKBACK):
        valuation_date = datetime.today() - timedelta(days=i)

        for source_currency in currencies:
            for exchanged_currency in currencies:
                if source_currency == exchanged_currency:
                    continue  # Avoid same currency rates

                rate_value = round(random.uniform(0.8, 1.3), 6)  # Simulate realistic rates

                historical_rates.append(
                    CurrencyExchangeRate(
                        source_currency=source_currency,
                        exchanged_currency=exchanged_currency,
                        valuation_date=valuation_date.date(),
                        rate_value=rate_value
                    )
                )

    await sync_to_async(CurrencyExchangeRate.objects.bulk_create)(historical_rates)
    return "Test data generated successfully."


class Command(BaseCommand):
    """
    Django management command to generate test exchange rate data for the last 30 days.
    """
    help = "Generates test exchange rate data for the last 30 days."

    def handle(self, *args, **kwargs):
        self.stdout.write("Generating test exchange rate data...")
        result = asyncio.run(generate_test_data())
        if result:
            self.stdout.write(self.style.SUCCESS(result))
        else:
            self.stderr.write(result)