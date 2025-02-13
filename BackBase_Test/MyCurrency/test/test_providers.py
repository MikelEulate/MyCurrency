# test/test_providers.py

import os
from django.test import TestCase
from unittest.mock import patch, MagicMock
from dotenv import load_dotenv
from MyCurrency.providers import CurrencyBeaconProvider, MockProvider, get_exchange_rate_data
from MyCurrency.models import Provider, Currency

class ExchangeRateProviderTest(TestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        load_dotenv()  # Load environment variables from .env file

    @patch('requests.get')
    def test_CurrencyBeaconProvider_returns_exchange_rate(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"rates": {"EUR": 0.85}}
        mock_get.return_value = mock_response

        provider = CurrencyBeaconProvider()
        rate = provider.get_exchange_rate("USD", "EUR")
        self.assertEqual(rate, 0.85)

    @patch('requests.get')
    def test_CurrencyBeaconProvider_returns_none_on_failure(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_get.return_value = mock_response

        provider = CurrencyBeaconProvider()
        rate = provider.get_exchange_rate("USD", "EUR")
        self.assertIsNone(rate)

    def test_MockProvider_returns_random_exchange_rate(self):
        provider = MockProvider()
        rate = provider.get_exchange_rate("USD", "EUR")
        self.assertTrue(0.5 <= rate <= 1.5)

    @patch('requests.get')
    def test_get_exchange_rate_data_returns_rate_from_active_provider(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"rates": {"EUR": 0.85}}
        mock_get.return_value = mock_response

        provider = Provider.objects.create(name="CurrencyBeacon", priority=1, active=True)
        rate = get_exchange_rate_data("USD", "EUR", "2025-01-01")
        self.assertEqual(rate, 0.85)

    @patch('requests.get')
    def test_get_exchange_rate_data_returns_none_for_invalid_date(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_get.return_value = mock_response

        rate = get_exchange_rate_data("USD", "EUR", "invalid-date")
        self.assertIsNone(rate)

    def test_get_exchange_rate_data_returns_none_if_no_active_providers(self):
        rate = get_exchange_rate_data("USD", "EUR", None)
        self.assertIsNone(rate)