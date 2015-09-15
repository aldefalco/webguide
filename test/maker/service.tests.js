

'use strict';

describe('Check if the REST web service api works', function () {
    var Guide, httpBackend;

    //mock Application to allow us to inject our own dependencies
    beforeEach(module('WebGuide.Service'));

    beforeEach(inject(['WebGuide', '$httpBackend',
        function (guide, $httpBackend) {
            Guide = guide;
            httpBackend = $httpBackend;
    }]));

    // tests start here
    it('Create a new guide', function (done) {

        httpBackend.whenPOST("/guide").respond({
            "description": "d1",
            "id": 100,
            "title": "t1"
        });

        httpBackend.whenGET("/guide/100/page").respond([]);

        httpBackend.whenPOST("/guide/100/page").respond({
            "id": 1001,
            "image": "1001.png"
        });
        
        Guide.saveGuide({ title: 'foo', pages: [{comment:""}, {comment:""}] }).then(function(){
            done();
        });
        
        httpBackend.flush();
    });

});