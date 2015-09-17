(function () {

    var pager = angular.module('wgmPager', []);

    pager.controller('Pager', ['$scope',
        function ($scope, WebGuide) {

            $scope.screenshot = Maker.screenshot;
            $scope.pages = [];
            $scope.save = function () {
                Maker.save($scope.pages);
            };

            Maker.onAppendPage(function (page) {
                $scope.$apply(function () {
                    console.log('append a page');
                    $scope.pages.push(page);
                });
            });
    }]);

})();