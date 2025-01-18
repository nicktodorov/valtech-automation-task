import requests
from tabulate import tabulate
import common_variables


def fetch_broker_data(base_url, page):
    url = f"{base_url}&page={page}"
    headers = {
        'accept': '*/*',
        'cookie': '__Host-next-auth.csrf-token=f65143f0660f4e46312f59dc408998d323b24da9dce7286b3d9b1a62f001efda%7C91cebc41fd023bb02cf7af5af8cf79c65b6a77c374ae3d42efb623ef6f5ffb3c; __Secure-next-auth.callback-url=https%3A%2F%2Fwww.yavlena.com',
        'referer': 'https://www.yavlena.com/en/broker?city=Sofia',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36'
    }
    response = requests.get(url, headers=headers)
    assert response.status_code == 200, f"Unexpected status code {response.status_code} for page {page}!"
    return response.json()


def combine_all_broker_data(base_url):
    common_variables.all_broker_api_data["brokers"] = []
    page = 1
    while True:
        data = fetch_broker_data(base_url, page)
        brokers = data["brokers"]
        if brokers:
            common_variables.all_broker_api_data["brokers"].extend(brokers)
            page += 1
        else:
            break


def extract_and_print_broker_data(fields):
    brokers = common_variables.all_broker_api_data.get("brokers", [])
    for broker in brokers:
        for field in fields:
            if field in broker:
                print(f"{field.capitalize()}: {broker[field]}")
        print("-" * 20)


def extract_and_print_broker_data_table(fields):
    brokers = common_variables.all_broker_api_data.get("brokers", [])
    table_headers = ['Row Number'] + fields
    table_rows = []
    for idx, broker in enumerate(brokers, start=1):
        row = [idx]
        for field in fields:
            if field in broker:
                row.append(broker[field])
            else:
                row.append("N/A")
        table_rows.append(row)
    print("\nBroker Data Table:")
    print(tabulate(table_rows, headers=table_headers, tablefmt="grid"))
