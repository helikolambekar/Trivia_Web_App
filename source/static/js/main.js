window.addEventListener("DOMContentLoaded", event => {
    var bg = document.getElementById("bg");
    var box = document.getElementById("box");
    var text = document.getElementById("text");

    // function to let the screen move with the mouse
    document.onmousemove = function (e) {

        /*
        * Initial coordinates of the background image is (300,100), you can adjust it if you need
        * element_name.style.left|top = initial X|Y coordinate (optional) + (e.pageX|Y - main content width|height / 2) / constant (optional) + "px"
        */

        bg.style.left = 100 + (-e.pageX - 960) / 10 + "px";
        bg.style.top = 100 + (-e.pageY - 540) / 10 + "px";

        box.style.left = 500 + (-e.pageX - 480) / 5 + "px";
        box.style.top = 380 + (-e.pageY - 270) / 5 + "px";

        text.style.left = 500 + (-e.pageX - 400) / 5 + "px";
        text.style.top = 300 + (-e.pageY - 200) / 5 + "px";
    }
});