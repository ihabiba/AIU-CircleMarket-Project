// Selectors
const cartItems = document.getElementById('cart-items');
const cartTotal = document.getElementById('cart-total');
let cart = [];

// Function to add an item to the cart
function addToCart(element) {
    const productId = element.getAttribute('data-id');
    const productName = element.getAttribute('data-name');
    const productPrice = parseFloat(element.getAttribute('data-price'));

    // Check if the product is already in the cart
    const existingProduct = cart.find(item => item.id === productId);
    if (existingProduct) {
        existingProduct.quantity++;
    } else {
        cart.push({ id: productId, name: productName, price: productPrice, quantity: 1 });
    }

    updateCart();
}

// Function to remove an item from the cart
function removeFromCart(productId) {
    cart = cart.filter(item => item.id !== productId);
    updateCart();
}

// Function to update the cart UI
function updateCart() {
    cartItems.innerHTML = ''; // Clear the current cart items
    let total = 0;

    cart.forEach(item => {
        const li = document.createElement('li');
        li.innerHTML = `
            ${item.name} (x${item.quantity}) - RM${(item.price * item.quantity).toFixed(2)}
            <span class="remove-item" onclick="removeFromCart('${item.id}')">Remove</span>
        `;
        cartItems.appendChild(li);
        total += item.price * item.quantity;
    });

    cartTotal.textContent = total.toFixed(2);
}
const scroReveal = {
    distance: "50px",
    origin: "bottom",
    duration: 500,
};
document.addEventListener('DOMContentLoaded', function() {
    document.getElementById('search-button').addEventListener('click', function() {
        document.getElementById('search-popup').style.display = 'block';
    });

    document.getElementById('close-search').addEventListener('click', function() {
        document.getElementById('search-popup').style.display = 'none';
    });
});

ScrollReveal().reveal(".product-item", {
...scroReveal,
});
ScrollReveal().reveal(".category .first", {
    ...scroReveal,
  });
  ScrollReveal().reveal(".category .men", {
    ...scroReveal,
    delay: 500,
  });
  ScrollReveal().reveal(".category .others", {
    ...scroReveal,
    delay: 1000,
  });
