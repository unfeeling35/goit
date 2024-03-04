
def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except KeyError:
            return 'Wrong name'
        except TypeError:
            return 'Please enter correct command'
        except IndexError:
            return 'Wrong amount values'
        except ValueError:
            return "Give me Name and Phone Number, please"

    return inner
