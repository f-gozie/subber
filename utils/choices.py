

class Account:
    NAIRA, DOLLAR, OTHER = range(3)
    CURRENCY_CHOICES = (
        (NAIRA, 'ngn'),
        (DOLLAR, 'usd'),
        (OTHER, 'oth')
)