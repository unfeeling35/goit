from AddressBook import Record, contacts
from input_error import input_error
from AbstractBasic import BasicConsoleUI


UI = BasicConsoleUI()

@input_error
def add(data: list):
    if contacts.has_record(data[0]):
        raise KeyError
    if not (data[1].strip()).isnumeric():
        raise ValueError
    record = Record(data[0].strip())
    # print("created record ", data[0].strip())
    for phone in data[1:]:
        record.add_phone(phone)
        # print(f"added {phone} to contact {data[0]}")
    contacts.add_record(record)
    return f'Added new Contact "{data[0]}"'


@input_error
def change(data):
    if not contacts.has_record(data[0]):
        return "No such contact"
    if not (data[1]).isnumeric():
        raise ValueError
    record = contacts.get_record(data[0])
    record.edit_phone(data[1], data[2])
    return f'Number {data[1]} with name {data[0]} was changed.'


@input_error
def hello():
    return 'Hello, How can I help you?'


@input_error
def wrong_command():
    return 'Wrong command.. Make sure you typed correctly and try again.'


def delete(name):
    contacts.delete(name[0].strip())
    return 'contact has been deleted'


def birthday(data):
    # command example: birthday john 2011-01-18
    record = contacts.get_record(data[0])
    print(record)
    record.birthday = data[1]
    return f"added birthday to contact{data[0]}"


def days_to_birthday(name):
    # command example: bday john
    return contacts.get_record(name[0]).days_to_birthday()


def find(data):
    # command example find test123
    for contact in contacts.find_extended(data[0]):
        print(contact)


COMMANDS = {
    'hello': hello,
    'add': add,
    'change': change,
    'phone': UI.find_phone,
    'show all': UI.show_all,
    'wrong command': wrong_command,
    'delete': delete,
    'birthday': birthday,
    'bday': days_to_birthday,
    'find': find,
    'help': UI.show_help
}


@input_error
def handler(user_line):
    result = {
        'user_command': '',
        'data': []
    }
    if user_line.lower() == 'show all':
        result['user_command'] = user_line.lower()
        # print(result)
        return result['user_command'], result['data']
    user_line_list = user_line.split(' ')
    # print(user_line_list)
    result['user_command'] = user_line_list[0].lower()
    result['data'] = user_line_list[1:]

    return result['user_command'], result['data']


@input_error
def command_handler(command):
    if command not in COMMANDS:
        return COMMANDS['wrong command']
    return COMMANDS[command]


def main():
    try:
        while True:
            user_input = input(">>")
            if user_input.lower() == 'exit' or user_input.lower() == 'good bye' or user_input.lower() == 'bye':
                print("Good bye")
                break
            command, data = handler(user_input)
            if not data:
                result = command_handler(command)
                result()
                continue
            result = command_handler(command)(data)
            if result:
                print(result)
    finally:
        contacts.save_data_to_file()


if __name__ == "__main__":
    print("Welcome to CLI contacts bot.")
    print("Please enter your command\nFor more info type 'help'")
    main()
