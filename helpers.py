from colorama import Fore, Back, Style


def green_text(text):
    return f"{Fore.GREEN}{text}{Style.RESET_ALL}"


def red_text(text):
    return f"{Fore.RED}{text}{Style.RESET_ALL}"


def purple_text(text):
    return f"{Fore.LIGHTMAGENTA_EX}{text}{Style.RESET_ALL}"


def text_with_red_background(text):
    return f"{Back.RED}{text}{Style.RESET_ALL}"


def text_with_blue_background(text):
    return f"{Back.BLUE}{text}{Style.RESET_ALL}"


def get_int_input_option(message='Your choice: ') -> int:
    try:
        option = int(input(message))
    except ValueError as e:
        print(red_text("Please enter a number"))
        return get_int_input_option()
    else:
        return option
