import requests
from config import FASTFOREX_API_KEY


def currency_converter(amount, base, target):

    url = f"https://api.fastforex.io/fetch-one?from={base}&to={target}"

    headers = {
        "X-API-Key": FASTFOREX_API_KEY
    }

    response = requests.get(url, headers=headers)

    data = response.json()

    rate = data["result"][target]

    result = amount * rate

    return f"{amount} {base} = {round(result,2)} {target}"


def multiply(a, b):
    return a * b