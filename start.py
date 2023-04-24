import itertools
import requests
from colorama import init, Fore
from colorama import Back
from colorama import Style
import time
import os

def clear_screen():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')

ROBOT = r"""
  \o/
   |        Email generator and checker by Timur Vendin
  / \
"""

ROBOT1 = r"""
   o
  /|\       Email generator and checker by Timur Vendin
  / \
"""

for i in range(5):
    clear_screen()
    print(ROBOT)
    time.sleep(0.2)
    clear_screen()
    print(ROBOT1)
    time.sleep(0.2)

init(autoreset=True)

print(Fore.BLUE + 'Введите имя: \n Gib Vornamen ein')
name = input()
print(Fore.BLUE + 'Введите фамилию: \n Gib Nachnamen ein')
surname = input()

payload = {}
headers= {
  "apikey": "uXs0rUPkQaIvl6Xc99Guma2QAmBBzW0v" # Вставьте сюда свой API для email verify c apilayer.com
}

# Загружаем список email провайдеров
with open('service.txt', 'r') as f:
    email_providers = [line.strip() for line in f.readlines()]

# Функция, которая генерирует все возможные варианты email'ов для заданного имени и фамилии
def generate_email_combinations(name, surname, email_providers):
    # Генерируем все возможные комбинации имени и фамилии
    name_combinations = list(itertools.product(name.split(), surname.split()))

    # Генерируем все возможные email'ы для каждой комбинации
    email_combinations = []
    for name_combination in name_combinations:
        for provider in email_providers:
            email_combinations.append('{}{}{}'.format(name_combination[0], name_combination[1], provider))
            email_combinations.append('{}.{}{}'.format(name_combination[0], name_combination[1], provider))
            email_combinations.append('{}{}{}'.format(name_combination[1], name_combination[0], provider))
            email_combinations.append('{}.{}{}'.format(name_combination[1], name_combination[0], provider))
            #print (email_combinations[provider])
    
    return email_combinations
    
def write_to_txt(variable, filename):
    with open(filename, 'a') as f:
        f.write(str(variable) + '\n')

# Функция, которая проверяет email на существование
def verify_email(email):
    #api_key = 'uXs0rUPkQaIvl6Xc99Guma2QAmBBzW0v'
    url = f"https://api.apilayer.com/email_verification/check?email={email}"
    response = requests.request("GET", url, headers=headers, data = payload)
    status_code = response.status_code
    result = response.json()#response.text
    if result['smtp_check'] == True and result['format_valid'] == True:
        return True
    else:
        return False

# Пример использования
#name = 'Andrea'
#surname = 'Gomber'
email_combinations = generate_email_combinations(name, surname, email_providers)
for email in email_combinations:
    print(Fore.GREEN + 'Email "{}" найден | Die E-Mail ist gefunden'.format(email))
    write_to_txt(email, "total.txt")
    if verify_email(email):
        print(Fore.GREEN + 'Email "{}" существует | Die E-Mail existiert'.format(email))
        write_to_txt(email, "good.txt")
    else:
        print(Fore.RED + 'Email "{}" не существует| Die E-Mail nicht existiert'.format(email))
        write_to_txt(email, "ng.txt")
