import re
from tools import currency_converter, multiply


def run_agent(user_query):

    user_query = user_query.lower()

    # ---- Currency Conversion ----
    currency_pattern = r'(\d+(?:\.\d+)?)\s*([a-z]{3})\s*(?:to|in)\s*([a-z]{3})'

    match = re.search(currency_pattern, user_query)

    if match:
        amount = float(match.group(1))
        base = match.group(2).upper()
        target = match.group(3).upper()

        return currency_converter(amount, base, target)

    # ---- Multiplication ----
    mult_pattern = r'(\d+(?:\.\d+)?)\s*\*\s*(\d+(?:\.\d+)?)'

    mult = re.search(mult_pattern, user_query)

    if mult:
        a = float(mult.group(1))
        b = float(mult.group(2))

        return multiply(a, b)

    return "Sorry, I cannot handle this request."