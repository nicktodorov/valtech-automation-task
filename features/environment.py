import datetime
import os
from playwright.sync_api import sync_playwright

import common_variables

SCREENSHOTS_DIR = os.path.join(os.getcwd(), "screenshots")


def before_all(context):
    print(f'!!! {context.config.userdata['ui_run']}')
    common_variables.ui_run = context.config.userdata.get("ui_run", "true").lower() == "true"
    if common_variables.ui_run:
        print(f"Starting UI run...")
        context.playwright = sync_playwright().start()
        headless_str = context.config.userdata.get("headless")
        headless = headless_str.lower() == "true"
        context.browser = context.playwright.chromium.launch(headless=headless, slow_mo=200)
    else:
        print(f"Starting API run...")


def before_feature(context, feature):
    print(f"Executing feature: '{context.feature.name}'")


def before_scenario(context, scenario):
    if common_variables.ui_run:
        context.context = context.browser.new_context(
            viewport={'width': 1280, 'height': 720},
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            record_video_dir=f"screenshots/videos/{context.scenario.name}",
            record_video_size={"width": 640, "height": 480}
        )
        context.page = context.context.new_page()


def before_step(context, step):
    context.step = step
    print(f"Executing step: {context.step.name}")


def after_step(context, step):
    if step.status == "failed":
        print(f"Failed step: {context.step.name}")
        print("Taking screenshots")
        if common_variables.ui_run:
            if not os.path.exists(SCREENSHOTS_DIR):
                os.makedirs(SCREENSHOTS_DIR)
            current_time = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
            scenario_name = context.scenario.name.replace(" ", "_")
            screenshot_filename = f"{scenario_name}_{current_time}.png"
            screenshot_path = os.path.join(SCREENSHOTS_DIR, screenshot_filename)
            context.page.screenshot(path=screenshot_path)
            print(f"Screenshot saved: {screenshot_path}")
    else:
        print(f"Completed step: {context.step.name}")


def after_scenario(context, scenario):
    if common_variables.ui_run:
        video_dir = f"screenshots/videos/{context.scenario.name}"
        context.page.close()
        context.context.close()
    if scenario.status == "failed":
        print(f"Failed scenario: '{context.scenario.name}'")
    else:
        print(f"Completed scenario: '{context.scenario.name}'")


def after_feature(context, feature):
    if feature.status == "failed":
        print(f"Failed feature: '{context.feature.name}'")
    else:
        print(f"Completed feature: '{context.feature.name}'")


def after_all(context):
    print("Run completed")
    if common_variables.ui_run:
        context.browser.close()
        context.playwright.stop()
