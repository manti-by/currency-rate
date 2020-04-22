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
                    if (
                        currency.find('code').text == 'BYN'
                        and currency.find('codeTo').text == 'USD'
                    ):
                        data['usd_buy'] = float(currency.find('purchase').text)
                        data['usd_sell'] = usd_sell = float(currency.find('sale').text)
                    if (
                        currency.find('code').text == 'BYN'
                        and currency.find('codeTo').text == 'EUR'
                    ):
                        data['eur_buy'] = float(currency.find('purchase').text)
                        data['eur_sell'] = float(currency.find('sale').text)
                    if (
                        currency.find('code').text == 'BYN'
                        and currency.find('codeTo').text == 'RUB'
                    ):
                        data['rur_buy'] = float(currency.find('purchase').text)
                        data['rur_sell'] = float(currency.find('sale').text)
        save_data(data)

    print(json.dumps(get_data()))
