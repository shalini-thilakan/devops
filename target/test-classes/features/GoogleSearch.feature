Feature: Google Search Functionality

  Scenario: Search for a valid keyword on Google
    Given the user is on the Google homepage
    When the user searches for "OpenAI"
    Then search results should contain "OpenAI"

  Scenario: Search for a random string that has no results
    Given the user is on the Google homepage
    When the user searches for "asdlkfjasdflkjasdf"
    Then no search results should be displayed
