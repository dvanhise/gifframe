"use strict";
angular.module('frameApp', []).config(function($interpolateProvider) {
    $interpolateProvider.startSymbol('{[{');
    $interpolateProvider.endSymbol('}]}');
}).controller('frameCtrl', frameController);

function frameController($scope, $location) {
    $scope.frames = [];
    console.log($location.$$path);
    $scope.currentFrame = $location.$$path ? parseInt($location.$$path.replace(/[^0-9]/, '')) - 1 : 0;

    activate();

    function activate() {
        var elem, counter = 0;
        while (true) {
            elem = angular.element('#frame' + counter);
            if (!elem.length || counter >= 200) { break; }

            $scope.frames.push(elem[0].value);
            console.log(elem[0].value);
            counter++;
        }

        if ($scope.currentFrame < 0) {
            $scope.currentFrame = 0
        } else if ($scope.currentFrame >= $scope.frames.length) {
            $scope.currentFrame = $scope.frames.length - 1;
        }

        $scope.source = angular.element('#source-value')[0].value;
        $scope.imageRoot = angular.element('#image-root-value')[0].value;
        $scope.externalId = angular.element('#external-id-value')[0].value;
        $scope.height = angular.element('#height-value')[0].value;
        $scope.width = angular.element('#width-value')[0].value;
    }
};