from datetime import datetime, date, timedelta
from models.records import AddressBook, Record
from models.fields import Field, Birthday, Name, Phone
from operations.functions import (input_error, change_error, show_phone_error, date_to_string, string_to_date,
                                  prepare_user_list, find_next_weekday)


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


