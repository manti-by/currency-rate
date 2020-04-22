import sqlite3

from app import DB_PATH, TRENDING_COUNT


def get_data() -> dict:
    with sqlite3.connect(DB_PATH) as session:
        session.row_factory = sqlite3.Row
        cursor = session.cursor()
        cursor.execute(
            "SELECT usd_buy, usd_sell, eur_buy, eur_sell, rur_buy, rur_sell, datetime "
            "FROM exchange_rates ORDER BY datetime LIMIT ?",
            (TRENDING_COUNT, ),
        )
        session.commit()

        # Calculating trends for exchange rates
        data = {
            'usd_buy': 0,
            'usd_sell': 0,
            'eur_buy': 0,
            'eur_sell': 0,
            'rur_buy': 0,
            'rur_sell': 0,
        }
        for item in cursor.fetchall():
            for key in data:
                data[key] += item[key]

        return_data = dict(zip([c[0] for c in cursor.description], item))

        for key in data:
            return_data['{}_trend'.format(key)] = round(
                return_data[key] - data[key] / TRENDING_COUNT, 2
            )

        return return_data


def save_data(data: dict):
    with sqlite3.connect(DB_PATH) as connection:
        cursor = connection.cursor()
        cursor.execute(
            "INSERT INTO exchange_rates (usd_buy, usd_sell, eur_buy, eur_sell, rur_buy, rur_sell) "
            "VALUES (?, ?, ?, ?, ?, ?)",
            (data['usd_buy'], data['usd_sell'], data['eur_buy'],
             data['eur_sell'], data['rur_buy'], data['rur_sell']),
        )
        connection.commit()