"use strict";
// GameMap class
function GameMap(canvas, origin, hexRadius, gridOffset, gridRadius, size) {
    this.gridRadius = gridRadius;
    this.origin = origin;
    this.radius = hexRadius;
    this.size = size;  // x,y size of the drawing area
    this.offset = gridOffset;
    this.ctx = canvas.getContext('2d');
}

GameMap.prototype.drawGrid = function() {
    for (var i = -1*this.gridRadius - this.offset.row; i <= this.gridRadius - this.offset.row; i++) {
        for (var j = -1*this.gridRadius - this.offset.col; j <= this.gridRadius - this.offset.col; j++) {
            if (Math.abs(i-j) <= this.gridRadius){
                var pos = this.translate(i, j);
                this.drawHex(pos, this.radius, '#000');

                // debug text
                this.ctx.font = '14px Arial';
                this.ctx.fillText(i + ',' + j, pos.x - 10, pos.y - 30);
            }
        }
    }
};

GameMap.prototype.drawHex = function(pos, radius, color) {
    var sin60 = Math.sin(Math.PI/3.0);
    var cos60 = Math.cos(Math.PI/3.0);

    this.ctx.strokeStyle = "#000";
    this.ctx.beginPath();
    this.ctx.moveTo(pos.x + radius, pos.y);
    this.ctx.lineTo(pos.x + radius*cos60, pos.y - radius*sin60);
    this.ctx.lineTo(pos.x - radius*cos60, pos.y - radius*sin60);
    this.ctx.lineTo(pos.x - radius, pos.y);
    this.ctx.lineTo(pos.x - radius*cos60, pos.y + radius*sin60);
    this.ctx.lineTo(pos.x + radius*cos60, pos.y + radius*sin60);
    this.ctx.lineTo(pos.x + radius, pos.y);

    //this.ctx.fillStyle = color || '#FFF';
    //this.ctx.fill();

    this.ctx.closePath();
    this.ctx.stroke();
};

GameMap.prototype.drawTank = function(row, col, rotation) {
    var pos = this.translate(row, col);
    this.ctx.save();
    this.ctx.translate(pos.x,pos.y);
    this.ctx.rotate(rotation * Math.PI/180);
    this.ctx.fillRect(-25,-20,50,40);
    this.ctx.fillRect(0,-2,35,4);

    this.ctx.restore();
};

GameMap.prototype.translate = function(row, col) {
    var newRow = this.offset.row + row;
    var newCol = this.offset.col + col;
    var offsetX = this.radius * (newRow * -1.5 + newCol * 1.5);
    var offsetY = this.radius * -1 * Math.sin(Math.PI/3.0) * (newRow + newCol);

    return {
        x: this.origin.x + offsetX,
        y: this.origin.y + offsetY
    };
};

GameMap.prototype.clear = function() {
    this.ctx.clearRect(0, 0, this.size.x, this.size.y);
};