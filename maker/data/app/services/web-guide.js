(function () {
    "use strict";
    
    var mod = angular.module('WebGuide.Service', ['restangular']);
    mod.factory('WebGuide', ['$q', '$http', 'Restangular',
        function ($q, $http, Restangular) {

            var guides = Restangular.all('guide');

            return {

                saveGuide: function (guide) {

                    var deferred = $q.defer(),
                        newPages = guide.pages;

                    delete guide.pages;

                    guides.post(guide).then(function (guide) {
                        guide.getList('page').then(function (pages) {

                            function post(page, pageDef, count) {
                                pages.post(page,
                                    function () {
                                        pageDef.resolve();
                                    }, function () {
                                        if (--count > 0) {
                                            post(page, pageDef, count - 1);
                                        } else {
                                            pageDef.reject();
                                        }
                                    }
                                );
                            }

                            var deferres = _.map(newPages, function (page) {
                                var d = $q.defer();
                                post(page, d, 3);
                                return d;
                            });
                            
                            $q.all(deferres).then(
                                function(){ deferred.resolve(); },
                                function(){ deferred.reject();}
                            );

                        }, function(){ deferred.reject();});

                    }, function(){ deferred.reject();});

                    return deferred.promise;
                }
            };
    }]);
})();