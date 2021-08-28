import datetime as dt


class Calculator:
    def __init__(self, limit):
        self.limit = limit
        self.records = []
        self.today = dt.date.today()
        self.last_week = self.today - dt.timedelta(days=7)

    def add_record(self, record):
        self.records.append(record)

    def get_today_stats(self):
        today_stats = []
        for record in self.records:
            if record.date == self.today:
                today_stats.append(record.amount)
        return sum(today_stats)

    def get_week_stats(self):
        week_stats = []
        for record in self.records:
            if self.lastweek <= record.date <= self.today:
                week_stats.append(record.amount)
        return sum(week_stats)

    def limit_today(self):
        balance = self.limit - self.get_today_stats()
        return balance


class CaloriesCalculator(Calculator):
    def get_calories_remained(self):
        calories_remained = self.limit_today()
        if calories_remained > 0:
            text = (f'Сегодня можно съесть что-нибудь ещё, но'
                    f'с общей калорийностью не более {calories_remained} кКал')
        else:
            text = ('Хватит есть!')
        return text


class CashCalculator(Calculator):
    BYN_RATE = 1
    USD_RATE = 2.52
    EUR_RATE = 2.96

    def get_today_cash_remained(self, currency='byn'):
        all_currencies = {'byn': ('руб', CashCalculator.BYN_RATE),
                          'usd': ('USD', CashCalculator.USD_RATE),
                          'eur': ('Euro', CashCalculator.EUR_RATE)}
        name, curr = all_currencies[currency]
        currency_remained = self.limit_today()
        currency_remained = round(currency_remained / curr, 2)
        if currency_remained > 0:
            text = (f'На сегодня осталось {currency_remained} {name}')
        elif currency_remained == 0:
            text = ('Денег нет, держись')
        else:
            currency_remained = abs(currency_remained)
            text = (f'Денег нет, держись: твой долг'
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
