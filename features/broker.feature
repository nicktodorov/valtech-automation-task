Feature: Verify broker search and details

  @all_brokers
  # This scenario gets all possible brokers and searches for each of them
  # It takes more than 10 minutes in headless mode!
  Scenario: Search for all brokers and verify search results
    Given user is on the "brokers" page
    When user retrieve all broker names
    Then user search for each broker and verify their details


  @first_displayed_brokers
  # This scenario gets only the first 16 displayed brokers and searches only for them for faster execution
  # It takes 1-2 minutes in headless mode
  Scenario: Search for first displayed brokers only and verify search results
    Given user is on the "brokers" page
    When user retrieve first visible broker names
    Then user search for each broker and verify their details


  @api_broker_data_as_table
    # This scenario uses API request to get all brokers and extract
      # required data (from field table) for each of them in a table
  Scenario: Get all brokers data from API in a table
    Given user retrieve broker data from Yavlena API for "Sofia"
    When user make API requests for all brokers
    Then user extract the following data for each broker and print it as table:
      | Field                |
      | name                 |
      | cityLocalized        |
      | officePhone          |
      | phoneNumber          |
      | offersCountLocalized |


  @api_broker_data_as_plain_text
    # This scenario uses API request to get all brokers and extract
      # required data (from field table) for each of them in plain text
  Scenario: Get all brokers data from API as plain text
    Given user retrieve broker data from Yavlena API for "Sofia"
    When user make API requests for all brokers
    Then user extract the following data for each broker and print it as plain text:
      | Field                |
      | name                 |
      | cityLocalized        |
      | officePhone          |
      | phoneNumber          |
      | offersCountLocalized |
