from django.contrib import admin
from .models import Currency, CurrencyExchangeRate

@admin.register(Currency)
class CurrencyAdmin(admin.ModelAdmin):
    """
    Returns the enum name and associated value.

    Returns:
    --------
    Tuple[str, str]
        The enum name and associated value.
    """
    list_display = ('code', 'name', 'symbol')
    search_fields = ('code', 'name')
    ordering = ('code',)


@admin.register(CurrencyExchangeRate)
class CurrencyExchangeRateAdmin(admin.ModelAdmin):
    """
    Admin interface options for the CurrencyExchangeRate model.

    Attributes:
    -----------
    list_display : tuple
        Fields to display in the list view.
    list_filter : tuple
        Fields to include in the filter functionality.
    search_fields : tuple
        Fields to include in the search functionality.
    ordering : tuple
        Default ordering for the list view.
    """
    list_display = ('source_currency', 'exchanged_currency', 'valuation_date', 'rate_value')
    list_filter = ('valuation_date', 'source_currency', 'exchanged_currency')
    search_fields = ('source_currency__code', 'exchanged_currency__code')
    ordering = ('-valuation_date',)

