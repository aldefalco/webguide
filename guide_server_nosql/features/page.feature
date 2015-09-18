Feature: Page
  As an API client
  I want to be able to get pages of a guide, add a new page and remove any or all pages

  Background: Set server URL and reset database
    Given I am using server "http://localhost:5000/v1"
    And I set Accept header to "application/json"
    When I send a DELETE request to "guide"
    Then the response status should be "204"
    When I send a POST request to "guide"
    """
      { "title": "title1", "description": "description1" }
      """
    Then the response status should be "201"
    And the JSON at path "id" should be 1

  Scenario: Add a new guide and a few pages
    Given I set Content-Type header to "application/json"
    When I send a POST request to "guide/1/page"
    """
      {"comment": "comment1", "region":"{1}",
      "src": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAoAAAADCAYAAACqPZ51AAAAEklEQVQImWMQ6330nxjMQHWFAPTeS3n1L96wAAAAAElFTkSuQmCC" }
      """
    Then the response status should be "201"
    When I send a POST request to "guide/1/page"
    """
      {"comment": "comment1", "region":"{1}",
      "src": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAoAAAADCAYAAACqPZ51AAAAEklEQVQImWMQ6330nxjMQHWFAPTeS3n1L96wAAAAAElFTkSuQmCC" }
      """
    Then the response status should be "201"
    When I send a GET request to "guide/1/page"
    Then the response status should be "200"
    And the JSON at path "[0].id" should be 1
    And the JSON at path "[1].id" should be 2


  Scenario: Add a new guide and a few pages and delete one
    Given I set Content-Type header to "application/json"
    When I send a POST request to "guide/1/page"
    """
      {"comment": "comment1", "region":"{1}",
      "src": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAoAAAADCAYAAACqPZ51AAAAEklEQVQImWMQ6330nxjMQHWFAPTeS3n1L96wAAAAAElFTkSuQmCC" }
      """
    Then the response status should be "201"
    When I send a POST request to "guide/1/page"
    """
      {"comment": "comment1", "region":"{1}",
      "src": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAoAAAADCAYAAACqPZ51AAAAEklEQVQImWMQ6330nxjMQHWFAPTeS3n1L96wAAAAAElFTkSuQmCC" }
      """
    Then the response status should be "201"
    When I send a DELETE request to "guide/1/page/1"
    Then the response status should be "204"
    When I send a GET request to "guide/1/page"
    Then the response status should be "200"
    And the JSON at path "[0].id" should be 2

  Scenario: Add a new guide and a new page and modify one
    Given I set Content-Type header to "application/json"
    When I send a POST request to "guide/1/page"
    """
      {"comment": "comment1", "region":"{1}",
      "src": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAoAAAADCAYAAACqPZ51AAAAEklEQVQImWMQ6330nxjMQHWFAPTeS3n1L96wAAAAAElFTkSuQmCC" }
      """
    Then the response status should be "201"
    When I send a PUT request to "guide/1/page/1"
    """
      {"comment": "comment2", "region":"{2}" }
      """
    Then the response status should be "201"
    And the JSON at path "id" should be 1
    And the JSON at path "comment" should be "comment2"
