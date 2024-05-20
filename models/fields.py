import re
from datetime import datetime, date, timedelta


class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class Birthday(Field):
    def __init__(self, value):
        super().__init__(value)
        try:
            self.value = datetime.strptime(value, "%d.%m.%Y").date()
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")


class Name(Field):
    def __init__(self, name):
        super().__init__(name)


class Phone(Field):
    def __init__(self, phone):
        if not self.valid_phone(phone):
            raise ValueError('Number must be 10 digits!')
        super().__init__(phone)

    def valid_phone(self, phone):
        return isinstance(phone, str) and re.match(r'^\d{10}$', phone)
