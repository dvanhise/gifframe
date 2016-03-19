"use strict";
angular.module('frameApp', []).config(function($interpolateProvider) {
    $interpolateProvider.startSymbol('{[{');
    $interpolateProvider.endSymbol('}]}');
}).controller('frameCtrl', frameController);

function frameController($scope) {
    $scope.frames = [];
    $scope.currentFrame = 0;

    activate();

    function activate() {
        var elem, counter = 0;
        while (true) {
            elem = angular.element('#frame' + counter);
            if (!elem.length || counter >= 200) { break; }

            $scope.frames.push(elem[0].value);
            counter++;
        }

        $scope.source = angular.element('#source-value')[0].value;
        $scope.imageRoot = angular.element('#image-root-value')[0].value;
        console.log($scope.imageRoot);
        $scope.externalId = angular.element('#external-id-value')[0].value;
        console.log($scope.externalId);
        $scope.height = angular.element('#height-value')[0].value;
        $scope.width = angular.element('#width-value')[0].value;
    }
};