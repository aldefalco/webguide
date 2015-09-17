(function () {

    var save = angular.module('wgmSave', ['WebGuide.Service']);


    save.config([
            '$compileProvider', 'RestangularProvider',
            function ($compileProvider, RestangularProvider) {
            RestangularProvider.setBaseUrl('http://localhost:5000/v1');
            //$compileProvider.aHrefSanitizationWhitelist(/^\s*(https?|ftp|mailto|chrome-extension):/);
            // Angular before v1.2 uses $compileProvider.urlSanitizationWhitelist(...)
            }
        ]);


    save.controller('Save', ['$scope', 'WebGuide',
        function ($scope, WebGuide) {

            $scope.guide = {
                title: '',
                description: '',
                pages: []
            };

            $scope.save = function () {

                WebGuide.saveGuide($scope.guide).then(
                    function () {
                        console.log('Save guide is success');
                        Maker.complete();
                    },
                    function () {
                        console.log('Save guide is failed');
                    }
                );
            };

            Maker.onOpenSave(function (pages) {

                $scope.$apply(function () {
                    //console.log('append a page');

                    $scope.guide.pages = _.map(pages, function (page, i) {
                        return {
                            src: page.image.cropped,
                            comment: page.comments,
                            region: JSON.stringify(page.image.region),
                            order: i
                        };
                    });
                });
            });
  }]);

})();