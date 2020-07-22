"""
Minecraft Time Machine
Console mode
Author: Buty935 aka workonfire
"""

__VERSION__ = '1.0.1 BETA'
__AUTHOR__ = 'Buty935'
__CLIENT_ID__ = 680766220764839966
__AUTHORS_DISCORD__ = "workonfire#8262"

# Importing required libraries

import atexit
import ciso8601
import datetime
import gzip
import os
import shutil
import sys
import yaml
from time import sleep, mktime

from colors import color_text, colored_message


# Removing old log files and safe closing the program on exit
def exit_handler():
    try:
        shutil.rmtree('temp')
        if sys.argv[1] == '-s':
            os.system('pause')
    except FileNotFoundError:
        pass
    except IndexError:
        pass


atexit.register(exit_handler)


# Defining the function for printing colored timestamps
def print_with_timestamp(timestamp, message_input):
    print("\033[0;96m" + timestamp + " " + "\033[0;37m" + message_input + "\033[00m")


# Defining the function for time correction
def take_closest(shot, target):
    return int(min(target, key=lambda x: abs(x - int(mktime(ciso8601.parse_datetime(shot).timetuple())))))


# Reading the configuration file
try:
    with open('config.yml') as config_file:
        config = yaml.load(config_file, Loader=yaml.FullLoader)
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
        config = yaml.load(config_file, Loader=yaml.FullLoader)

# Reading the language file
try:
    with open('messages\\' + config['locale'] + '.yml') as language_file:
        language = yaml.load(language_file, Loader=yaml.FullLoader)
except FileNotFoundError:
    print(color_text('red', 'none', "Error: locale file 'messages\\" + config[
        'locale'] + ".yml' does not exist. Please check your configuration."))
    print("Setting default language...")
    try:
        with open('messages\\en.yml') as language_file:
            language = yaml.load(language_file, Loader=yaml.FullLoader)
    except FileNotFoundError:
        print(color_text('red', 'none', "DEFAULT LOCALE FILE (en.yml) NOT FOUND."))
        raise SystemExit

# Welcome
if config['splash']:
    print("\n")
    print(color_text('purple', 'none',
                     "████████╗██╗███╗   ███╗███████╗    ███╗   ███╗ █████╗  ██████╗██╗  ██╗██╗███╗   ██╗███████╗"))
    print(color_text('purple', 'bright',
                     "╚══██╔══╝██║████╗ ████║██╔════╝    ████╗ ████║██╔══██╗██╔════╝██║  ██║██║████╗  ██║██╔════╝"))
    print(color_text('purple', 'none',
                     "   ██║   ██║██╔████╔██║█████╗      ██╔████╔██║███████║██║     ███████║██║██╔██╗ ██║█████╗"))
    print(color_text('purple', 'bright',
                     "   ██║   ██║██║╚██╔╝██║██╔══╝      ██║╚██╔╝██║██╔══██║██║     ██╔══██║██║██║╚██╗██║██╔══╝"))
    print(color_text('purple', 'none',
                     "   ██║   ██║██║ ╚═╝ ██║███████╗    ██║ ╚═╝ ██║██║  ██║╚██████╗██║  ██║██║██║ ╚████║███████╗"))
    print(color_text('purple', 'bright',
                     "   ╚═╝   ╚═╝╚═╝     ╚═╝╚══════╝    ╚═╝     ╚═╝╚═╝  ╚═╝ ╚═════╝╚═╝  ╚═╝╚═╝╚═╝  ╚═══╝╚══════╝"))
    print("\n")

print(color_text('purple', 'back', "Minecraft Time Machine by " + __AUTHOR__))
print(color_text('green', 'bright', language['version'] + __VERSION__))
print(color_text('yellow', 'bright', language['text_mode'] + "\n"))

# Setting Discord Rich Presence environment
if config['discord_rich_presence']:
    from pypresence import Presence

    try:
        RPC = Presence(__CLIENT_ID__)
        RPC.connect()
        RPC.update(large_image='avatar',
                   large_text=language['discord_author'] + __AUTHORS_DISCORD__,
                   small_image='clock',
                   small_text="MCTimeMachine",
                   details=language['discord_choosing_date']
                   )
    except:  # I know, it's ugly.
        print(color_text('red', 'none', language['discord_rich_presence_error']))
        config['discord_rich_presence'] = False

