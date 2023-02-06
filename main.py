from dadata import Dadata
import sqlite3
import rsa

publickey, privatekey = rsa.newkeys(512)

def init():
    global result
    global API_KEY
    global lang
    global url
    global dataObject
    db = sqlite3.connect(r'settings.db')
    cursor = db.cursor()
    cursor.execute("SELECT * FROM settings;")
    result = cursor.fetchone()
    db.close()
    API_KEY = result[0]
    lang = result[1]
    url = 'address'
    dataObject = Dadata(API_KEY)


def settings():
    api = input('Введите API ключ, '
                'или оставьте пустую строку чтобы оставить по умолчанию: ')

    while True:
        lang = input('Ввдите язык на котром должен выводиться ответ en/ru, '
                     'или оставьте пустую строку чтобы оставить по умолчанию (ru): ')
        langoptions = ['en', 'ru', '']
        if lang in langoptions:
            break
        else:
            print(f'Введите один из предложенных вариантов{langoptions}')
            continue

    url = input('Введите базовый URL сервиса dadata, '
                'или оставьте пустую строку чтобы оставить по умолчанию (address): ')

    count = 0
    listval = [api, lang, url]
    for i in listval:
        if i == '':
            listval[count] = result[count]
            count += 1
        else: count += 1
    values = tuple(listval)
    db = sqlite3.connect('settings.db')
    cursor = db.cursor()
    cursor.execute("""UPDATE settings SET api = ?, lang = ?, url = ?""", values)
    db.commit()



def getdata(j, query):
    try:
        result = dataObject.suggest('address', query, 20, language=lang)
    except:
        print('Неверный токен API, перейдите в настройки и введите правильный токен')
        return "Неверный токен"
    if not result:
        print("Ничего не найдено по вашему запросу")
        return
    for i in result:
        list.append(i)
    for i in list:
        print(f'{j})', i['value'])
        j += 1
    select = ''
    while True:
        try:
            select = int(input('Введите номер варианта: '))
            select -= 1
            if select in range(len(list)):
                break
            else:
                print("Введите число от 1 до ", len(list))
                continue
        except ValueError:
            print('Пожалуйста введите число')
            continue
    val = list[select]['value']
    lat = list[select]['data']['geo_lat']
    lon = list[select]['data']['geo_lon']
    print(val, f'Широта {lat} Долгота {lon}')

init()
while True:
    list = []
    j = 1
    option = input('Введите 1, чтобы запустить программу \n'
                   'Введите 2 для перехода к настройкам \n'
                   'Введите 3 для выхода \n> ')
    if option == '1':
        query = str(input("Введите жалемый адрес или нажмите Enter для выхода: "))
        if query == '':
            break
        else:
            getdata(j, query)
    elif option == '2':
        settings()
        init()
    elif option == '3':
        break
    else:
        print("Выберите вариант от 1 до 3")