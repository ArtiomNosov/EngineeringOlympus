def foo(currency1, currency2, timePeriod=None):
    if timePeriod:
        return getExchangeRate(currency1, currency2, timePeriod)
    else:
        return getLastExchangeRate(currency1, currency2)

# проверить что будет принимать и возвращать пользователю