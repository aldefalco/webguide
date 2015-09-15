Web serivce code example
========================


This is my 24 hours coding challenge to implement a web service that helps to make and show "how-to" user's guides. In this example I tried to show my practice how to implement such things and what we need to do for.

It has following modules: 
 * Maker is a Firefox extension that assists user for guide creating. It has been implemented on JavaScript and AngularJS. 
 * Server is a flask application that provides following capabilities: REST API for JavaScript frontends and website pages. 
 * CacheSync is a worker process for the Redis cache invalidation. It exploits PostgreSQL notification functionality.

For database I use the PostgreSQL 9.4 and Redis as a cache backend.