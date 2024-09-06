document.addEventListener("DOMContentLoaded", function (){

    /*----------------------------------------- header -----------------------------------------*/

    window.addEventListener('scroll', function(){
        const header = document.querySelector('header');

        if (window.scrollY > 0) header.classList.add('scrolled');
        else header.classList.remove('scrolled');
    });
    
    /*----------------------------------------- log -----------------------------------------*/

    document.getElementById("log-icon").addEventListener("click", function () {
        document.getElementById("log-panel").classList.toggle("log-open");
    });

    document.getElementById("log-close").addEventListener("click", function () {
        document.getElementById("log-panel").classList.remove("log-open");
    });

    /*----------------------------------------- sign -----------------------------------------*/

    document.getElementById("sign-in").addEventListener("click", function () {
        document.getElementById("log-panel").classList.remove("log-open");
        document.getElementById("sign-panel").classList.toggle("sign-open");
    });

    document.getElementById("sign-close").addEventListener("click", function () {
        document.getElementById("sign-panel").classList.remove("sign-open");
    });

    /*----------------------------------------- reset email -----------------------------------------*/

    document.getElementById("reset").addEventListener("click", function () {
        document.getElementById("log-panel").classList.remove("log-open");
        document.getElementById("sign-panel").classList.remove("sign-open");
        document.getElementById("reset-panel").classList.toggle("reset-open");
    });

    document.getElementById("reset-close").addEventListener("click", function () {
        document.getElementById("reset-panel").classList.remove("reset-open");
    });

    /*----------------------------------------- reset link -----------------------------------------*/

    document.getElementById("reset-link").addEventListener("click", function () {
        document.getElementById("log-panel").classList.remove("log-open");
        document.getElementById("sign-panel").classList.remove("sign-open");
        document.getElementById("reset-panel").classList.remove("reset-open");
        document.getElementById("reset-link-panel").classList.toggle("reset-link-open");
    });

    document.getElementById("reset-link-close").addEventListener("click", function () {
        document.getElementById("reset-link-panel").classList.remove("reset-link-open");
    });
});