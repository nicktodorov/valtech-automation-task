# valtech-automation-task

This repository contains a test automation framework built using Python, Playwright, and Behave. This document will guide you through the setup process and provide instructions on how to execute the tests.

## Prerequisites

Before starting, ensure you have the following installed on your machine:
1.	Python (version 3.8 or later)
2An IDE such as PyCharm (recommended)

## Setup Instructions
1. Clone the Repository
2. Create and Activate a Virtual Environment
    ```bash
    python -m venv venv
    source venv/bin/activate      # For Linux/macOS
    venv\Scripts\activate         # For Windows
3. Install Dependencies
    ```bash
   pip install -r requirements.txt
4. Install Playwright Browsers
    ```bash
   playwright install

## Running the Tests

1. Using the behave Command in terminal:
    ```bash
   behave --tags @XXX --no-capture -D headless=True
Where @XXX can be:
- @first_displayed_brokers
- @all_brokers