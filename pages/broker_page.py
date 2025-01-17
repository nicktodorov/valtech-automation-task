import time
import common_variables
from pages.base_page import BasePage
from locators import *


class BrokersPage(BasePage):
    def __init__(self, context):
        BasePage.__init__(self, context)

    def get_all_broker_names(self):
        self.scroll_slowly_until_element_in_viewport(FOOTER_SECTION)
        time.sleep(5)
        found_brokers = self.find_all_elements(BROKER_NAME_LABEL)
        for item in found_brokers:
            broker_name = self.get_text_from_object(item)
            common_variables.brokers.append(broker_name)
        assert len(found_brokers) > 0,'No brokers found!'
        print(f'Brokers: {common_variables.brokers}')

    def get_first_visible_broker_names(self):
        self.verify_element_visible(NAME_SEARCH_FIELD)
        found_brokers = self.find_all_elements(BROKER_NAME_LABEL)
        for item in found_brokers:
            broker_name = self.get_text_from_object(item)
            common_variables.brokers.append(broker_name)
        assert len(found_brokers) > 0,'No brokers found!'
        print(f'Brokers: {common_variables.brokers}')

    def search_for_broker_and_verify(self):
        more_than_one_broker_found = []
        brokers_with_missing_data = {}
        for broker in common_variables.brokers:
            self.enter_text_with_clear(NAME_SEARCH_FIELD, broker)
            time.sleep(1)
            found_brokers = self.find_all_elements(BROKER_NAME_LABEL)
            if len(found_brokers) != 1:
                for item in found_brokers:
                    broker_name = self.get_text_from_object(item)
                    more_than_one_broker_found.append(broker_name)
                raise Exception(f'More than one broker found! Should be only {broker}, '
                                f'but found ones are: {more_than_one_broker_found}')
            self.click(EXPAND_BROKER_DETAILS_BUTTON)
            missing_data = []
            try:
                self.verify_element_visible(BROKER_ADDRESS_LABEL)
            except:
                missing_data.append("Address")
            try:
                self.verify_element_visible(BROKER_LANDLINE_PHONE_LABEL)
            except:
                missing_data.append("Landline Phone")
            try:
                self.verify_element_visible(BROKER_MOBILE_PHONE_LABEL)
            except:
                missing_data.append("Mobile Phone")
            try:
                self.verify_element_visible(BROKER_ASSIGNED_PROPERTIES_LABEL)
            except:
                missing_data.append("Assigned Properties")
            if missing_data:
                brokers_with_missing_data[broker] = missing_data
        if brokers_with_missing_data:
            raise Exception(f'The following brokers have missing data:\n {brokers_with_missing_data}')

