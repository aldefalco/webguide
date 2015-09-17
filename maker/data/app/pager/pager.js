(function() {

	var pager = angular.module('wgmPager', [ ]);
	
     
    
    
	pager.controller('Pager', ['$scope',  function($scope,  WebGuide) {
		  
        $scope.screenshot = Maker.screenshot;
        $scope.pages = [];
        $scope.save = function(){
            
            /*
            
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
            */
            
            Maker.save($scope.pages);
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