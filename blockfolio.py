import click
import requests
from tabulate import tabulate

base = 'http://blockfoliorest-pxrpmzggzv.elasticbeanstalk.com/rest'


def get_all_positions(device_id):
    data = requests.get(f'{base}/get_all_positions/{device_id}').json()
    return ['{base}-{coin}'.format_map(p) for p in data['positionList'] if p['quantity'] > 0]


def get_coin_summary(device_id, pair, fiat_currency='USD'):
    url = f'{base}/get_coin_summary/{device_id}/{pair}'
    data = requests.get(url, params={'fiat_currency': fiat_currency}).json()
    h = data['holdings']
    return {
        'coin': h['coin'],
        'holdings': h['quantityString'],
        'net cost': h['netCostString'],
        'market value': h['holdingValueString'],
        'profit/loss': h['lifetimeChangeString'],
    }


@click.command()
@click.argument('device_id')
def main(device_id):
    pairs = get_all_positions(device_id)
    summaries = []
    for pair in pairs:
        summaries.append(get_coin_summary(device_id, pair))
    print(tabulate(summaries, headers='keys'))


if __name__ == '__main__':
    main()
