Web serivce code example
========================

This is my 24 hours coding challenge to implement a web service that helps to make and show "how-to" user's guides. In this example I tried to show my practice how to implement such things and what we need to do for.

It has following modules:
 * Maker is a Firefox extension that assists user for guide creating. It has been implemented on JavaScript and AngularJS.
 * Server is a flask application that provides following capabilities: REST API for JavaScript and website frontend.
 * Sync is a module for worker processes for Redis cache invalidation and Elasticsearch indexes updating. It exploits PostgreSQL notification functionality.

For database I use the PostgreSQL 9.4,  the Redis as a cache backend and the Elasticsearch for full text search.

For REST API testing I intend to use the BDD Cucumber specifications and the 'Behave' test framework. For other python's modules the doctests and the unittest libs. For JavaScript I use the Jasmin and the Karma environments.
