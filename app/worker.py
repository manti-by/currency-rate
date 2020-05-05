import json
import requests
import xml.etree.ElementTree as ET

from app.database import get_data, save_data

if __name__ == '__main__':
    response = requests.get('https://www.mtbank.by/currxml.php?ver=2')
    if response.status_code == 200:
        data = {
            'usd_buy': 0,
            'usd_sell': 0,
            'eur_buy': 0,
            'eur_sell': 0,
            'rur_buy': 0,
            'rur_sell': 0,
        }
        for child in ET.fromstring(response.content):
            if child.attrib.get('id') == '168,768,968,868':
                for currency in child.findall('currency'):
                    code = currency.find('code').text
                    code_to = currency.find('codeTo').text

                    print('.')
                    if (
                        (code == 'BYN' and code_to == 'USD') or
                        (code == 'USD' and code_to == 'BYN')
                    ):
                        data['usd_buy'] = float(currency.find('purchase').text)
                        data['usd_sell'] = float(currency.find('sale').text)

                    if (
                        (code == 'BYN' and code_to == 'EUR') or
                        (code == 'EUR' and code_to == 'BYN')
                    ):
                        data['eur_buy'] = float(currency.find('purchase').text)
                        data['eur_sell'] = float(currency.find('sale').text)

                    if (
                        (code == 'BYN' and code_to == 'RUB') or
                        (code == 'RUB' and code_to == 'BYN')
                    ):
                        data['rur_buy'] = float(currency.find('purchase').text)
                        data['rur_sell'] = float(currency.find('sale').text)
        save_data(data)

    print(json.dumps(get_data()))
