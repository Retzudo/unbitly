(function(angular) {
    app = angular.module('BitlyApp', []);

    app.controller('BitlyController', ['$scope', '$http', function($scope, $http) {
        $scope.url = '';
        $scope.decodedUrl = '';
        $scope.loading = false;

        $scope.decode = function() {
            $scope.loading = true;
            getDecoded($scope.url).success(function(data) {
                $scope.decodedUrl = data.url;
            }).finally(function() {
                $scope.loading = false;
            });
        };

        $scope.open = function() {
            $scope.loading = true;
            getDecoded($scope.url).success(function(data) {
                window.location = data.url;
            });
        };

        function getDecoded(url) {
            return $http.post('/follow', {'url': url});
        }
    }]);

    app.directive('ngEnter', function () {
        return function (scope, element, attrs) {
            element.bind("keydown keypress", function (event) {
                if(event.which === 13) {
                    scope.$apply(function (){
                        scope.$eval(attrs.ngEnter);
                    });
                    event.preventDefault();
                }
            });
        };
    });
})(angular);
