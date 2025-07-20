// Get cart from localStorage
const cart = JSON.parse(localStorage.getItem("cart")) || [];

// Select the cart items container
const cartItemsContainer = document.getElementById("cart-items");

// Select the cart count element
const cartCountElement = document.getElementById("cart-count");

// Function to update cart count dynamically
function updateCartCount() {
    const totalCount = cart.reduce((sum, item) => sum + item.quantity, 0);
    cartCountElement.textContent = totalCount;
    localStorage.setItem("cartCount", totalCount);
}

// Function to render cart items
function renderCartItems() {
    // Clear existing items
    cartItemsContainer.innerHTML = '';

    // Render each product in the cart
    cart.forEach(product => {
        const row = document.createElement("tr");

        row.innerHTML = `
            <td class="align-middle">
                <img src="${product.image}" alt="Product Image" class="product-img"> ${product.name}
            </td>
            <td class="align-middle">RM${product.price.toFixed(2)}</td>
            <td class="align-middle">
                <div class="quantity-controls">
                    <button class="btn btn-sm btn-primary btn-minus">-</button>
                    <input type="text" value="${product.quantity}" class="quantity-input" readonly>
                    <button class="btn btn-sm btn-primary btn-plus">+</button>
                </div>
            </td>
            <td class="align-middle">RM${(product.price * product.quantity).toFixed(2)}</td>
            <td class="align-middle">
                <button class="btn btn-danger btn-sm remove-btn">Remove</button>
            </td>
        `;

        cartItemsContainer.appendChild(row);

        // Remove button functionality
        row.querySelector(".remove-btn").addEventListener("click", () => {
            const index = cart.findIndex(item => item.id === product.id);
            cart.splice(index, 1);
            localStorage.setItem("cart", JSON.stringify(cart));
            renderCartItems(); // Re-render cart items
            updateCartCount();
        });

        // Quantity controls
        row.querySelector(".btn-minus").addEventListener("click", () => {
            if (product.quantity > 1) {
                product.quantity--;
                updateCart();
            }
        });

        row.querySelector(".btn-plus").addEventListener("click", () => {
            product.quantity++;
            updateCart();
        });
    });

    // Update the cart summary
    updateCartSummary();
}

// Update cart and re-render
function updateCart() {
    localStorage.setItem("cart", JSON.stringify(cart));
    updateCartCount();
    renderCartItems(); // Re-render cart items
}

// Function to update cart summary
function updateCartSummary() {
    const subtotalElement = document.getElementById("subtotal");
    const totalElement = document.getElementById("total");
    const shippingCostElement = document.getElementById("shipping-cost"); // Get the shipping cost element
    
    // Calculate subtotal
    let subtotal = cart.reduce((sum, item) => sum + (item.price * item.quantity), 0);
    
    // Calculate shipping cost (RM1 for each product)
    const shippingCost = cart.length; // RM1 for each product
    const total = subtotal + shippingCost; // Total includes subtotal + shipping cost

    // Update the DOM elements
    subtotalElement.textContent = `RM${subtotal.toFixed(2)}`;
    shippingCostElement.textContent = `RM${shippingCost.toFixed(2)}`; // Update shipping cost display
    totalElement.textContent = `RM${total.toFixed(2)}`; // Adding shipping cost
}

// Initialize cart on page load
document.addEventListener("DOMContentLoaded", () => {
    renderCartItems();
    updateCartCount();

    // Add event listener for checkout button
    const checkoutButton = document.getElementById("checkoutButton");
    if (checkoutButton) {
        checkoutButton.addEventListener("click", (event) => {
            event.preventDefault();
            const checkoutModal = document.getElementById("checkoutModal");
            checkoutModal.style.display = "block";
        });
    }

    // Add event listener for closing the modal
    const closeModal = document.getElementById("closeModal");
    if (closeModal) {
        closeModal.addEventListener("click", () => {
            const checkoutModal = document.getElementById("checkoutModal");
            checkoutModal.style.display = "none";
        });
    }

    // Handle form submission
const checkoutForm = document.getElementById("checkoutForm");
if (checkoutForm) {
    checkoutForm.addEventListener("submit", (event) => {
        event.preventDefault();

        // Collect form data
        const formData = new FormData(checkoutForm);
        formData.append('cart', JSON.stringify(cart)); // Add cart data to the form

        // Send data to the server
        fetch('/place-order', {
            method: 'POST',
            body: formData
        })
        .then(response => {
            if (response.ok) {
                // Display the order status message
                const orderStatus = document.getElementById("order-status");
                orderStatus.style.display = "block"; // Show the message
                orderStatus.textContent = "Your order is pending. Thank you for your purchase!"; // Set the message text

                // Clear the cart
                localStorage.removeItem("cart"); // Clear the cart from localStorage
                cart.length = 0; // Clear the cart array
                renderCartItems(); // Re-render to show empty cart
                updateCartCount(); // Update cart count
                const checkoutModal = document.getElementById("checkoutModal");
                checkoutModal.style.display = "none"; // Close the modal
            } else {
                alert('There was an error placing your order. Please try again.');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('There was an error placing your order. Please try again.');
        });
    });
}
});