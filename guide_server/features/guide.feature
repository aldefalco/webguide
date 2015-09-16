Feature: Guide 
  As an API client
  I want to be able to get guide list, add a new guide and remove all guides

  Background: Set server URL and reset database
    Given I am using server "http://localhost:5000/v1"
    And I set Accept header to "application/json"
    When I send a DELETE request to "guide"
    Then the response status should be "204"

  Scenario: Add a new guide, declare json, but don't send anything
    Given I set Content-Type header to "application/json"
    When I send a POST request to "guide"
    Then the response status should be "400"

  Scenario: Add a new guide, declare json, but send invalid json
    Given I set Content-Type header to "application/json"
    When I send a POST request to "guide"
      """
      {"title": "forgot the end quote}
      """
    Then the response status should be "400"

  Scenario: Add a new guide
    Given I set Content-Type header to "application/json"
    When I send a POST request to "guide"
      """ 
      { "title": "title1", "description": "description1" } 
      """
    Then the response status should be "201"
    And the JSON at path "title" should be "title1"

  Scenario: Add a few guides and get a list
    Given I set Content-Type header to "application/json"
    When I send a POST request to "guide"
      """ 
      { "title": "title1", "description": "description1" } 
      """
    Then the response status should be "201"
    When I send a POST request to "guide"
      """ 
      { "title": "title2", "description": "description2" } 
      """
    Then the response status should be "201"
    When I send a GET request to "guide"
    Then the response status should be "200"
    And the JSON at path "[0].title" should be "title1"
    And the JSON at path "[1].title" should be "title2"

  Scenario: Add a guide and get by id
    Given I set Content-Type header to "application/json"
    When I send a POST request to "guide"
      """ 
      { "title": "title1", "description": "description1" } 
      """
    Then the response status should be "201"
    When I send a GET request to "guide/1"
    Then the response status should be "200"
    And the JSON at path "title" should be "title1"

  Scenario: Add a few guides, remove one and get a list
    Given I set Content-Type header to "application/json"
    When I send a POST request to "guide"
      """ 
      { "title": "title1", "description": "description1" } 
      """
    Then the response status should be "201"
    When I send a POST request to "guide"
      """ 
      { "title": "title2", "description": "description2" } 
      """
    Then the response status should be "201"
    When I send a DELETE request to "guide/1"
    Then the response status should be "204"
    When I send a GET request to "guide"
    Then the response status should be "200"
    And the JSON at path "[0].title" should be "title2"

