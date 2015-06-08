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
            getDecoded($scope.url).success(function(data) {
                window.location = data.url;
            });
        };

        function getDecoded(url) {
            return $http.post('/follow', {'url': url});
        }
    }]);
})(angular);
