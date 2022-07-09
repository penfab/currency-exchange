import os
import unittest


from currency_exchange.router import supported_currencies
from currency_exchange.utils import make_request
from currency_exchange.constant import URL_CURRENCIES, URL_CONVERT


class TestCurrencyExchange(unittest.IsolatedAsyncioTestCase):
    async def test_get_currencies(self):
        response = await make_request(URL_CURRENCIES)
        currencies = response.get("symbols", None)
        self.assertIsNot(None, currencies)
        print("test_get_currencies assertIsNot None -->", currencies)


    async def test_convertion_from_to_is_OK(self):
        is_supported, message = await supported_currencies("USD", "EUR")
        self.assertTrue(True, is_supported)
        print("test_convertion_from_to_is_OK assertTrue -->", is_supported, message)


    async def test_convertion_from_to_is_not_OK1(self):
        is_supported, message = await supported_currencies("ABC", "XYZ")
        self.assertFalse(False, is_supported)
        print("test_convertion_from_to_is_not_OK1 assertFalse -->", is_supported, message)


    async def test_convertion_from_to_is_not_OK2(self):
        is_supported, message = await supported_currencies("EUR", "XYZ")
        self.assertFalse(False, is_supported)
        print("test_convertion_from_to_is_not_OK2 assertFalse -->", is_supported, message)


if __name__ == "__main__":
    unittest.main()
