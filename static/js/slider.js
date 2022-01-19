
var slider = document.getElementById("volume");
var slider2 = document.getElementById("volume1");
var slider3 = document.getElementById("range-1b");
var output = document.getElementById("slider_value1");
var output2 = document.getElementById("slider_value2");
output.innerHTML = slider.value;

slider.oninput = function () {
    output.innerHTML = this.value;
}
slider2.oninput = function () {
    output2.innerHTML = slider2.value;
}
slider3.oninput = function () {
    output.innerHTML = this.value;
}