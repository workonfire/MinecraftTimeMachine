import colorama

def color_print(color, text):
    colorama.init(autoreset=True)
    if color == 'red':
        color_to_print = colorama.Fore.RED
    elif color == 'green':
        color_to_print = colorama.Fore.GREEN
    elif color == 'yellow':
        color_to_print = colorama.Fore.YELLOW
    elif color == 'blue':
        color_to_print = colorama.Fore.BLUE
    elif color == 'magenta':
        color_to_print = colorama.Fore.MAGENTA
    elif color == 'cyan':
        color_to_print = colorama.Fore.CYAN
    else:
        color_to_print = colorama.Fore.WHITE
    print(colorama.Style.BRIGHT + color_to_print + text)
    colorama.deinit()

def colored_message(format):
    # Przykład: &c&lB&6&lu&e&lt&a&ly&b&l9&3&l3&9&l5
    colorama.init(autoreset=True)
    format = format.replace('&4', colorama.Style.DIM + colorama.Fore.RED)
    format = format.replace('&c', colorama.Style.BRIGHT + colorama.Fore.RED)
    format = format.replace('&6', colorama.Style.DIM + colorama.Fore.YELLOW)
    format = format.replace('&e', colorama.Style.BRIGHT + colorama.Fore.YELLOW)
    format = format.replace('&2', colorama.Style.DIM + colorama.Fore.GREEN)
    format = format.replace('&a', colorama.Style.BRIGHT + colorama.Fore.GREEN)
    format = format.replace('&b', colorama.Style.BRIGHT + colorama.Fore.CYAN)
    format = format.replace('&3', colorama.Style.DIM + colorama.Fore.CYAN)
    format = format.replace('&1', colorama.Style.BRIGHT + colorama.Fore.BLUE)
    format = format.replace('&9', colorama.Style.DIM + colorama.Fore.BLUE)
    format = format.replace('&d', colorama.Style.BRIGHT + colorama.Fore.MAGENTA)
    format = format.replace('&5', colorama.Style.DIM + colorama.Fore.MAGENTA)
    format = format.replace('&f', colorama.Style.BRIGHT + colorama.Fore.WHITE)
    format = format.replace('&7', colorama.Style.DIM + colorama.Fore.WHITE)
    format = format.replace('&8', colorama.Style.DIM + colorama.Fore.WHITE)
    format = format.replace('&0', colorama.Style.DIM + colorama.Fore.WHITE)
    format = format.replace('&l', '')
    format = format.replace('&o', '')
    format = format.replace('&m', '')
    format = format.replace('&n', '')
    format = format.replace('&r', colorama.Style.DIM + colorama.Fore.WHITE)
    format = format.replace('&k', '')
    colorama.deinit()
    return format + colorama.Style.RESET_ALL