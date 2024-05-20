import unittest
from datetime import datetime
from operations.commands import (AddressBook, add_contact, change_contact, delete_contact, show_phone, add_birthday,
                                 show_birthday, birthdays)
from operations.functions import parse_input


class TestAddressBook(unittest.TestCase):

    def setUp(self):
        self.book = AddressBook()

    def test_add_contact(self):
        args = ["V", "1234567890"]
        result = add_contact(args, self.book)
        self.assertEqual(result, "Contact added.")
        self.assertEqual(len(self.book.data), 1)
        self.assertIn("V", self.book.data)

    def test_add_contact_existing(self):
        args = ["V", "1234567890"]
        add_contact(args, self.book)
        result = add_contact(args, self.book)
        self.assertEqual(result, "Contact updated.")
        self.assertEqual(len(self.book.data), 1)
        self.assertIn("V", self.book.data)

    def test_change_contact(self):
        add_contact(["V", "1234567890"], self.book)
        result = change_contact(["V", "0987654321"], self.book)
        self.assertEqual(result, "Contact phone updated.")
        self.assertEqual(str(self.book.data["V"].phones[0]), "0987654321")

    def test_show_phone(self):
        add_contact(["V", "1234567890"], self.book)
        result = show_phone(["V"], self.book)
        self.assertEqual(result, "V's phone number(s): 1234567890")

    def test_add_birthday(self):
        add_contact(["V", "1234567890"], self.book)
        result = add_birthday(["V", "01.01.2000"], self.book)
        self.assertEqual(result, "Birthday added.")
        self.assertEqual(str(self.book.data["V"].birthday), "2000-01-01")

    def test_show_birthday(self):
        add_contact(["V", "1234567890"], self.book)
        add_birthday(["V", "01.01.2000"], self.book)
        result = show_birthday(["V"], self.book)
        self.assertEqual(result, "2000-01-01")

    def test_birthdays(self):
        add_contact(["V", "1234567890"], self.book)
        today = datetime.today().strftime("%d.%m.%Y")
        add_birthday(["V", today], self.book)
        result = birthdays(self.book)
        self.assertIn("V", result)

    def test_parse_input(self):
        command, args = parse_input("add V 1234567890")
        self.assertEqual(command, "add")
        self.assertEqual(args, ["V", "1234567890"])

    def test_delete_contact(self):
        add_contact(["V", "1234567890"], self.book)
        result = delete_contact(["V"], self.book)
        self.assertEqual(result, "Contact V deleted.")
        self.assertNotIn("V", self.book.data)


if __name__ == "__main__":
    unittest.main()
