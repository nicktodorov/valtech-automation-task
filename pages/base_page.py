import time
from playwright.sync_api import Page, expect


class BasePage(object):
    __TIMEOUT = 15000

    def __init__(self, context):
        self.context = context

    def find_element(self, locator: str) -> object:
        """
            Finds and returns the element located by the specified locator.
            Args:
                locator (str): The locator (e.g., CSS selector, XPath) used to find the element.
            Returns:
                Object: A Playwright Locator object that represents the found element.
            """
        return self.context.page.locator(locator)

    def find_all_elements(self, locator: str) -> list[object]:
        """
            Finds all visible elements located by the specified locator.
            Args:
                locator (str): The locator (e.g., CSS selector, XPath) used to find the elements.
            Returns:
                list[objects]: A list of Playwright objects representing the visible elements.
            Raises:
                Exception: If no elements or no visible elements are found.
            """
        elements = self.context.page.locator(locator).all()
        if not elements:
            raise Exception(f'No elements found with locator {locator}!')
        visible_elements = [element for element in elements if element.is_visible()]
        if not visible_elements:
            raise Exception(f'No visible elements found with locator {locator}!')
        visible_elements_amount = len(visible_elements)
        print(f'===> {visible_elements_amount} visible elements with "{locator}" found from total {len(elements)}.')
        return visible_elements

    def verify_element_visible(self, locator: str, timeout: int = __TIMEOUT):
        """
            Verifies that the element located by the specified locator is visible within the given timeout.
            Args:
                locator (str): The locator (e.g., CSS selector, XPath) used to find the element.
                timeout (int, optional): The maximum time (in milliseconds) to wait for the element to be visible. Defaults to the value of __TIMEOUT.
            Raises:
                TimeoutError: If the element is not visible within the specified timeout.
            """
        self.context.page.wait_for_selector(locator, timeout=timeout)
        expect(self.find_element(locator)).to_be_visible()
        print(f'===> Verified element "{locator}" is visible')

    def click(self, locator: str):
        """
            Clicks the element located by the specified locator after scrolling it into view if needed.
            Args:
                locator (str): The locator (e.g., CSS selector, XPath) used to find the element.
            """
        element = self.find_element(locator)
        element.scroll_into_view_if_needed()
        element.click()
        print(f'===> Clicked element "{locator}"')

    def get_text(self, locator: str) -> str:
        """
            Retrieves the text content of the element located by the specified locator.
            Args:
                locator (str): The locator (e.g., CSS selector, XPath) used to find the element.
            Returns:
                str: The text content of the located element.
            """
        print(f'===> Getting text from element "{locator}"...')
        return self.find_element(locator).text_content()

    def get_text_from_object(self, element: object) -> str:
        """
            Retrieves the text content of Playwright object element.
            Args:
                element (ElementHandle): The Playwright element handle from which to retrieve the text content.
            Returns:
                str: The text content of the specified element.
            """
        print(f'===> Getting text from element "{element}"...')
        return element.text_content()

    def enter_text(self, locator: str, text: str):
        """
            Enters the specified text into an input field identified by the given locator.
            Args:
                locator (str): The locator for the input field where the text will be entered.
                text (str): The text to be entered into the input field.
            """
        self.find_element(locator).press_sequentially(text)
        print(f'===> Entered "{text}" in "{locator}" field')

    def enter_text_with_clear(self, locator: str, text:str):
        """
            Clears the text from an input field and then enters the specified text.
            Args:
                locator (str): The locator for the input field to be cleared and filled.
                text (str): The text to be entered into the input field.
            """
        element = self.find_element(locator)
        element.clear()
        element.press_sequentially(text)
        print(f'===> Entered "{text}" with clear in "{locator}" field')

    def navigate_to_url(self, url: str):
        """
            Navigates the browser to the specified URL.
            Args:
                url (str): The URL to navigate to.
            """
        self.context.page.goto(url)

    def scroll_slowly_until_element_in_viewport(self, locator: str, max_retries:int = 100, wait_time: float = 0.5):
        """
            Scrolls the page slowly until the element with the specified locator is in the viewport.
            Args:
                locator (str): The locator of the element to check.
                max_retries (int, optional): The maximum number of retries to check if the element is in the viewport. Defaults to 100.
                wait_time (float, optional): The amount of time (in seconds) to wait before retrying. Defaults to 0.5.
            Returns:
                Locator: The locator of the element that has been found in the viewport.
            Raises:
                Exception: If the element is not found in the viewport after the specified number of retries.
            """
        for _ in range(max_retries):
            element = self.context.page.locator(locator)
            try:
                expect(element).to_be_in_viewport(timeout=wait_time)
                print(f"Element {locator} found within viewport.")
                return element
            except:
                pass
            print(f"Element not visible in viewport, retrying ({_ + 1}/{max_retries})...")
            self.context.page.evaluate("window.scrollBy(0, 100);")
            time.sleep(wait_time)
        raise Exception(f"Element with locator '{locator}' not found in viewport after {max_retries} retries.")
