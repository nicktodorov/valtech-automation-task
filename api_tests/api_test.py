import requests
from tabulate import tabulate
import common_variables


def fetch_broker_data(base_url: str, page: int) -> dict[str, any]:
    """
        Fetch broker data from the specified URL for a given page.

        Args:
            base_url (str): The base URL for the broker data API.
            page (int): The page number to retrieve data for.
        Returns:
            dict: A dictionary containing the broker data, including total count and a list of brokers.
                The structure of the response is expected to have:
                - 'totalCount' (int): Total number of brokers.
                - 'brokers' (list): A list of brokers, each represented by a dictionary.
        Raises:
            AssertionError: If the response status code is not 200.
        """
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


def combine_all_broker_data(base_url: str):
    """
        Combine all broker data from multiple pages of the broker API into a single collection.

        This function repeatedly fetches broker data from the provided base URL, page by page,
        and appends the brokers to the common collection `common_variables.all_broker_api_data["brokers"]`.
        The process continues until there are no more brokers to fetch.

        Args:
            base_url (str): The base URL for the broker data API. The page number will be appended to this URL
                            to fetch data for each page.
        Modifies:
            common_variables.all_broker_api_data["brokers"] (list): A list that holds the combined broker data
                                                                    across all pages. This list will be populated
                                                                    with the brokers fetched from the API.
        """
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


def extract_and_print_broker_data(fields: list[str]):
    """
       Extract and print specific fields from the broker data.

       This function iterates over the brokers in `common_variables.all_broker_api_data["brokers"]`,
       and for each broker, it checks if the specified fields exist. If a field exists,
       it prints the field name (capitalized) and its corresponding value. Each broker's
       data is separated by a line of dashes.

       Args:
           fields (list of str): A list of field names to extract and print from each broker's data.
                                 Each field will be checked for existence in the broker's dictionary.
       Prints:
           The specified fields and their values for each broker in the form:
           "<Field>: <Value>"
           Each broker's data is followed by a line of dashes for separation.
       """
    brokers = common_variables.all_broker_api_data.get("brokers", [])
    for broker in brokers:
        for field in fields:
            if field in broker:
                print(f"{field.capitalize()}: {broker[field]}")
        print("-" * 20)


def extract_and_print_broker_data_table(fields: list[str]):
    """
        Extract specified fields from broker data and display it as a formatted table.

        This function constructs a table where each row represents a broker and each column
        corresponds to a field from the `fields` list. It also includes a "Row Number" column
        at the start. For each broker, if a field is missing, "N/A" is displayed in its place.
        The table is printed in a grid format using the `tabulate` library.

        Args:
            fields (list of str): A list of field names to extract and display for each broker.
                                  Each field will be checked for existence in the broker's dictionary.
        Prints:
            A formatted table showing the broker data with the specified fields. Each row corresponds
            to a broker, and missing fields are represented as "N/A".
        """
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
