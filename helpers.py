from colorama import Fore, Back, Style


def green_text(text):
    return f"{Fore.GREEN}{text}{Style.RESET_ALL}"


def text_with_red_background(text):
    return f"{Back.RED}{text}{Style.RESET_ALL}"


def text_with_blue_background(text):
    return f"{Back.BLUE}{text}{Style.RESET_ALL}"
