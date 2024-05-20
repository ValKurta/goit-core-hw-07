from collections import UserDict
from operations.functions import (input_error, change_error, show_phone_error, date_to_string, string_to_date,
                                  prepare_user_list, find_next_weekday, adjust_for_weekend)
from models.fields import Field, Birthday, Name, Phone
from datetime import datetime, date, timedelta


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


@input_error
def add_contact(args, book: AddressBook):
    if len(args) < 2:
        return "Not enough arguments. Usage: add <name> <phone>"
    name, phone = args[:2]
    record = book.find(name)
    message = "Contact updated."
    if record is None:
        record = Record(name)
        book.add_record(record)
        message = "Contact added."
    record.add_phone(phone)
    return message


@input_error
def add_birthday(args, book: AddressBook):
    if len(args) < 2:
        return "Not enough arguments. Usage: add-birthday <name> <birthday>"
    name, birthday = args[:2]
    record = book.find(name)
    if record is None:
        return "Contact not found."
    record.add_birthday(birthday)
    return "Birthday added."


@input_error
def show_birthday(args, book: AddressBook):
    if len(args) < 1:
        return "Not enough arguments. Usage: show-birthday <name>"
    name = args[0]
    record = book.find(name)
    if record is None:
        return "Contact not found."
    return str(record.birthday) if record.birthday else "Birthday not set."


@input_error
def birthdays(book: AddressBook):
    upcoming_birthdays = book.get_upcoming_birthdays()
    if upcoming_birthdays:
        return "\n".join(f"{entry['name']} - {entry['congratulation_date']}" for entry in upcoming_birthdays)
    else:
        return "There is no one to congratulate within the next week."


@change_error
def change_contact(args, book: AddressBook):
    if len(args) < 2:
        return "Not enough arguments. Usage: change <name> <new_phone>"
    name, phone = args[:2]
    record = book.find(name)
    if record:
        record.phones = [Phone(phone)]
        return "Contact phone updated."
    else:
        return "This name was not found in contacts."


@show_phone_error
def delete_contact(args, book: AddressBook):
    if len(args) < 1:
        return "Not enough arguments. Usage: delete <name>"
    name = args[0]
    book.delete(name)
    return f"Contact {name} deleted."


@show_phone_error
def show_phone(args, book: AddressBook):
    if len(args) < 1:
        return "Not enough arguments. Usage: phone <name>"
    name = args[0]
    record = book.find(name)
    if record:
        return f"{name}'s phone number(s): {', '.join(str(p) for p in record.phones)}"
    else:
        return "This name was not found in contacts."


