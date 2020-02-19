"""
Minecraft Time Machine
Tryb tekstowy
Autor: Buty935 aka workonfire
"""

__VERSION__ = '1.0.1 ALPHA'

# TODO: Niestandardowe formaty
# TODO: Losowy czas
# TODO: Komentarze w tworzeniu domyślnego config.yml

# Wczytanie wymaganych bibliotek
from colors import color_print, colored_message
from time import sleep, mktime
import gzip, shutil, os, atexit, yaml, datetime, ciso8601

# Usunięcie plików logów przy wyjściu z programu
def exit_handler():
    try:
        shutil.rmtree('temp')
    except FileNotFoundError:
        pass

atexit.register(exit_handler)

# Zdefiniowanie funckji do wyświetlania kolorowych wiadomości
def print_with_timestamp(colored_timestamp, colored_message):
    import colorama
    print(colorama.Style.BRIGHT + colorama.Fore.CYAN + colored_timestamp + " " + colorama.Fore.WHITE + colored_message)

# Zdefiniowanie funkcji odpowiadającej za korekcję czasu
def take_closest(shot, target):
    return int(min(target, key=lambda x: abs(x - int(mktime(ciso8601.parse_datetime(shot).timetuple())))))

# Wczytanie pliku konfiguracyjnego
try:
    with open('config.yml') as config_file:
        config = yaml.load(config_file, Loader=yaml.FullLoader)
except FileNotFoundError:
    # Ustalenie domyślnych wartości pliku konfiguracyjnego
    with open('config.yml', 'w') as config_file:
        yaml.dump({
            'show_timestamps': True,
            'selected_time': 'none',
            'logs_path': 'default',
        }, config_file)
    with open('config.yml') as config_file:
        config = yaml.load(config_file, Loader=yaml.FullLoader)

# Powitanie
color_print('cyan', "Minecraft Time Machine")
color_print('blue', "Wersja " + __VERSION__)
color_print('yellow', "Tryb tekstowy\n")

# Ostrzeżenie o prędkości odtwarzania czatu
if config['playback_speed'] > 5:
    color_print('red', "UWAGA! Prędkość odtwarzania czatu o wartości większej niż 5x może skutkować brakiem czytelności czatu, a wysokie wartości mogą skutkować crashem programu.")
elif config['playback_speed'] <= 0:
    config['playback_speed'] = 1

# Ustalenie ścieżki pliku z logami
if config['logs_path'] == 'default':
    config['logs_path'] = os.getenv("APPDATA") + '\.minecraft\logs\\'

# Ustalenie daty
color_print('magenta', "Obsługiwany format: YYYY-MM-DD [HH:mm:ss]")
while True:
    if config['selected_time'] != 'none':
        target_time_unparsed = str(config['selected_time'])
        color_print('green', "Cel podróży: " + target_time_unparsed)
    else:
        target_time_unparsed = input("Wprowadź datę, do której chcesz się przenieść: ")

    # Przetworzenie daty i godziny
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
        color_print('red', "Nie znaleziono żadnych wiadomości odnoszących się do daty " + target_time_parsed['date'] + ". Sprawdź ścieżkę logów w pliku konfiguracyjnym (config.yml).")

# Ustalenie ilości plików z logami
logs_files = []
for filename in os.listdir(config['logs_path']):
    if filename.endswith('.log.gz') and filename[:10] == target_time_parsed['date']:
        logs_files.append(filename)

# Wypakowywanie plików z logami
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

# Wczytanie zawartości plików z logami do listy
full_logs = []
if config['filter'] == 'default':
    config['filter'] = "[CHAT]"
with open('temp\\used.log') as used_log_file:
    for line in used_log_file.readlines():
        if config['filter'] in line:
            full_logs.append(line.rstrip())

# Wczytanie znaczników czasów z logów do listy i przekonwertowanie ich na czas uniksowy (GMT+1)
times = []
messages = []
for line in full_logs:
    times.append(int(mktime(ciso8601.parse_datetime(target_time_parsed['date'] + ' ' + line.split(' ')[0].strip('[]')).timetuple())))
    # Wczytanie wiadomości z logów do listy
    messages.append(' '.join(line.split(' ')[3:]))

# Pobieranie wiadomości tylko z podanej godziny, jeśli została podana
try:
    messages = messages[times.index(take_closest(target_time_unparsed, times)) + 1:]
    times = times[times.index(take_closest(target_time_unparsed, times)) + 1:]
    if target_time_parsed['time']:
        color_print('green', "Nie znaleziono żadnych wiadomości z podanej przez ciebie godziny, więc przeniesiono cię do najbliższej")
except KeyError:
    pass
except ValueError:
    color_print('red', "Wystąpił niespodziewany błąd. Sprawdź swój plik konfiguracyjny.")
    raise SystemExit

# Zamiania oryginalnych wartości z wiadomości na te z pliku konfiguracyjnego
edited_messages = []
for message in messages:
    new_val = message
    for key, val in config['replace'].items():
        new_val = new_val.replace(key, val)
    edited_messages.append(new_val)
del new_val, messages

# Wyświetlenie wiadomości
iterator = 0
for message in edited_messages:
    if config['show_timestamps']:
        print_with_timestamp("[" + datetime.datetime.fromtimestamp(int(times[iterator])).strftime('%Y-%m-%d %H:%M:%S') + "]", colored_message(message))
    else:
        print(colored_message(message))
    try:
        sleep(int(times[iterator + 1] - times[iterator]) / config['playback_speed'])
    except IndexError:
        pass
    iterator += 1
