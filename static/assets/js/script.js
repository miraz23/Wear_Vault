document.addEventListener("DOMContentLoaded", function (){

    /*----------------------------------------- header -----------------------------------------*/

    window.addEventListener('scroll', function(){
        const header = document.querySelector('header');

        if (window.scrollY > 0) header.classList.add('scrolled');
        else header.classList.remove('scrolled');
    });

    const menuIcon = document.querySelector('.nav-menu-icon');
    const navMenu = document.getElementById('nav-menu');
    const removeMenuButton = document.querySelector('.nav-menu-remove');
  
    menuIcon.addEventListener('click', function() {
      navMenu.classList.toggle('open');
    });
  
    removeMenuButton.addEventListener('click', function() {
      navMenu.classList.remove('open');
    });
      

    /*----------------------------------------- banner -----------------------------------------*/

    const banners = document.querySelectorAll(".banner");
    let currentIndex = 0;
    
    function showNextBanner() {
        banners[currentIndex].classList.remove("active");
        currentIndex = (currentIndex + 1) % banners.length;
        banners[currentIndex].classList.add("active");
    }
    setInterval(showNextBanner, 5000);

    /*----------------------------------------- banner mobile-----------------------------------------*/

    const bannersMobile = document.querySelectorAll(".banner-mobile");
    let currentIndexMobile = 0;
    
    function showNextBannerMobile() {
        bannersMobile[currentIndexMobile].classList.remove("active");
        currentIndexMobile = (currentIndexMobile + 1) % bannersMobile.length;
        bannersMobile[currentIndexMobile].classList.add("active");
    }
    setInterval(showNextBannerMobile, 5000);


    /*----------------------------------------- arrivals -----------------------------------------*/


    document.querySelectorAll('.arrivals-product').forEach((item, index)=>{
        item.addEventListener('mouseenter', () => {
            item.style.transform = 'scale(1.02)';
        });
        item.addEventListener('mouseleave', () => {
            item.style.transform = 'scale(1)';
        });
    });

    const swiper = new Swiper('.arrivals-wrapper', {

        loop: true,
        grabCursor: true,
        spaceBetween: 15,

        navigation: {
          nextEl: '.swiper-button-next',
          prevEl: '.swiper-button-prev',
        },

        breakpoints:{
            0:{
                slidesPerView: 1,
            },
            768:{
                slidesPerView: 2,
            },
            821:{
                slidesPerView: 3,
            },
            1025:{
                slidesPerView: 4,
            },
            1200:{
                slidesPerView: 5,
            },
            1600:{
                slidesPerView: 7,
            },
            2000:{
                slidesPerView: 9,
            }
        }
    });
    
    /*----------------------------------------- search -----------------------------------------*/

    document.getElementById("search-icon").addEventListener("click", function () {
        document.getElementById("search-panel").classList.toggle("search-open");
    });

    document.getElementById("search-menu-icon").addEventListener("click", function () {
        document.getElementById("search-panel").classList.toggle("search-open");
    });
    
    document.getElementById("search-close").addEventListener("click", function () {
        document.getElementById("search-panel").classList.remove("search-open");
    });

    /*----------------------------------------- cart -----------------------------------------*/

    document.getElementById("cart-icon").addEventListener("click", function () {
        document.getElementById("cart-panel").classList.toggle("cart-open");
    });

    document.getElementById("cart-menu-icon").addEventListener("click", function () {
        document.getElementById("cart-panel").classList.toggle("cart-open");
    });

    document.getElementById("cart-close").addEventListener("click", function () {
        navMenu.classList.remove('open');
        document.getElementById("cart-panel").classList.remove("cart-open");
    });

    /*----------------------------------------- log -----------------------------------------*/

    document.getElementById("log-icon").addEventListener("click", function () {
        document.getElementById("log-panel").classList.toggle("log-open");
    });

    document.getElementById("log-menu-icon").addEventListener("click", function () {
        document.getElementById("log-panel").classList.toggle("log-open");
    });

    document.getElementById("log-close").addEventListener("click", function () {
        navMenu.classList.remove('open');
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
        document.getElementById("reset-link-panel").classList.toggle("reset-open");
    });

    document.getElementById("reset-link-close").addEventListener("click", function () {
        document.getElementById("reset-link-panel").classList.remove("reset-open");
    });

    /*----------------------------------------- reset password -----------------------------------------*/

    document.getElementById("reset-link").addEventListener("click", function () {
        document.getElementById("log-panel").classList.remove("log-open");
        document.getElementById("sign-panel").classList.remove("sign-open");
        document.getElementById("reset-link-panel").classList.remove("reset-open");
        document.getElementById("reset-password-panel").classList.toggle("reset-password-open");
    });

    document.getElementById("reset-password-close").addEventListener("click", function () {
        document.getElementById("reset-password-panel").classList.remove("reset-password-open");
    });

    

    /*----------------------------------------- checkout -----------------------------------------*/


    var cart = localStorage.getItem('cart') ? JSON.parse(localStorage.getItem('cart')) : {};
    
    console.log(cart);

    var sum = 0;
    var totalPrice = 0;
    var itemsContainer = document.getElementById('items');
    var itemsJson = document.getElementById('itemsJson');

    if (Object.keys(cart).length === 0) {
        var emptyCartMessage = document.createElement('p');
        emptyCartMessage.textContent = 'Your cart is empty, please add some items to your cart before checking out!';
        itemsContainer.appendChild(emptyCartMessage);
    } 
    else {
        for (var item in cart) {
            if (cart.hasOwnProperty(item)) {
                let name = cart[item][1];
                let qty = cart[item][0];
                let itemPrice = cart[item][2];
                sum += qty;
                totalPrice += qty * itemPrice;

                var listItem = document.createElement('li');
                listItem.className = 'list-group-item d-flex justify-content-between align-items-center';

                var nameDiv = document.createElement('div');
                nameDiv.className = 'col-md-5';
                nameDiv.textContent = name;

                var priceDiv = document.createElement('div');
                priceDiv.className = 'col-md-5';
                priceDiv.innerHTML = `<b> Price : ${itemPrice}</b>`;

                var badgeSpan = document.createElement('span');
                badgeSpan.className = 'badge badge-primary badge-pill';
                badgeSpan.textContent = qty;

                listItem.appendChild(nameDiv);
                listItem.appendChild(priceDiv);
                listItem.appendChild(badgeSpan);
                itemsContainer.appendChild(listItem);
            }
        }
        document.getElementById('totalprice').textContent = totalPrice;
    }

    if (itemsJson) {
        itemsJson.value = JSON.stringify(cart);
    }

    var thank = "{{ thank }}"
    if (thank) {    
        localStorage.clear();
        // document.location = "/";
    }

    document.getElementById("amt").value = totalPrice;

});

