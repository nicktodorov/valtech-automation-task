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