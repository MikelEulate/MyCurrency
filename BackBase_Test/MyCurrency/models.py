from enum import StrEnum, auto
from typing import Tuple

from django.db import models


# Create your models here.

class Currency(models.Model):
    """
    Model representing a currency.

    Attributes:
    -----------
    code : str
        The currency code (e.g., USD, EUR).
    name : str
        The name of the currency.
    symbol : str
        The symbol of the currency.
    """

    code = models.CharField(max_length=3, unique=True)  # Ej: USD, EUR
    name = models.CharField(max_length=20, db_index=True)
    symbol = models.CharField(max_length=10)

    def __str__(self):
        """
        Returns the string representation of the currency, which is its code.

        Returns:
        --------
        str
            The currency code.
        """
        return self.code

class CurrencyExchangeRate(models.Model):
    """
    Model representing an exchange rate between two currencies.

    Attributes:
    -----------
    source_currency : ForeignKey
        The source currency.
    exchanged_currency : ForeignKey
        The exchanged currency.
    valuation_date : date
        The date of the exchange rate valuation.
    rate_value : Decimal
        The value of the exchange rate.
    """

    source_currency = models.ForeignKey(Currency, related_name='exchanges', on_delete=models.CASCADE)
    exchanged_currency = models.ForeignKey(Currency,on_delete=models.CASCADE)
    valuation_date = models.DateField(db_index=True)
    rate_value = models.DecimalField(db_index=True,decimal_places=6, max_digits=18)

    def __str__(self):
        """
        Returns the string representation of the exchange rate.

        Returns:
        --------
        str
            The exchange rate in the format "source_currency to exchanged_currency on valuation_date".
        """
        return f"{self.source_currency} to {self.exchanged_currency} on {self.valuation_date}"


class Provider(models.Model):
    """
    Model representing a provider of exchange rates.

    Attributes:
    -----------
    name : str
        The name of the provider.
    priority : int
        The priority of the provider.
    active : bool
        Whether the provider is active.
    """

    name = models.CharField(max_length=50, unique=True)
    priority = models.PositiveIntegerField(default=1)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ['priority']

    def __str__(self):
        """
        Returns the string representation of the provider, which is its name.

        Returns:
        --------
        str
            The provider name.
        """
        return self.name


class CurrencyType(StrEnum):
    """
    Enum representing different types of currencies.

    Attributes:
    -----------
    EUR : str
        Euro.
    CHF : str
        Swiss Franc.
    USD : str
        US Dollar.
    GBP : str
        British Pound.
    """

    EUR = "EUR"
    CHF = "CHF"
    USD = "USD"
    GBP = "GBP"

    def describe(self) -> Tuple[str, str]:
        """
        Returns the enum name and associated value.

        Returns:
        --------
        Tuple[str, str]
            The enum name and associated value.
        """
        return self.name, self.value

    def __str__(self) -> str:
        """
        Returns the string representation of the enum, which is its name.

        Returns:
        --------
        str
            The enum name.
        """
        return self.name

    @classmethod
    def default_code(cls) -> str:
        """
        returns default enum value

        Returns
        -------
        int
            default enum value
        """
        return cls.EUR
