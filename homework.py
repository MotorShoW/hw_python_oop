import datetime as dt


class Calculator:
    def __init__(self, limit):
        self.limit = limit
        self.records = []

    def add_record(self, record):
        self.records.append(record)

    def get_today_stats(self):
        today_stats = sum(record.amount for record in self.records
                          if record.date == dt.date.today())
        return today_stats

    def get_week_stats(self):
        # Нужна ли переменная last_week,
        # или стоит все вычисления пихать в выражение-генератор?
        last_week = dt.date.today() - dt.timedelta(days=7)
        week_stats = sum(record.amount for record in self.records
                         if last_week <= record.date <= dt.date.today())
        return week_stats

    def get_limit_today(self):
        balance = self.limit - self.get_today_stats()
        return balance


class CaloriesCalculator(Calculator):
    def get_calories_remained(self):
        calories_remained = self.get_limit_today()
        if calories_remained > 0:
            text = (f'Сегодня можно съесть что-нибудь ещё, но с'
                    f' общей калорийностью не более {calories_remained} кКал')
        else:
            text = 'Хватит есть!'
        return text


class CashCalculator(Calculator):
    RUB_RATE = 1
    USD_RATE = 74.0
    EURO_RATE = 87.0

    def get_today_cash_remained(self, currency='rub'):
        currency_remained = self.get_limit_today()
        if currency_remained == 0:
            return 'Денег нет, держись'
        all_currencies = {'rub': ('руб', CashCalculator.RUB_RATE),
                          'usd': ('USD', CashCalculator.USD_RATE),
                          'eur': ('Euro', CashCalculator.EURO_RATE)}
        name, curr = all_currencies[currency]
        currency_remained = round(currency_remained / curr, 2)
        if currency_remained > 0:
            text = (f'На сегодня осталось {currency_remained} {name}')
        else:
            currency_remained = abs(currency_remained)
            text = (f'Денег нет, держись: твой долг - '
                    f'{currency_remained} {name}')
        return text


class Record():
    def __init__(self, amount, comment, date=None):
        self.amount = amount
        self.comment = comment
        if date is None:
            self.date = dt.date.today()
        else:
            self.date = dt.datetime.strptime(date, '%d.%m.%Y').date()
