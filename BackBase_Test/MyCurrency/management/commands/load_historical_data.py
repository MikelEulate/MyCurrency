import asyncio
from datetime import datetime, timedelta
from asgiref.sync import sync_to_async
from django.core.management.base import BaseCommand
from MyCurrency.models import Currency, CurrencyExchangeRate
from MyCurrency.providers import get_exchange_rate_data

DAYS_LOOKBACK = 365 # Load historical data for the last selected days


async def fetch_and_store_exchange_rate(source_currency, exchanged_currency, valuation_date):
    """
    Obtains and stores the exchange rate between two currencies on a specific date.

    Parameters:
    -----------
    source_currency : Currency
        The source currency object.
    exchanged_currency : Currency
        The exchanged currency object.
    valuation_date : datetime
        The date for which the exchange rate is needed.

    Returns:
    --------
    None
    """
    try:
        rate = await sync_to_async(get_exchange_rate_data)(source_currency.code, exchanged_currency.code, valuation_date)
        if rate:
            await sync_to_async(CurrencyExchangeRate.objects.update_or_create)(
                source_currency=source_currency,
                exchanged_currency=exchanged_currency,
                valuation_date=valuation_date.date(),
                defaults={'rate_value': rate}
            )
    except Exception as e:
        print(f"Error fetching rate for {source_currency.code} -> {exchanged_currency.code}: {e}")

async def load_historical_exchange_rates():
    """
    Asynchronous task to load historical exchange rate data.
    Processes large volumes of data concurrently.

    Returns:
    --------
    None
    """
    currencies = await sync_to_async(list)(Currency.objects.all())  # Load all currencies

    async def process_data():
        tasks = []
        for i in range(DAYS_LOOKBACK):
            valuation_date = datetime.today() - timedelta(days=i)

            for source_currency in currencies:
                for exchanged_currency in currencies:
                    if source_currency == exchanged_currency:
                        continue  # Avoid converting the same currency

                    # Create the asynchronous task
                    tasks.append(fetch_and_store_exchange_rate(source_currency, exchanged_currency, valuation_date))

        # Run all tasks concurrently
        await asyncio.gather(*tasks)

    # Run the main asynchronous task
    await process_data()

class Command(BaseCommand):
    """
    Django management command to run the asynchronous task for loading historical exchange rate data.
    """
    help = "Runs the asynchronous task to load historical exchange rate data."

    def handle(self, *args, **kwargs):
        self.stdout.write("Starting to load historical exchange rate data...")

        # Run the asynchronous task
        asyncio.run(load_historical_exchange_rates())
        self.stdout.write(self.style.SUCCESS("Historical exchange rate data loaded successfully."))