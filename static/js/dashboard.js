const checkoutButton = document.getElementById("add-product-link");
    if (checkoutButton) {
        checkoutButton.addEventListener("click", (event) => {
            event.preventDefault();
            const checkoutModal = document.getElementById("add_product");
            checkoutModal.style.display = "block";
        });
    }

    // Add event listener for closing the modal
    const closeModal = document.getElementById("closeModal");
    if (closeModal) {
        closeModal.addEventListener("click", () => {
            const checkoutModal = document.getElementById("add_product");
            checkoutModal.style.display = "none";
        });
    }