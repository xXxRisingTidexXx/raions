let dots = [];
let count = 50;
let radius = 100;

let canvas;
let context;

let drawing;

window.onload = function() {
  canvas = document.getElementById("canvas");
  context = canvas.getContext("2d");
  start();
  drawing = setInterval(draw, 20);
};

window.onresize = function() {
  clearInterval(drawing);
  start();
  drawing = setInterval(draw, 20);
};

function start() {
  context.canvas.width = window.innerWidth;
  context.canvas.height = window.innerHeight;
  radius = window.innerWidth * 0.1;
  generateList();
  context.strokeStyle = "orange";
  context.lineWidth = 2;
  context.lineCap = "round";
}

function draw() {
  context.clearRect(0, 0, canvas.width, canvas.height);
  let len = dots.length;
  for (let i = 0; i < len; i++) {
    dots[i].show(i);
    dots[i].phy();
  }
}

function generateList() {
  dots = [];
  for (let i = 0; i < count; i++) {
    let x = Math.random() * canvas.width;
    let y = Math.random() * canvas.height;
    dots[dots.length] = new Dot(x, y);
  }
}

function Dot(x, y) {
  this.x = x;
  this.y = y;
  this.r = Math.random() * Math.PI * 2;

  this.show = function(id) {
    context.beginPath();
    for (let i = id; i < dots.length; i++) {
      let dist = Math.dist(this.x, this.y, dots[i].x, dots[i].y);
      if (dist < radius) {
        context.globalAlpha = Math.map(dist, 0, radius, 1, 0);
        context.beginPath();
        context.moveTo(this.x, this.y);
        context.lineTo(dots[i].x, dots[i].y);
        context.stroke();
      }
    }
    context.stroke();
  };
  this.phy = function() {
    this.x += Math.cos(this.r);
    this.y += Math.sin(this.r);
    this.r += Math.PI / 500;
  }
}

Math.dist = function(x1, y1, x2, y2) {
  if (!x2) x2 = 0;
  if (!y2) y2 = 0;
  return Math.sqrt((x2 - x1) * (x2 - x1) + (y2 - y1) * (y2 - y1));
};

Math.map = function(i, x1, y1, x2, y2) {
  return (i - x1) * (y2 - x2) / (y1 - x1) + x2;
};
