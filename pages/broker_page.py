import time
import common_variables
from pages.base_page import BasePage
from locators import *


class BrokersPage(BasePage):
    def __init__(self, context):
        BasePage.__init__(self, context)

    def get_all_broker_names(self):
        """
            Extracts broker names from the UI and stores them in a global list.

            This method scrolls the page until the footer section is in the viewport, waits for
            5 seconds to make sure all brokers were loaded and displayed, and then finds all elements with the broker
            name label. Each broker's name is extracted and appended to a global list `common_variables.brokers`.
            The function asserts that at least one broker is found. If no brokers are found, it raises
            an AssertionError with a custom message.
            Modifies:
                common_variables.brokers (list): The broker names are added to this list.
            Raises:
                AssertionError: If no broker names are found after scrolling and waiting for the page to load.
            """
        self.scroll_slowly_until_element_in_viewport(FOOTER_SECTION)
        time.sleep(5)
        found_brokers = self.find_all_elements(BROKER_NAME_LABEL)
        for item in found_brokers:
            broker_name = self.get_text_from_object(item)
            common_variables.brokers.append(broker_name)
        assert len(found_brokers) > 0,'No brokers found!'

    def get_first_visible_broker_names(self):
        """
            Extracts broker names from the first visible elements on the UI and stores them in a global list.

            This method first verifies the visibility of the element corresponding to the search field
            (`NAME_SEARCH_FIELD`). It then retrieves all broker name elements on the page, extracts
            the text from each of these elements, and appends the broker names to a global list
            `common_variables.brokers`. The function asserts that at least one broker name is found.
            If no brokers are found, it raises an AssertionError with a custom message.
            Modifies:
                common_variables.brokers (list): The broker names are added to this list.
            Raises:
                AssertionError: If no broker names are found after verifying visibility and retrieving the elements.
            """
        self.verify_element_visible(NAME_SEARCH_FIELD)
        found_brokers = self.find_all_elements(BROKER_NAME_LABEL)
        for item in found_brokers:
            broker_name = self.get_text_from_object(item)
            common_variables.brokers.append(broker_name)
        assert len(found_brokers) > 0,'No brokers found!'

    def search_for_broker_and_verify(self):
        """
            Searches for each broker by name, verifies that only one broker is found,
            and checks for the visibility of key broker information.

            For each broker name in the `common_variables.brokers` list, this method:
            1. Enters the broker's name into a search field (`NAME_SEARCH_FIELD`).
            2. Verifies that exactly one broker is found. If more than one broker is found, it collects
               the names of the brokers and raises an exception.
            3. Clicks to expand the broker details.
            4. Verifies the visibility of key broker information (Address, Landline Phone, Mobile Phone,
               Assigned Properties). If any of these elements are missing, it adds the missing data to a
               list for the current broker.
            5. At the end of the loop, if any broker is found with missing data, it raises an exception
               detailing which brokers are missing what information.
            Modifies:
                common_variables.brokers (list): The brokers that are being searched for.
            Raises:
                Exception: If more than one broker is found when searching for a specific broker, or if any broker
                          is missing key information (address, phone, assigned properties).
            """
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

