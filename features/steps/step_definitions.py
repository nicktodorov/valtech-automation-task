from behave import step
import common_variables
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
