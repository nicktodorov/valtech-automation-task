# valtech-automation-task

This repository contains a test automation framework built using Python, Playwright, Behave and the requests library for API tests. This document will guide you through the setup process and provide instructions on how to execute the tests.

## Prerequisites

Before starting, ensure you have the following installed on your machine:

**1.	Python (version 3.12 or later)**

**2. An IDE such as PyCharm (recommended)**

## Setup Instructions

**1. Clone the Repository**

**2. Create and Activate a Virtual Environment**

 ```bash
 python -m venv venv
 source venv/bin/activate      # For Linux/macOS
 venv\Scripts\activate         # For Windows
```
   
**3. Install Dependencies**

```bash
pip install -r requirements.txt
```
**4. Install Playwright Browsers**

```bash
   playwright install
   ```
## Running the Tests

By default, the framework is configured to run UI tests. To specify which type of tests to execute (UI or API), you can use the behave command with the appropriate parameter.

**1. To run the UI tests (the default mode), simply execute the following command:**
 ```bash
behave --tags @XXX --no-capture -D headless=True
```
Where @XXX can be:
- `@first_displayed_brokers`
- `@all_brokers`

This will execute the UI tests using the default settings in the behave.userdata configuration file, where ui_run = true and will run just a single scenario that has the specified tag.

#### Additional Parameters
You can also use the `headless=False` parameter to run the tests with opening a browser window.

<br>

**2. To run API tests instead of UI tests, you need to set the ui_run parameter to false.** 
This can be done by passing the -D parameter to the behave command:
```bash
behave --tags @XXX --no-capture -D headless=True -D ui_run=false
```
Where @XXX can be:
- `@api_broker_data_as_table`
- `@api_broker_data_as_plain_text`