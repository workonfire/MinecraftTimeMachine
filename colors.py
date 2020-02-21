def color_text(color, format, text):
    colors = {'black': 0, 'red': 1, 'green': 2, 'yellow': 3, 'blue': 4, 'purple': 5, 'cyan': 6, 'white': 7}
    if format == 'back':
        format = "\033[4"
    elif format == 'underline':
        format =  "\033[4;3"
    elif format == 'bright':
        format =  "\033[0;9"
    else:
        format = "\033[0;3"
    return format + str(colors[color]) + 'm' + text + "\033[00m"

def colored_message(message):
    color_codes = {
        '&0': "\033[0;30m",
        '&1': "\033[0;34m",
        '&2': "\033[0;32m",
        '&3': "\033[0;34m",
        '&4': "\033[0;31m",
        '&5': "\033[0;35m",
        '&6': "\033[0;33m",
        '&7': "\033[0;37m",
        '&8': "\033[0;90m",
        '&9': "\033[0;34m",
        '&a': "\033[0;92m",
        '&b': "\033[0;96m",
        '&c': "\033[0;91m",
        '&d': "\033[0;95m",
        '&e': "\033[0;93m",
        '&f': "\033[0;37m",
        '&l': "",
        '&o': '',
        '&m': "",
        '&n': "",
        '&r': "\033[0;37m",
        '&k': ""
    }
    for value in color_codes.items():
        message = message.replace(value[0], value[1])
    return message + "\033[00m"