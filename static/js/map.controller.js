"use strict";
angular.module('mapApp', []).config(function($interpolateProvider) {
    $interpolateProvider.startSymbol('{[{');
    $interpolateProvider.endSymbol('}]}');
}).controller('mapCtrl', mapController);

function mapController($scope) {
    $scope.rotate = rotate;
    $scope.move = move;
    $scope.clear = clear;

    $scope.rot = {
        UP: 270,
        RIGHTUP: 330,
        RIGHTDOWN: 30,
        DOWN: 90,
        LEFTUP: 210,
        LEFTDOWN: 150
    };

    $scope.coordinates = coord(1,-1);
    $scope.rotation = $scope.rot.LEFTDOWN;

    activate();

    function activate() {
        $scope.canvas = angular.element('#map_area').get(0);  // Get the regular js element
        $scope.gameMap = new GameMap($scope.canvas, 500, 330, 50.0, 3, coord(1000,700));
        $scope.gameMap.drawGrid();
        $scope.gameMap.drawTank(1, 1, $scope.rot.RIGHTDOWN);
        $scope.gameMap.drawTank(0, -2, $scope.rot.UP);
    }

    function rotate() {
        console.log('asdf');
    }
    
    function move() {
        console.log('asdf');
    }

    function clear() {
        $scope.gameMap.clear();
        $scope.gameMap.drawGrid();
    }

    function coord(x,y) {
        return {x:x,y:y};
    }
};