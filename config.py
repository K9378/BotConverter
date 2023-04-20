import requests
data = requests.get('https://www.cbr-xml-daily.ru/daily_json.js').json()


def convert(val1, val2):
    val1 = val1.upper()
    val2 = val2.upper()
    if val1 == 'RUB':
        current = 1/data['Valute'][val2]['Value']
    elif val2 == 'RUB':
        current = data['Valute'][val1]['Value']
    else:
        current = data['Valute'][val1]['Value']/data['Valute'][val2]['Value']
    return current


def actual():
    a = ''
    x = []
    for i in data['Valute']:
        c = ' '.join(map(str, (i, data['Valute'][i]['Nominal'], data['Valute'][i]['Name'], ' = ', data['Valute'][i]['Value'], 'Рублей.\n')))
        x.append(c)
        a = ''.join(x)

    return a

def check_func(v1, v2):
    check = []
    v1 = v1.upper()
    v2 = v2.upper()
    print(v1)
    for i in data['Valute']:
        if i == v1:
            check.append(1)

    for i in data['Valute']:
        if i == v2:
            check.append(1)
    return check


