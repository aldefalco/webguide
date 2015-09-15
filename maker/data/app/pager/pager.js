(function() {

	var pager = angular.module('wgmPager', [ 'WebGuide.Service' ]);
	
     
    pager.config([
            '$compileProvider', 'RestangularProvider',
            function ($compileProvider, RestangularProvider) {
                RestangularProvider.setBaseUrl('http://localhost:5000/v1');
                //$compileProvider.aHrefSanitizationWhitelist(/^\s*(https?|ftp|mailto|chrome-extension):/);
                // Angular before v1.2 uses $compileProvider.urlSanitizationWhitelist(...)
            }
        ]);

    
	pager.controller('Pager', ['$scope',  'WebGuide', function($scope,  WebGuide) {
		  
        $scope.screenshot = Maker.screenshot;
        $scope.pages = [];
        $scope.save = function(){
            
            //TODO: fix it
            var pages = _.map($scope.pages, function(page, i){
                return { 
                    src:  page.image.cropped,
                    comment: page.comments,
                    region: JSON.stringify(page.image.region),
                    order: i
                };
            });
            
            var guide = {
                title: 'Test how-to guide',
                description: 'Hello world',
                pages: pages
            };
            
            WebGuide.saveGuide(guide).then(
                function(){
                    console.log('Save guide is success');
                },
                function(){
                    console.log('Save guide is failed');
                }
            );
        };
        
          Maker.onAppendPage(function(page){
              $scope.$apply(function () {
                    console.log('append a page');
                    $scope.pages.push(page);
                    //console.log(data);
                });
          });
		}]);

	
})();