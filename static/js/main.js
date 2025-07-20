const hamburger = document.querySelector(".hamburger");
const navList = document.querySelector(".nav-list");

if(hamburger){
    hamburger.addEventListener("click", () => {
        navList.classList.toggle("open");
    });
}


// Function to update cart count dynamically
function updateCartCount() {
    const cart = JSON.parse(localStorage.getItem("cart")) || [];
    const totalCount = cart.reduce((sum, item) => sum + item.quantity, 0);
    const cartCountElement = document.getElementById("cart-count");
    cartCountElement.textContent = totalCount;
}

// Add event listeners to add-to-cart buttons
const addToCartButtons = document.querySelectorAll(".add-to-cart-btn");

addToCartButtons.forEach(button => {
    button.addEventListener("click", (event) => {
        event.preventDefault(); // Prevent default anchor behavior

        // Get product data from attributes
        const productItem = button.closest(".product-item");
        const id = productItem.dataset.id;
        const name = productItem.dataset.name;
        const price = productItem.dataset.price;
        const image = productItem.dataset.image;

        // Create product object
        const product = { id: parseInt(id), name, price: parseFloat(price), image, quantity: 1 };

        // Get cart from localStorage
        let cart = JSON.parse(localStorage.getItem("cart")) || [];

        // Check if product already exists in the cart
        const existingProduct = cart.find(item => item.id === product.id);
        if (existingProduct) {
            existingProduct.quantity++;
        } else {
            cart.push(product);
        }

        // Save updated cart to localStorage
        localStorage.setItem("cart", JSON.stringify(cart));

        // Update cart count
        updateCartCount();

        alert(`${name} added to cart!`);
    });
});

// Initialize cart count on page load
document.addEventListener("DOMContentLoaded", updateCartCount);

//popu
