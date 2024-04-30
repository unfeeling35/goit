import argparse
import asyncio
import logging
import platform
from datetime import datetime, timedelta

from aiohttp import ClientSession, ClientConnectorError

CURRENCY = ['USD', 'EUR']
URL_PB = 'https://api.privatbank.ua/p24api/exchange_rates?json'


def command_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "days",
        default=1,
        nargs='?',
        choices=range(1, 11),
        type=int)
    parser.add_argument(
        "--currency", "-c",
        nargs='+',
        required=False,
        default=['USD', 'EUR'],
        type=str)
    return vars(parser.parse_args())


async def get_currency_request(url):
    async with ClientSession() as session:
        try:
            async with session.get(url) as resp:
                if resp.ok:
                    r = await resp.json()
                    return r
                logging.error(f'Error status {resp.status} for {url}')
                return None
        except ClientConnectorError as e:
            logging.error(f"Connection error {str(e)}")
        return None


async def get_currency(days=0):
    dates = [
        (datetime.now() - timedelta(days=x)).strftime('%d.%m.%Y')
        for x in range(days)]
    exchange_rate_data = [
        get_currency_request(f'{URL_PB}&date={date}')
        for date in dates]
    results = await asyncio.gather(*exchange_rate_data)
    for result in results:
        if result:
            parse_currency(result)


def parse_currency(exchange_rate):
    date = exchange_rate['date']
    print(f'\n{date}:')
    for rate in exchange_rate['exchangeRate']:
        if rate['currency'] in CURRENCY:
            print(f'{rate["currency"]} sale: {rate["saleRate"]} purchase: {rate["purchaseRate"]}')


async def main():
    args = command_parser()
    number_of_days = int(args.get('days'))
    if number_of_days > 10:
        print('The date range must be less than or equal to 10 days')
        number_of_days = 10
    await get_currency(number_of_days)


if __name__ == '__main__':
    if platform.system() == 'Windows':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    asyncio.run(main())
