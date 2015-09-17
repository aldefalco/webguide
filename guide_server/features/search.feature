Feature: Search
  As an API client
  I want to be able to get search functions

  Background: Set server URL and reset database
    Given I am using server "http://localhost:5000/v1"
    And I set Accept header to "application/json"
    And I set Content-Type header to "application/json"
    When I send a DELETE request to "guide"
    Then the response status should be "204"
    When I send a POST request to "guide"
    """
      { "title": "new progress window", "description": "simple first description bullet" }
      """
    Then the response status should be "201"
    When I send a POST request to "guide"
    """
      { "title": "second simple window", "description": "second description bullet" }
      """
    Then the response status should be "201"
    When I send a POST request to "guide"
    """
      { "title": "second complex", "description": "no way" }
      """
    Then the response status should be "201"

  @dev
  Scenario: Autocomplete with one entry
    Given I set Content-Type header to "application/json"
    When I send a POST request to "search/autocomplete/title"
    """
      { "title":"new" }
    """
    Then the response status should be "200"
    And the JSON at path "hits.total" should be 1
    And the JSON at path "hits.hits[0]._source.title" should be "new progress window"