/*----------------------------------------- cart functionality -----------------------------------------*/
    
    // Initialize cart from localStorage
    let cart = localStorage.getItem('cart') ? JSON.parse(localStorage.getItem('cart')) : {};
    updateCartPanel(cart);
    
    // Function to update the cart when quantity changes
    function updateCartQuantity(idstr) {
        let qtyInput = document.getElementById('quantity' + idstr);
        let qty = parseInt(qtyInput.value);
        
        if (cart[idstr]) {
            cart[idstr][0] = qty; // Update the quantity in the cart
        }
        
        // Save updated cart to localStorage and update UI
        localStorage.setItem('cart', JSON.stringify(cart));
        updateCartPanel(cart);
    }
    
    // Add to cart functionality
    document.querySelectorAll('.divpr').forEach(div => {
        div.addEventListener('click', function(event) {
            if (event.target.classList.contains('cart')) {
                let idstr = event.target.id.toString();

                // Get selected color and size
                let color = document.getElementById('color').value;
                let size = document.getElementById('size').value;
                let qtyInput = document.getElementById('quantity' + idstr); // Get the quantity input
                let qty = parseInt(qtyInput.value); // Get the current quantity

                // Validate color and size selection
                if (!color || !size) {
                    alert("Please select both color and size options before adding to cart.");
                    return; // Stop function execution if color or size is not selected
                }

                // Proceed with adding to cart if color and size are selected
                if (cart[idstr] !== undefined) {
                    cart[idstr][0] += qty; // Increment quantity
                } else {
                    // Get product details
                    let name = document.getElementById('name' + idstr).innerHTML;
                    let price = document.getElementById('price' + idstr).innerHTML;
                    let imageUrl = document.getElementById('image' + idstr).getAttribute('src');  // Assuming you have an img tag with this ID in the HTML

                    // Store color and size in the cart data
                    cart[idstr] = [qty, name, price, color, size, imageUrl];  // Add color and size to cart data
                }
            
                // Save cart to localStorage and update UI
                localStorage.setItem('cart', JSON.stringify(cart));
                updateCartPanel(cart);
            
                // Open the cart panel after adding an item
                document.getElementById("cart-panel").classList.add("cart-open");
            }
        });
    });
    
    // Function to handle quantity increase
    document.querySelectorAll('[id^="increase"]').forEach(button => {
        button.addEventListener('click', function() {
            let idstr = button.id.replace('increase', ''); // Get product ID
            let qtyInput = document.getElementById('quantity' + idstr);
            qtyInput.value = parseInt(qtyInput.value) + 1;  // Increase quantity
        
            // Update cart with new quantity
            updateCartQuantity(idstr);
        });
    });
    
    // Function to handle quantity decrease
    document.querySelectorAll('[id^="decrease"]').forEach(button => {
        button.addEventListener('click', function() {
            let idstr = button.id.replace('decrease', ''); // Get product ID
            let qtyInput = document.getElementById('quantity' + idstr);
            let newQty = parseInt(qtyInput.value) - 1; // Decrease quantity
        
            // Prevent quantity from going below 1
            if (newQty > 0) {
                qtyInput.value = newQty; 
                // Update cart with new quantity
                updateCartQuantity(idstr);
            }
        });
    });
    
    // Prevent manual negative input in quantity field
    document.querySelectorAll('[id^="quantity"]').forEach(input => {
        input.addEventListener('blur', function() {
            let qty = parseInt(input.value);
            let idstr = input.id.replace('quantity', '');
        
            if (qty < 1 || isNaN(qty)) {
                input.value = 1;
                updateCartQuantity(idstr); // Update cart to reflect this change
            }
        });
    });
    
    
    // Function to update the sliding cart panel
    function updateCartPanel(cart) {
        let cartContent = "";
        let total = 0;
        var totalItems = 0;
    
        for (let item in cart) {
            let qty = cart[item][0];
            let name = cart[item][1];
            let price = parseFloat(cart[item][2]);
            let imageUrl = cart[item][5];
        
            // Calculate total for each item
            total += qty * price;
            totalItems += qty;
        
            // Generate HTML for each cart item
            cartContent += `
                <div class="cart-item">
                    <img src="${imageUrl}" class="cart-item-image">
                    <div class="cart-item-details">
                        <p class="cart-item-name">${name}</p>
                        <p class="cart-item-quantity">${qty} x $${price}</p>
                        <p class="cart-item-price">$${(qty * price).toFixed(2)}</p>
                    </div>
                    <span class="cart-remove-item" data-id="${item}">✕</span>
                </div>`;
        }
    
        // Update the cart panel HTML
        document.querySelector('.cart-content').innerHTML = cartContent;
        document.querySelector('.cart-footer h5').innerHTML = `Total: $${total.toFixed(2)}`;
        document.getElementById('cart').textContent = totalItems;
    }
    
    // Clear the cart
    function clearCart() {
        cart = {};
        localStorage.clear();
        updateCartPanel(cart);
    }
    
    document.getElementById('clear-cart').addEventListener('click', function(event) {
        clearCart();
    });
    
    // Remove individual item
    document.querySelector('.cart-content').addEventListener('click', function(event) {
        if (event.target.classList.contains('cart-remove-item')) {
            let id = event.target.getAttribute('data-id');
            delete cart[id];
            localStorage.setItem('cart', JSON.stringify(cart));
            updateCartPanel(cart);
        }
    });


    /*----------------------------------------- load products -----------------------------------------*/


    document.addEventListener("DOMContentLoaded", function() {
      const products = document.querySelectorAll(".shop-product");
      const seeMoreBtn = document.getElementById("seeMoreBtn");
      const seeLessBtn = document.getElementById("seeLessBtn");

      let visibleCount = 20;

      const showProducts = () => {
        products.forEach((product, index) => {
          product.style.display = index < visibleCount ? "block" : "none";
        });
      };

      seeMoreBtn.addEventListener("click", () => {
        visibleCount += 20;
        showProducts();
        seeLessBtn.style.display = "inline-block";


        if (visibleCount >= products.length) {
          seeMoreBtn.style.display = "none";
        }
      });


      seeLessBtn.addEventListener("click", () => {
        visibleCount = Math.max(20, visibleCount - 20);
        showProducts();
        seeMoreBtn.style.display = "inline-block";

        if (visibleCount === 20) {
          seeLessBtn.style.display = "none";
        }
      });


      showProducts();
    });
