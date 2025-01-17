import time
from playwright.sync_api import Page, expect


class BasePage(object):
    __TIMEOUT = 15000

    def __init__(self, context):
        self.context = context

    def find_element(self, locator):
        return self.context.page.locator(locator)

    def find_all_elements(self, locator):
        elements = self.context.page.locator(locator).all()
        if not elements:
            raise Exception(f'No elements found with locator {locator}!')
        visible_elements = [element for element in elements if element.is_visible()]
        if not visible_elements:
            raise Exception(f'No visible elements found with locator {locator}!')
        visible_elements_amount = len(visible_elements)
        print(f'===> {visible_elements_amount} visible elements with "{locator}" found from total {len(elements)}.')
        return visible_elements

    def verify_element_visible(self, locator, timeout=__TIMEOUT):
        self.context.page.wait_for_selector(locator, timeout=timeout)
        expect(self.find_element(locator)).to_be_visible()
        print(f'===> Verified element "{locator}" is visible')


    def click(self, locator):
        element = self.find_element(locator)
        element.scroll_into_view_if_needed()
        element.click()
        print(f'===> Clicked element "{locator}"')

    def get_text(self, locator):
        print(f'===> Getting text from element "{locator}"...')
        return self.find_element(locator).text_content()

    def get_text_from_object(self, element):
        print(f'===> Getting text from element "{element}"...')
        return element.text_content()

    def enter_text(self, locator, text):
        self.find_element(locator).press_sequentially(text)
        print(f'===> Entered "{text}" in "{locator}" field')

    def enter_text_with_clear(self, locator, text):
        element = self.find_element(locator)
        element.clear()
        element.press_sequentially(text)
        print(f'===> Entered "{text}" with clear in "{locator}" field')

    def navigate_to_url(self, url):
        self.context.page.goto(url)

    def scroll_slowly_until_element_in_viewport(self, locator, max_retries=100, wait_time=0.5):
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

