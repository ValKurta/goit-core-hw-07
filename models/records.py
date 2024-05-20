from collections import UserDict
from datetime import datetime, date, timedelta
from models.fields import Field, Birthday, Name, Phone
from operations.functions import find_next_weekday, date_to_string


class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def add_birthday(self, birthday):
        self.birthday = Birthday(birthday)

    def add_phone(self, phone):
        self.phones.append(Phone(phone))

    def remove_phone(self, phone):
        self.phones = [p for p in self.phones if p.value != phone]

    def edit_phone(self, old_phone, new_phone):
        phone = self.find_phone(old_phone)
        if not phone:
            raise ValueError
        index = self.phones.index(phone)
        self.phones[index] = Phone(new_phone)

    def find_phone(self, phone):
        for p in self.phones:
            if p.value == phone:
                return p
        return None

    def __str__(self):
        phones = '; '.join(str(p) for p in self.phones)
        birthday = str(self.birthday) if self.birthday else "Not set"
        return f"Contact name: {self.name.value}, phones: {phones}, birthday: {birthday}"


class AddressBook(UserDict):
    def add_record(self, record):
        if record.name.value not in self.data:
            self.data[record.name.value] = record
        else:
            return "Name is already in the list!"

    def find(self, name):
        return self.data.get(name)

    def delete(self, name):
        if name in self.data:
            del self.data[name]
        else:
            raise ValueError("Record not found in the address book.")

    def get_upcoming_birthdays(self, days=7):
        today = date.today()
        upcoming_birthdays = []
        for record in self.data.values():
            if record.birthday:
                birthday_this_year = record.birthday.value.replace(year=today.year)
                if birthday_this_year < today:
                    birthday_this_year = birthday_this_year.replace(year=today.year + 1)
                if birthday_this_year.weekday() >= 5:
                    birthday_this_year = find_next_weekday(birthday_this_year, 0)
                if 0 <= (birthday_this_year - today).days <= days:
                    congratulation_date_str = date_to_string(birthday_this_year)
                    upcoming_birthdays.append({"name": record.name.value,
                                               "congratulation_date": congratulation_date_str})
        return upcoming_birthdays

    def __str__(self):
        return '\n'.join(str(record) for record in self.data.values())