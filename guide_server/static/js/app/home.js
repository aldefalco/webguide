/**
 * Created by alex on 13.09.2015.
 */

(function () {

    var home = angular.module('wgHome', ['WebGuide.Search', 'autocomplete']);

    home.config([
            'RestangularProvider',
            function (RestangularProvider) {
               RestangularProvider.setBaseUrl('http://localhost:5000/v1');
            }
    ]);

    home.controller('wgSearch', ['$scope',  'Search', function($scope,  Search) {
        $scope.query = '';
        $scope.guides = [];
        $scope.titles = [];
        $scope.search = function(){
            Search.search($scope.query).then(function(result){

                $scope.guides = result;
                /*
                $scope.$apply(function(){
                    $scope.result = result;
                });
                */
            });
        };
        $scope.autofill = function(prefix){
            if(prefix && prefix.length>2){
               Search.autocomplete(prefix).then(function(result){
                    $scope.titles = result;
                });
            }
        };

    }]);

})();