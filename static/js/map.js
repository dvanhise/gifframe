
$( document ).ready(function() {
    var rot = {
        UP: 270,
        RIGHTUP: 330,
        RIGHTDOWN: 30,
        DOWN: 90,
        LEFTUP: 210,
        LEFTDOWN: 150
    };

    function coord(x,y) {
        return {x:x,y:y};
    }

    function rowcol(row, col) {
        return {row:row,col:col};
    }

    _.forEach(tanks, function(tank) {
        gameMap.drawTank(tank.col, tank.row, tank.rotation);
    });
});



function Tank() {
    this.position = {row: 1, col: -1};
    this.rotation = 0;
}

Tank.prototype.moveFoward = function() {

};

Tank.prototype.moveBackward = function() {

};
