(function () {

    var editor = angular.module('wgmEditor', ['ui.router']);

    editor.config(function ($stateProvider, $urlRouterProvider) {

        $urlRouterProvider.otherwise("crop");

        $stateProvider.state('crop', {
            url: "/crop",
            templateUrl: "partials/crop.html"
        }).state('highlight', {
            url: "/highlight",
            templateUrl: "partials/highlight.html"
        }).state('comments', {
            url: "/comments",
            templateUrl: "partials/comments.html"
        });
    });


    editor.controller('Editor', ['$scope', '$state',
        function ($scope, $state) {
            $scope.save = Maker.savePage;
            
            $scope.image = {
                
                crop: function(image, rect){
                    console.log("crop");
                    console.log(rect);
                    var canvas = document.createElement('canvas'),
                        ctx = canvas.getContext('2d');
                    canvas.width = rect.width;
                    canvas.height = rect.height;
                    ctx.drawImage(image, rect.left, rect.top, rect.width, rect.height, 0, 0, rect.width, rect.height);
                    $scope.$apply(function(){
                         $scope.image.cropped = canvas.toDataURL();
                    });
                },
                
                 highlight: function(image, rect){
                    console.log("highlight");
                    console.log(rect);
                    var canvas = document.createElement('canvas'),
                        ctx = canvas.getContext('2d');
                    canvas.width = rect.width;
                    canvas.height = rect.height;
                    ctx.drawImage(image, rect.left, rect.top, rect.width, rect.height, 0, 0, rect.width, rect.height);
                     
                    $scope.image.region = rect;
                     
                    $scope.$apply(function(){
                         $scope.image.highlighted = canvas.toDataURL();
                    });
                }
                
            };

            Maker.onScreenshot(function (data) {
                $state.go('crop');
                $scope.$apply(function () {
                    console.log('screenshot');
                    $scope.image.data = data;
                    //console.log(data);
                });
            });

  }]);

    editor.directive('jqCropper', function () {
        var directive = {
            restrict: 'C',
            
            link: function (scope, element, attrs, ctrl) {

                var complete,
                    canvas = new fabric.Canvas(element[0]);
                
                canvas.setDimensions({ width:700, height: 400});
                canvas.setCursor("crosshair");
                
                // create a rectangle object
                var rect, isMouseDown = false;
                
                
                var img = new Image(),
                    fImg;
                
                scope.$watch(attrs.imageSrc, function(value) {
                //scope.$watch(scope.imageSrc, function(value) {
                    console.log('image source watch');
                    img.src = value;
                });
                
                scope.$watch(attrs.complete, function(value) {
                    console.log('image source watch');
                    complete = value;
                });
                
                
                img.onload = function () {
                    fImg = new fabric.Image(img);
                    fImg.selectable = false; 
                    fImg.scaleToHeight(400);
                    
                    canvas.add(fImg);
                };
                
                canvas.on('mouse:down', function(options) {
                      
                      if (!rect){
                          rect = new fabric.Rect({
                          left: 0,
                          top: 0,
                          width: 0,
                          height: 0,
                          stroke: "#00F",
                          strokeWidth: 2,
                          fill: 'rgba(255, 85, 85, 0.1)'
                        });

                        canvas.add(rect);
                      }
                    
                      isMouseDown = true;
                      
                      var canBounds =  element[0].getBoundingClientRect();
                      rect.set({ left: options.e.clientX-canBounds.left, top: options.e.clientY-canBounds.top});
                      console.log(rect.top, rect.left);
                                          console.log(options.e);
                  //}
                });
                
                 canvas.on('mouse:move', function(options) {
                     if (isMouseDown) {
                         var canBounds =  element[0].getBoundingClientRect();
                         rect.set({ width: options.e.clientX-rect.left-canBounds.left, height: options.e.clientY-rect.top-canBounds.top});
                         canvas.renderAll();
                     }
                 });
                
                canvas.on('mouse:up', function(options) {
                     isMouseDown = false;
                    console.log(rect.top, rect.left, rect.width, rect.height);
                    var scale = 1/fImg.getScaleY();
                    console.log(scale);
                    complete(img, { left:rect.left*scale, 
                                         top:rect.top*scale,
                                         width: rect.width*scale, 
                                         height: rect.height*scale });
                    
                 });
                
            }
        };
        return directive;
    });

})();