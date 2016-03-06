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

        $scope.source = angular.element('#source-value');
        $scope.externalId = angular.element('#external-id-value');
        $scope.height = angular.element('#height-value');
        $scope.width = angular.element('#width-value');
    }
};