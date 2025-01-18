from behave import step
import common_variables
from api_tests import api_test as API
from pages import (
    BasePage,
    BrokersPage,
)


@step('user is on the "{page}" page')
def user_is_on_brokers_page(context, page):
    if not hasattr(common_variables, f'{page}_page'):
        raise Exception(f"The page '{page}' is not defined in common_variables!")
    url = getattr(common_variables, f'{page}_page')
    page = BasePage(context)
    page.navigate_to_url(url)


@step('user retrieve all broker names')
def retrieve_all_broker_names(context):
    page = BrokersPage(context)
    page.get_all_broker_names()


@step('user retrieve first visible broker names')
def retrieve_first_broker_names(context):
    page = BrokersPage(context)
    page.get_first_visible_broker_names()


@step('user search for each broker and verify their details')
def search_for_each_broker_and_verify(context):
    page = BrokersPage(context)
    page.search_for_broker_and_verify()


@step('user retrieve broker data from Yavlena API for "{city}"')
def user_make_api_broker_requests(context, city):
    context.base_url = f"https://www.yavlena.com/en/api/broker?city={city}"


@step('user make API requests for all brokers')
def user_combine_api_data(context):
    API.combine_all_broker_data(context.base_url)


@step('user extract the following data for each broker and print it as plain text')
def user_extract_brokers_api_data(context):
    fields = [row['Field'] for row in context.table]
    API.extract_and_print_broker_data(fields)


@step('user extract the following data for each broker and print it as table')
def user_extract_brokers_api_data(context):
    fields = [row['Field'] for row in context.table]
    API.extract_and_print_broker_data_table(fields)