# Showing the playback speed warning
if config['playback_speed'] > 10:
    print(color_text('red', 'none', language['playback_speed_warning']))
elif config['playback_speed'] <= 0:
    config['playback_speed'] = 1

# Getting the logs path
if config['logs_path'] == 'default':
    config['logs_path'] = os.getenv("APPDATA") + '\\.minecraft\\logs\\'

# Setting the date
print(language['supported_formats'])
while True:
    if config['selected_time'] != 'none':
        target_time_unparsed = str(config['selected_time'])
        print(color_text('green', 'none', language['target_time_set'] + target_time_unparsed))
    else:
        try:
            target_time_unparsed = input(color_text('purple', 'bright', language['target_time_input']))
        except KeyboardInterrupt:
            print(color_text('red', 'none', language['program_exit']))
            raise SystemExit

    # Processing the date and time
    try:
        target_time_parsed = {'date': target_time_unparsed.split(' ')[0],
                              'time': target_time_unparsed.split(' ')[1]}
    except IndexError:
        target_time_parsed = {'date': target_time_unparsed}
    try:
        if not os.path.exists(config['logs_path'] + target_time_parsed['date'] + '-1.log.gz'):
            raise FileNotFoundError
        if len(target_time_parsed['time'].split(':')) == 2:
            target_time_parsed['time'] += ':00'
        break
    except KeyError:
        break
    except FileNotFoundError:
        print(color_text('red', 'none',
                         language['time_not_found1'] + target_time_parsed['date'] + language['time_not_found2']))

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

# Loading the timestamps from logs into the list and converting them to UNIX timestamp
times = []
messages = []
for line in full_logs:
    times.append(int(
        mktime(ciso8601.parse_datetime(target_time_parsed['date'] + ' ' + line.split(' ')[0].strip('[]')).timetuple())))
    # Inserting the messages into the list
    if "[Client thread/INFO]" in line:
        messages.append(' '.join(line.split(' ')[4:]))
    else:
        messages.append(' '.join(line.split(' ')[3:]))

# Importing messages only from the given hour, if provided
try:
    messages = messages[times.index(take_closest(target_time_unparsed, times)) + 1:]
    times = times[times.index(take_closest(target_time_unparsed, times)) + 1:]
    if target_time_parsed['time']:
        print(color_text('green', 'none', language['moved_to_the_closest_time']))
except KeyError:
    pass
except ValueError:
    print(color_text('red', 'none', language['filter_error']))
    raise SystemExit

# Replacing the original values from the message with those from the configuration file
edited_messages = []
for message in messages:
    new_val = message
    for key, val in config['replace'].items():
        new_val = new_val.replace(key, val)
    edited_messages.append(new_val)
try:
    del new_val, messages
except NameError:
    print(color_text('red', 'none', language['time_range_exceeded']))
    raise SystemExit

# Updating Discord Rich Presence status
if config['discord_rich_presence']:
    RPC.update(large_image='clock',
               large_text="MCTimeMachine",
               small_image='avatar',
               small_text=language['discord_author'] + __AUTHORS_DISCORD__,
               details=language['discord_activity'],
               state=language['discord_target'] + target_time_parsed['date']
               )

# Displaying the messages
iterator = 0
for message in edited_messages:
    if config['spacing']:
        message += "\n"
    try:
        if config['show_timestamps']:
            print_with_timestamp(
                "[" + datetime.datetime.fromtimestamp(int(times[iterator])).strftime('%Y-%m-%d %H:%M:%S') + "]",
                colored_message(message))
        else:
            print(colored_message(message))
        try:
            interval = int(times[iterator + 1] - times[iterator]) / config['playback_speed']
            sleep(interval)
        except IndexError:
            pass
    except KeyboardInterrupt:
        print(color_text('red', 'none', language['program_exit']))
        raise SystemExit
    iterator += 1
