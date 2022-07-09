from fastapi import APIRouter
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from currency_exchange.utils import make_request
from currency_exchange.constant import (
    URL_CURRENCIES,
    URL_CONVERT,
    URL_HISTORICAL
)


router = APIRouter()


@router.get("/currencies")
async def currencies():
    """
    return a JSONResponse containing all supported currencies
    """
    data = await make_request(URL_CURRENCIES)

    # get the currencies from the api.exchangerate.host response
    currencies = data.get("symbols", None)

    if currencies:
        return JSONResponse(
                status_code=200,
                content={ "supported_currencies": currencies })


async def supported_currencies(_from: str, _to:str):
    """
    check if currencies (_from -> _to) are supported by the API
    return a boolean and a reason when _from/_to are/not supported
    """
    # retrieve all currencies supported by the API
    data = await make_request(URL_CURRENCIES)

    currencies = data.get("symbols", None)

    if currencies:
        __from = currencies.get(_from, None)
        __to = currencies.get(_to, None)

        # construct a detailed reason on a requested conversion exchange
        if __from and __to:
            detail = f"'{_from}' -> '{_to}' exchange supported"
            return True, detail
        elif not __from and not __to:
            detail = f"'{_from}' and '{_to}' are both not supported currencies"
            return False, detail
        elif not __from:
            detail = f"'{_from}' is not a supported currency"
            return False, detail
        elif not __to:
            detail = f"'{_to}' is not a supported currency"
            return False, detail


@router.get("/convert")
async def convert(_from: str, _to: str, _amount: float, historical: bool):
    """
    return a detail and a result for an exchange
    """
    if _amount > 0:
        _from = _from.upper()
        _to = _to.upper()
        can_make_request, message = await supported_currencies(_from, _to)

        if can_make_request:
            try:
                data = await make_request(URL_CONVERT.format(_from, _to, _amount))

                # construct the different details for a succesful conversion
                # exchange and return the response
                base_query = data.get("query")
                _from = base_query.get("from")
                _to = base_query.get("to")
                amount = base_query.get("amount")

                info = data.get("info")
                result = data.get("result")
                date = data.get("date")
                rate = f"rate is {info['rate']} on the {date}"

                if historical:
                    # historical are based on EUR (always 1) from the API
                    data = await make_request(URL_HISTORICAL.format(date))
                    rates = data.get("rates", None)
                    if rates:
                        result = f"for {amount} '{_from}' you get {result} '{_to}'"
                        historical = f"previous rates on the {date}: {rates}"
                    return JSONResponse(
                            status_code=200,
                            content={ "detail": message,
                                "result": result,
                                "rate": rate,
                                "historical": historical })

                result = f"for {amount} '{_from}' you get {result} '{_to}'"
                return JSONResponse(
                        status_code=200,
                        content={ "detail": message,
                            "result": result,
                            "rate": rate})
            except Exception as e:
                return JSONResponse(
                        status_code=500,
                        content={ "detail": e.args })
        else:
            # return a response detail on why the conversion exchange failed
            return JSONResponse(
                    status_code=202,
                    content={ "detail": message })
    # return response when amount <= 0
    return JSONResponse(
            status_code=202,
            content={ "detail": "provide an amount > 0" })
