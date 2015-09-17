

'use strict';

describe('Check if the REST search service api works', function () {
    var Search, httpBackend;

    beforeEach(module('WebGuide.Search'));

    beforeEach(inject(['Search', '$httpBackend',
        function (s, $httpBackend) {
            Search = s;
            httpBackend = $httpBackend;
    }]));

    it('Simple search', function (done) {

        httpBackend.whenPOST("/search").respond({
            "hits": {
                "total": 3,
                "hits": [
                    {
                        "_source": {
                            "description": "no way",
                            "title": "second complex",
                            "id": 4,
                            "query_class": null,
                            "query": null,
                            "pages": null
                        }
                 },
                    {
                        "_source": {
                            "description": "second description bullet",
                            "title": "second simple window",
                            "id": 3,
                            "query_class": null,
                            "query": null,
                            "pages": null
                        }
                 }
              ]
            }
        });

        Search.search({ query: 'second' }).then(function(guides){
            expect(guides[0].title).toBe("second complex");
            expect(guides[1].title).toBe("second simple window");
            expect(guides[0].href).toBe("/guide/4");
            done();
        });
        
        httpBackend.flush();
    });
    
     it('Autocomplete search', function (done) {

        httpBackend.whenPOST("/search/autocomplete").respond({
            "hits": {
                "total": 3,
                "hits": [
                    {
                        "_source": {
                            "description": "no way",
                            "title": "second complex",
                            "id": 4,
                            "query_class": null,
                            "query": null,
                            "pages": null
                        }
                 },
                    {
                        "_source": {
                            "description": "second description bullet",
                            "title": "second simple window",
                            "id": 3,
                            "query_class": null,
                            "query": null,
                            "pages": null
                        }
                 }
              ]
            }
        });

        Search.autocomplete({ prefix: 'second' }).then(function(titles){
            expect(titles[0]).toBe("second complex");
            expect(titles[1]).toBe("second simple window");
            done();
        });
        
        httpBackend.flush();
    });

});