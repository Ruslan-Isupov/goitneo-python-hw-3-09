# # HW 3

from datetime import datetime
from collections import defaultdict
from collections import UserDict
import re


class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class Name(Field):
    pass


class Phone(Field):

    def __init__(self, phone):

        if re.search("[0-9]{10}$", phone) and len(phone) == 10:
            super().__init__(phone)

        else:
            raise ValueError("Phone is not valid")


class Birthday(Field):

    def __init__(self, birthday):

        if datetime.strptime(birthday, "%d.%m.%Y"):
            birthday = datetime.strptime(birthday, "%d.%m.%Y").date()
            super().__init__(birthday)
        else:
            raise ValueError("Birthday is not valid")


class Record:

    def __init__(self, name):

        self.name = Name(name)
        self.phones = []
        self.birthday = ""

    def add_phone(self, phone):

        self.phones.append(Phone(phone))

    def edit_phone(self, new_phone):

        self.phones[0] = Phone(new_phone)

    def remove_phone(self, phone):

        phone = Phone(phone)
        for p in self.phones:
            if p.value == phone:
                self.phones.remove(p)
            else:
                return "Phone doesn't exist"

    def find_phone(self, search_phone):
        for p in self.phones:
            if p.value == search_phone:
                return p
            else:
                return "Phone doesn't exist"

    def add_birthday(self, birthday):

        if birthday:
            self.birthday = Birthday(birthday)
        else:
            birthday = ""

    def __str__(self):

        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)} , birhday: {self.birthday.value if self.birthday else self.birthday}"


class AddressBook(UserDict):

    def add_record(self, record):

        self.data[record.name.value] = record

    def find(self, name):

        if self.data.get(name):

            return self.data.get(name)
        else:
            return False

    def delete(self, name):

        if self.data.get(name):

            self.data.pop(name)

        else:
            return "Name doesn't exist"


def get_birthdays_per_week(self):

    dict_birthday = defaultdict(list)

    today = datetime.today().date()

    for name, record in self.data.items():
        birthday = record.birthday.value
        birthday_this_year = birthday.replace(year=today.year)

        if birthday_this_year < today:
            birthday_this_year = birthday.replace(year=today.year + 1)

        else:
            delta_days = (birthday_this_year - today).days
            precise_day = birthday_this_year.weekday()

            if delta_days < 7 and precise_day <= 4:
                day_of_week = birthday_this_year.strftime("%A")
                dict_birthday[day_of_week].append(name)

            elif delta_days < 7 and precise_day > 4:
                day_of_week = "Monday"
                dict_birthday[day_of_week].append(name)

            else:
                continue

    birthday_list = []
    for name, birthday in dict_birthday.items():
        info_birthdays = ", "
        birthday_list.append(f"{name}: {info_birthdays.join(birthday)}")

    return "\n".join(birthday_list)


book = AddressBook()


def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)

        except ValueError as e:
            return str(e)
        except KeyError:
            return "Contact not found."
        except IndexError:
            return "Doesn't exist."

    return inner


def parse_input(user_input):
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args


@input_error
def add_contact(args):
    try:
        name, phone = args
        if book.find(name):
            book.find(name).add_phone(phone)
            return "Additional phone added to this contact"
        else:
            new_contact = Record(name)
            new_contact.add_phone(phone)
            book.add_record(new_contact)
            return "Contact added."
    except ValueError:
        raise ValueError("Give me name and phone(only 10 digits), please")


@input_error
def change_contact(args):
    try:
        name, new_phone = args
        if name in book.data.keys():
            new_contact = book.find(name)
            new_contact.edit_phone(new_phone)
            return "Contact updated."
        else:
            raise KeyError
    except ValueError:
        raise ValueError("Give me name and new phone(only 10 digits), please")


@input_error
def show_phone(args):
    try:
        (name,) = args
        if name in book.data.keys():
            new_contact = book.find(name)
            value = ""
            for p in new_contact.phones:
                value += f"{p},"
            return value.removesuffix(",")
        else:
            raise KeyError
    except ValueError:
        raise ValueError("Give me name, please")


@input_error
def show_all():
    info_contacts = ""
    for _, record in book.data.items():
        info_contacts += f"{record}\n"
    if info_contacts:
        return info_contacts.strip()
    else:
        return "We don't have any contacts"


@input_error
def add_birthday(args):

    try:
        name, birthday = args
        if name in book.data.keys():
            new_contact = book.find(name)
            new_contact.add_birthday(birthday)
            return "Birthday added."
        else:
            raise KeyError

    except ValueError:
        raise ValueError("Give me name and birthday in format DD.MM.YYYY , please")


@input_error
def show_birthday(args):
    try:
        (name,) = args
        if name in book.data.keys():

            new_contact = book.find(name)

            return new_contact.birthday
        elif new_contact.birthday == "":
            return "We don't have contact's birthday"
        else:
            raise KeyError
    except ValueError:
        raise ValueError("Give me name, please")


def birthdays():
    return get_birthdays_per_week(book)


def main():

    print("Welcome to the assistant bot!")
    while True:
        user_input = input("Enter a command: ")
        command, *args = parse_input(user_input)

        if command in ["close", "exit"]:
            print("Good bye!")
            break
        elif command == "hello":
            print("How can I help you?")

        elif command == "add":
            print(add_contact(args))

        elif command == "change":
            print(change_contact(args))

        elif command == "phone":
            print(show_phone(args))

        elif command == "all":
            print(show_all())

        elif command == "add-birthday":
            print(add_birthday(args))

        elif command == "show-birthday":
            print(show_birthday(args))

        elif command == "birthdays":
            print(birthdays())

        else:
            print("Invalid command.")


if __name__ == "__main__":
    main()
