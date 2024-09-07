document.addEventListener("DOMContentLoaded", function (){

    /*----------------------------------------- header -----------------------------------------*/

    window.addEventListener('scroll', function(){
        const header = document.querySelector('header');

        if (window.scrollY > 0) header.classList.add('scrolled');
        else header.classList.remove('scrolled');
    });
    
    /*----------------------------------------- search -----------------------------------------*/

    document.querySelector('#search-icon').addEventListener('click', function () {
        document.querySelector('#search-panel').style.display = 'block';
    
        const categories = [
            { image: '/static/images/prod-1.JPG', name: 'Drop Shoulder' },
            { image: '/static/images/prod-2.JPG', name: 'Baggy Joggers' },
            { image: '/static/images/prod-3.JPG', name: 'Baggy Shirts' },
            { image: '/static/images/prod-4.JPG', name: 'Cargo Pants' },
            { image: '/static/images/prod-5.JPG', name: 'Head Wear' },
            { image: '/static/images/prod-6.JPG', name: 'Baggy Shorts' }
        ];
    
        const searchContent = document.querySelector('.search-content');
    
        for (let i = 0; i < categories.length; i++) {
            const category = categories[i];
            const categoryDiv = document.createElement('div');
            categoryDiv.classList.add('search-category');
        
            categoryDiv.innerHTML = `
                <div class="search-category">
                    <img src="${category.image}" width="200" height="250">
                    <h2>${category.name}</h2>
                </div>`;
        
            searchContent.appendChild(categoryDiv);
        }
    });
    
    document.querySelector('#search-close').addEventListener('click', function () {
        document.querySelector('#search-panel').style.display = 'none';
        document.querySelector('.search-content').innerHTML = '';
    });

    window.onclick = function (event) {
        if (event.target == document.querySelector('#search-panel')) {
            document.querySelector('#search-panel').style.display = 'none';
        }
    };

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