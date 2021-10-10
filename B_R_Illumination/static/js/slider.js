
var slider = document.getElementById("volume");
var output = document.getElementById("slider_value");
output.innerHTML = slider.value;

slider.oninput = function () {
    output.innerHTML = this.value;
}
