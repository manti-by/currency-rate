import sqlite3

from app import DB_PATH


def get_data() -> dict:
    with sqlite3.connect(DB_PATH) as session:
        session.row_factory = sqlite3.Row
        cursor = session.cursor()

        cursor.execute("""
            SELECT datetime
            FROM exchange_rates
            WHERE date(datetime) < date('now', '-1 day')
            ORDER BY datetime DESC;
        """)
        session.commit()

        previous_day = cursor.fetchone()[0]

        cursor.execute("""
            SELECT
              (AVG(usd_buy) + AVG(usd_sell)) / 2 as usd,
              (AVG(eur_buy) + AVG(eur_sell)) / 2 as eur,
              (AVG(rur_buy) + AVG(rur_sell)) / 2 as rur,
              date(datetime) as date
            FROM exchange_rates
            WHERE date(datetime) < ?
            ORDER BY datetime DESC;
        """, (previous_day,))
        session.commit()

        yesterday = dict(zip(
            [c[0] for c in cursor.description], cursor.fetchone()
        ))

        cursor.execute("""
            SELECT
              (AVG(usd_buy) + AVG(usd_sell)) / 2 as usd,
              (AVG(eur_buy) + AVG(eur_sell)) / 2 as eur,
              (AVG(rur_buy) + AVG(rur_sell)) / 2 as rur,
              date(datetime) as date
            FROM exchange_rates
            WHERE date(datetime) = date('now')
            ORDER BY datetime DESC;
        """)
        session.commit()

        today = dict(zip(
            [c[0] for c in cursor.description], cursor.fetchone()
        ))

        today['usd_trend'] = today['usd'] - yesterday['usd']
        today['eur_trend'] = today['eur'] - yesterday['eur']
        today['rur_trend'] = today['rur'] - yesterday['rur']

        return today


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

