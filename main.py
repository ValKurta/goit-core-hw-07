

import sys
from operations.functions import parse_input
from operations.commands import (AddressBook, add_contact, change_contact, delete_contact, show_phone, add_birthday,
                                 show_birthday, birthdays)


def main():
    book = AddressBook()
    print("Welcome to the assistant bot! Click the 'help' button to learn about all the commands.")
    while True:
        print("Commands list - help, close, exit, add, change, delete, phone, all, add-birthday, show-birthday "
              "and birthdays")
        user_input = input("Enter a command: ")
        command, args = parse_input(user_input)
        if command in ["close", "exit"]:
            print("Bye!")
            sys.exit(1)
        elif command == "hello":
            print("How can I help you? Please enter 'add' your name and number.")
        elif command == "help":
            print("You can:")
            print("add - add name and phone number;")
            print("close/exit - if you want quit;")
            print("change - if you need to do some change;")
            print("delete - if you need to remove a contact;")
            print("phone - you need enter name to see phone number")
            print("all - to see all list that you add")
            print("add-birthday - Add the date of birth for the specified contact.")
            print("show-birthday - Show the date of birth for the specified contact.")
            print("birthdays - Show birthdays that will take place within the next week.")
        elif command == "add":
            print(add_contact(args, book))
        elif command == "change":
            print(change_contact(args, book))
        elif command == "phone":
            print(show_phone(args, book))
        elif command == "all":
            print(f"Here's all contacts that you've added:\n{book}. Do you need to make any changes?")
        elif command == "add-birthday":
            print(add_birthday(args, book))
        elif command == "show-birthday":
            print(show_birthday(args, book))
        elif command == "birthdays":
            print(birthdays(book))
        elif command == "delete":
            print(delete_contact(args, book))
        else:
            print("Invalid command.")


if __name__ == "__main__":
    main()
