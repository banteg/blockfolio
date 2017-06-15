import click
import requests
from tabulate import tabulate

base = 'http://blockfoliorest-pxrpmzggzv.elasticbeanstalk.com/rest'


def get_all_positions(device_id):
    data = requests.get(f'{base}/get_all_positions/{device_id}').json()
    return ['{base}-{coin}'.format_map(p) for p in data['positionList'] if p['quantity'] > 0]


def get_coin_summary(device_id, pair, fiat_currency=None):
    url = f'{base}/get_coin_summary/{device_id}/{pair}'
    params = {'fiat_currency': fiat_currency} if fiat_currency else {}
    return requests.get(url, params=params).json()


def format_summary(data, fiat=False):
    Fiat = 'Fiat' if fiat else ''
    h = data['holdings']
    return {
        'coin': h['coin'],
        'holdings': h['quantityString'],
        'net cost': h[f'netCost{Fiat}String'],
        'market value': h[f'holdingValue{Fiat}String'],
        'profit/loss': h[f'lifetimeChange{Fiat}String'],
    }


@click.command()
@click.argument('device_id')
@click.option('-f', '--fiat', help='Fiat currency')
def main(device_id, fiat):
    pairs = get_all_positions(device_id)
    summaries = []
    for pair in pairs:
        summary = get_coin_summary(device_id, pair, fiat)
        summaries.append(format_summary(summary, bool(fiat)))
    print(tabulate(summaries, headers='keys'))


if __name__ == '__main__':
    main()
