/**
 * Created by alex on 13.09.2015.
 */

(function () {
    "use strict";

    var mod = angular.module('WebGuide.Search', ['restangular']);
    mod.factory('Search', ['$q', '$http', 'Restangular',
        function ($q, $http, Restangular) {

            var _search = Restangular.all('search'),
                _autocomplete = Restangular.all('search/autocomplete');

            return {

                autocomplete: function (prefix) {

                    var deferred = $q.defer();

                    _autocomplete.post({prefix:prefix}).then(
                        function (data) {

                            var titles = _.map(data.hits.hits, function(hit){
                                return hit._source.title;
                            });

                            deferred.resolve(titles);

                        }, deferred.reject
                    );
                    return deferred.promise;
                },

                search: function (query) {

                    var deferred = $q.defer();

                    _search.post({query:query}).then(
                        function (data) {

                            var guides = _.map(data.hits.hits, function(hit){
                                hit._source.href = '/guide/' + hit._source.id;
                                return hit._source;
                            });

                            deferred.resolve(guides);

                        }, deferred.reject
                    );
                    return deferred.promise;
                }

            };
    }]);
})();