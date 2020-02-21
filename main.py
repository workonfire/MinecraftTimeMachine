"""
Minecraft Time Machine
Console mode
Author: Buty935 aka workonfire
"""

__VERSION__ = 'UNDER DEVELOPMENT'

# TODO: Custom timestamp formats
# TODO: Random target time support
# TODO: Comments in default config.yml

# Importing required libraries
from colors import color_print, colored_message
from time import sleep, mktime
import gzip, shutil, os, atexit, yaml, datetime, ciso8601, colorama

# Removing old log files on program exit
def exit_handler():
    try:
        shutil.rmtree('temp')
    except FileNotFoundError:
        pass

atexit.register(exit_handler)

# Defining function for printing colored timestamps
def print_with_timestamp(timestamp, message):
    print(colorama.Style.BRIGHT + colorama.Fore.CYAN + timestamp + " " + colorama.Fore.WHITE + message + colorama.Style.RESET_ALL)

# Defining function for time correction
def take_closest(shot, target):
    return int(min(target, key = lambda x: abs(x - int(mktime(ciso8601.parse_datetime(shot).timetuple())))))

# Reading the configuration file
try:
    with open('config.yml') as config_file:
        config = yaml.load(config_file, Loader = yaml.FullLoader)
except FileNotFoundError:
    # Setting the default values if file does not exist
    with open('config.yml', 'w') as config_file:
        yaml.dump({
            'show_timestamps': True,
            'selected_time': 'none',
            'logs_path': 'default',
            'playback_speed': 1,
            'filter': 'default',
            'spacing': False,
            'locale': 'en'
        }, config_file)
    with open('config.yml') as config_file:
        config = yaml.load(config_file, Loader = yaml.FullLoader)

# Reading the language file
try:
    with open('messages\\' + config['locale'] + '.yml') as language_file:
        language = yaml.load(language_file, Loader = yaml.FullLoader)
except FileNotFoundError:
    color_print('red', "Error: locale file 'messages\\"+config['locale']+".yml' does not exist. Please check your configuration.")
    raise SystemExit

# Welcome
color_print('cyan', "Minecraft Time Machine by Buty935")
color_print('green', language['version'] + __VERSION__)
color_print('yellow', language['text_mode'] + "\n")

# Playback speed warning
if config['playback_speed'] > 10:
    color_print('red', language['playback_speed_warning'])
elif config['playback_speed'] <= 0:
    config['playback_speed'] = 1

# Getting the logs path
if config['logs_path'] == 'default':
    config['logs_path'] = os.getenv("APPDATA") + '\.minecraft\logs\\'

# Setting the date
color_print('magenta', language['supported_formats'])
while True:
    if config['selected_time'] != 'none':
        target_time_unparsed = str(config['selected_time'])
        color_print('green', language['target_time_set'] + target_time_unparsed)
    else:
        target_time_unparsed = input(language['target_time_input'])

    # Processing the date and time
    try:
        target_time_parsed = {'date': target_time_unparsed.split(' ')[0],
                              'time': target_time_unparsed.split(' ')[1]}
        if not os.path.exists(config['logs_path'] + target_time_parsed['date'] + '-1.log.gz'):
            raise FileNotFoundError
        if len(target_time_parsed['time'].split(':')) == 2:
            target_time_parsed['time'] += ':00'
        break
    except IndexError:
        target_time_parsed = {'date': target_time_unparsed}
        break
    except FileNotFoundError:  # zadziała tylko na podanie daty i godziny, bo dżejuś tak powiedział #TODO: naprawić to
        color_print('red', language['time_not_found1'] + target_time_parsed['date'] + language['time_not_found2'])

# Determining the number of log files
logs_files = []
for filename in os.listdir(config['logs_path']):
    if filename.endswith('.log.gz') and filename[:10] == target_time_parsed['date']:
        logs_files.append(filename)

# Extracting the log files
try:
    os.makedirs('temp')
except FileExistsError:
    os.remove('temp\\used.log')
for file in logs_files:
    with gzip.open(config['logs_path'] + file, 'rb') as f_in:
        with open('temp\\' + file.split('.')[0] + '.log', 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)
    with open('temp\\used.log', 'a') as used_log_file:
        with open('temp\\' + file.split('.')[0] + '.log') as extracted_log_file:
            used_log_file.write(extracted_log_file.read())
    os.remove('temp\\' + file.split('.')[0] + '.log')
del logs_files

# Loading the log files contents into the list
full_logs = []
if config['filter'] == 'default':
    config['filter'] = "[CHAT]"
with open('temp\\used.log') as used_log_file:
    for line in used_log_file.readlines():
        if config['filter'] in line:
            full_logs.append(line.rstrip())

# Loading the timestamps from logs into the list and converting them to UNIX time
times = []
messages = []
for line in full_logs:
    times.append(int(mktime(ciso8601.parse_datetime(target_time_parsed['date'] + ' ' + line.split(' ')[0].strip('[]')).timetuple())))
    # Inserting the messages into the list
    messages.append(' '.join(line.split(' ')[3:]))

# Importing messages only from the given time, if provided
try:
    messages = messages[times.index(take_closest(target_time_unparsed, times)) + 1:]
    times = times[times.index(take_closest(target_time_unparsed, times)) + 1:]
    if target_time_parsed['time']:
        color_print('green', language['moved_to_the_closest_time'])
except KeyError:
    pass
except ValueError:
    color_print('red', language['filter_error'])
    raise SystemExit

# Replacing the original values from the message with those from the configuration file
edited_messages = []
for message in messages:
    new_val = message
    for key, val in config['replace'].items():
        new_val = new_val.replace(key, val)
    edited_messages.append(new_val)
del new_val, messages

# Displaying the messages
iterator = 0
for message in edited_messages:
    if config['spacing']:
        message += "\n"
    if config['show_timestamps']:
        print_with_timestamp("[" + datetime.datetime.fromtimestamp(int(times[iterator])).strftime('%Y-%m-%d %H:%M:%S') + "]", colored_message(message))
    else:
        print(colored_message(message))
    try:
        sleep(int(times[iterator + 1] - times[iterator]) / config['playback_speed'])
    except IndexError:
        pass
    iterator += 1
