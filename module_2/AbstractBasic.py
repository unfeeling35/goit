from abc import abstractmethod, ABC
from input_error import input_error
from AddressBook import contacts


class AbstractBasicUI(ABC):
    @abstractmethod
    def find_phone(self, data):
        pass

    def show_all(self):
        pass

    def show_help(self):
        pass


class BasicConsoleUI(AbstractBasicUI):
    @input_error
    def find_phone(self, name):
        return contacts.get_record(name[0])

    # def help_command():
    @input_error
    def show_all(self):
        all_contacts = ''
        page_number = 1

        for page in contacts.iterator():
            all_contacts += f'Page #{page_number}\n'

            for record in page:
                all_contacts += f'{record.get_info()}\n'
            page_number += 1
        print(all_contacts)

    def show_help(self):
        available_commands = {
            'hello': "say hello",
            'add': "add contact, example add john 1234567890",
            'change': 'change number in existing contact. example: change John old_phone new_phone',
            'phone': "find contact by name. example: phone John",
            'show all': "returns all contacts in book",
            'delete': "remove contact from the book, example: delete john",
            'birthday': "set a birthday for contact, example: birthday john 2022-11-11",
            'bday': 'return days till next birthday of a contact, example: bday john',
            'find': 'find any matches in contact name or phones, example: find xxx'
        }
        for key, description in available_commands.items():
            print("{:<10} -> {}".format(key, description))
