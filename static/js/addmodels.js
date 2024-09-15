
// Handle form submission for customers
function submitCustomerForm() {
  document.getElementById('customerForm').submit();
}

// Handle form submission for users
function submitUserForm() {
  document.getElementById('userForm').submit();
}
function openProductModal(button) {
  const form = document.getElementById('productForm');

  if (button) {
      // Edit mode
      const id = button.getAttribute('data-id');
      const name = button.getAttribute('data-name');
      const unit = button.getAttribute('data-unit');
      const category = button.getAttribute('data-category-id');
      const price = button.getAttribute('data-price');
      const description = button.getAttribute('data-description');

      // Populate form for editing
      document.getElementById('productId').value = id;
      document.getElementById('productName').value = name;
      document.getElementById('product_unit').value = unit;
      document.getElementById('category_name').value = category;
      document.getElementById('productPrice').value = price;
      document.getElementById('productDescription').value = description;

      // Update form action and modal title for editing
      form.action = `/edit_product/${id}`;  // Directly set URL
      document.getElementById('submitProductBtn').textContent = 'Update Product';
      document.getElementById('addProductLabel').textContent = 'Edit Product';
  } else {
      // Add mode
      form.reset();
      document.getElementById('productId').value = '';
      form.action = "{{ url_for('add_product') }}";  // Ensure this URL is correct
      document.getElementById('submitProductBtn').textContent = 'Add Product';
      document.getElementById('addProductLabel').textContent = 'Add New Product';
  }

  new bootstrap.Modal(document.getElementById('addProduct')).show();
}











// Open User Edit Modal with pre-filled data
function openUserEditModal(button) {
  const modal = new bootstrap.Modal(document.getElementById('addUser'));
  document.getElementById('userId').value = button.getAttribute('data-id');
  document.getElementById('userName').value = button.getAttribute('data-name');
  document.getElementById('userTel').value = button.getAttribute('data-tel');
  document.getElementById('userEmail').value = button.getAttribute('data-email');
  document.getElementById('userRole').value = button.getAttribute('data-role');
  document.getElementById('userStatus').value = button.getAttribute('data-status');
  document.getElementById('userImage').value = ''; // Reset file input
  modal.show();
}

// Confirm deletion of a user
function confirmDelete(userId) {
  if (confirm('Are you sure you want to delete this user?')) {
      document.getElementById(`deleteForm${userId}`).submit();
  }
}
function openCustomerEditModal(button) {
  const modal = new bootstrap.Modal(document.getElementById('addCustomer'));
  document.getElementById('customerId').value = button.getAttribute('data-id');
  document.getElementById('customerName').value = button.getAttribute('data-name');
  document.getElementById('customerTel').value = button.getAttribute('data-tel');
  document.getElementById('customerEmail').value = button.getAttribute('data-email');
  document.getElementById('customerGender').value = button.getAttribute('data-gender');
  modal.show();
}

// Confirm deletion of a customer
function confirmDelete(customerId) {
  if (confirm('Are you sure you want to delete this customer?')) {
    document.getElementById(`deleteForm${customerId}`).submit();
  }
}



function submitSupplierForm() {
  document.getElementById('supplierForm').submit();
}

function openSupplierEditModal(button) {
  const modal = new bootstrap.Modal(document.getElementById('editSupplierModal'));


  document.getElementById('SupplierId').value = button.getAttribute('data-id');
  document.getElementById('supplierName').value = button.getAttribute('data-name');
  document.getElementById('supplierContact').value = button.getAttribute('data-contact');
  document.getElementById('supplierEmail').value = button.getAttribute('data-email');
  document.getElementById('supplierCompany').value = button.getAttribute('data-company');
  document.getElementById('supplierAddress').value = button.getAttribute('data-address');
  document.getElementById('supplierDate').value = button.getAttribute('data-date-added');
  modal.show();
}

document.addEventListener('DOMContentLoaded', function() {
  const supplierSelect = document.getElementById('supplier');
  const supplierTextbox = document.getElementById('supplierName'); // Ensure this ID matches your HTML

  supplierSelect.addEventListener('change', function() {
    const selectedOption = supplierSelect.options[supplierSelect.selectedIndex];
    const supplierName = selectedOption.getAttribute('data-supplier-name');
    supplierTextbox.value = supplierName; // Update the text box with the selected supplier's name
  });

  const orderForm = document.getElementById('orderForm');
  orderForm.addEventListener('submit', function(event) {
    const selectedSupplier = supplierSelect.value;
    if (!selectedSupplier) {
      alert('Please select a supplier.');
      event.preventDefault(); // Prevent form submission if no supplier is selected
    }
  });
});






document.addEventListener('DOMContentLoaded', function () {
  // Populate the edit form in the modal with order details
  window.populateForm = function(button) {
    const orderId = button.getAttribute('data-order_id');
    const invoiceNumber = button.getAttribute('data-invoice_number');
    const supplier = button.getAttribute('data-supplier');
    const productName = button.getAttribute('data-product_name');
    const unit = button.getAttribute('data-unit');
    const qty = button.getAttribute('data-qty');
    const price = button.getAttribute('data-price');
    const subtotal = button.getAttribute('data-subtotal');
    const dateOrder = button.getAttribute('data-date_order');
    const status = button.getAttribute('data-status');

    document.getElementById('orderId').value = orderId;
    document.getElementById('invoice_number').value = invoiceNumber;
    document.getElementById('supplier').value = supplier;
    document.getElementById('productId').value = productName;
    document.getElementById('product_unit').value = unit;
    document.getElementById('qty').value = qty;
    document.getElementById('price').value = price;
    document.getElementById('subtotal').value = subtotal;
    document.getElementById('date_order').value = dateOrder;
    document.getElementById('status').value = status;

    // Update form action to the edit route
    document.getElementById("editOrderForm").action = `/edit_order/${orderId}`;

    // Show the modal
    const modal = new bootstrap.Modal(document.getElementById('editOrderModal'));
    modal.show();
  };

  // Attach event listeners to all edit buttons
  document.querySelectorAll(".edit-btn").forEach((button) => {
    button.addEventListener("click", () => populateForm(button));
  });

  // Calculate subtotal
  function calculateSubtotal() {
    const qty = parseFloat(document.getElementById("qty").value) || 0;
    const price = parseFloat(document.getElementById("price").value) || 0;
    const subtotal = qty * price;
    document.getElementById("subtotal").value = subtotal.toFixed(2);
  }

  document.getElementById("qty").addEventListener("input", calculateSubtotal);
  document.getElementById("price").addEventListener("input", calculateSubtotal);

  // Remove or adjust category modal functions if not used
});





    // Populate the modal fields with the product data
    function openProductEditModal(button) {
      const form = document.getElementById('editProductForm');
      form.action = '/edit_product/' + button.getAttribute('data-id');
      document.getElementById('editProductName').value = button.getAttribute('data-name');
      document.getElementById('editProductUnit').value = button.getAttribute('data-unit');
      document.getElementById('editProductPrice').value = button.getAttribute('data-price');
      document.getElementById('editProductDescription').value = button.getAttribute('data-description');
      new bootstrap.Modal(document.getElementById('editProductModal')).show();
  }


    // Set the form action URL for updating the product (assuming a route for editing exists)
    const form = document.getElementById('addProductForm');
    form.action = `/edit_product/${productId}`;

    // Show the modal
    const addProductModal = new bootstrap.Modal(document.getElementById('addProduct'));
    addProductModal.show();


// Function to confirm product deletion
function confirmDelete(productId) {
    const confirmed = confirm("Are you sure you want to delete this product?");
    if (confirmed) {
        // Submit the form to delete the product
        document.getElementById(`deleteForm${productId}`).submit();
    }
}


//<!-- Pagination Controls -->
document.addEventListener('DOMContentLoaded', function() {
  const rowsPerPage = 10; // Number of rows per page
  let currentPage = 1;
  const tableRows = Array.from(document.querySelectorAll('#salesTableBody tr'));
  const totalPages = Math.ceil(tableRows.length / rowsPerPage);

  function showPage(page) {
      tableRows.forEach((row, index) => {
          row.style.display = (index >= (page - 1) * rowsPerPage && index < page * rowsPerPage) ? '' : 'none';
      });
      document.getElementById('pageInfo').textContent = `Page ${page} of ${totalPages}`;
      document.getElementById('prevPage').disabled = page === 1;
      document.getElementById('nextPage').disabled = page === totalPages;
  }

  document.getElementById('prevPage').addEventListener('click', function() {
      if (currentPage > 1) {
          currentPage--;
          showPage(currentPage);
      }
  });

  document.getElementById('nextPage').addEventListener('click', function() {
      if (currentPage < totalPages) {
          currentPage++;
          showPage(currentPage);
      }
  });

  showPage(currentPage); // Initial call to display the first page
});

//<!--end  Pagination Controls -->
function updateProductDetails() {
  const productId = document.getElementById("productId").value;
  const selectedOption = document.querySelector("#productId option:checked");
  if (selectedOption) {
    const price = selectedOption.getAttribute("data-price");
    const quantity = selectedOption.getAttribute("data-qty");
    document.getElementById("priceSale").value = price;
    document.getElementById("quty").value = quantity;
  }
}



 document.addEventListener("DOMContentLoaded", function () {
    const oldQuantityField = document.getElementById("quty");
    const saleQuantityField = document.getElementById("qty");
    const errorMessage = document.getElementById("error-message");
    function validateSaleQuantity() {
      const oldQuantity = parseInt(oldQuantityField.value, 10);
      const saleQuantity = parseInt(saleQuantityField.value, 10);
      errorMessage.textContent = "";
      // Validate oldQuantity
      if (isNaN(oldQuantity) || oldQuantity <= 0) {
        errorMessage.textContent = "Old quantity is invalid.";
        saleQuantityField.disabled = true;
        return;
      } else {
        saleQuantityField.disabled = false;
      }
      // Validate saleQuantity
      if (isNaN(saleQuantity) || saleQuantity <= 0) {
        errorMessage.textContent = "Sale quantity must be a positive number.";
      } else if (saleQuantity > oldQuantity) {
        errorMessage.textContent = "Sale quantity cannot exceed old quantity.";
      }
    }
    // Add event listeners
    oldQuantityField.addEventListener("input", validateSaleQuantity);
    saleQuantityField.addEventListener("input", validateSaleQuantity);
  });

  document.addEventListener("DOMContentLoaded", function () {
    var priceSaleInput = document.getElementById("priceSale");
    var qtyInput = document.getElementById("qty");
    var subtotalInput = document.getElementById("subtotal");
    var discountInput = document.getElementById("discount");
    var paymentInput = document.getElementById("payment");
    var balanceInput = document.getElementById("Balance");
    var qutyInput = document.getElementById("quty"); // Old quantity

    // Function to update product details when a product is selected
    function updateProductDetails() {
      var selectedProduct =
        document.getElementById("productId").selectedOptions[0];
      var price = selectedProduct.getAttribute("data-price");
      var qty = selectedProduct.getAttribute("data-qty");

      priceSaleInput.value = price;
      qutyInput.value = qty;
      calculateSubtotal();
    }

    // Function to calculate subtotal
    function calculateSubtotal() {
      var price = parseFloat(priceSaleInput.value) || 0;
      var qty = parseFloat(qtyInput.value) || 0;
      var discount = parseFloat(discountInput.value) || 0;
      var subtotal = price * qty - discount;

      subtotalInput.value = subtotal.toFixed(2);
      updateBalance();
    }

    // Function to update the balance based on payment
    function updateBalance() {
      var payment = parseFloat(paymentInput.value) || 0;
      var subtotal = parseFloat(subtotalInput.value) || 0;
      var balance = subtotal - payment;

      balanceInput.value = balance.toFixed(2);
    }

    // Event listeners for dynamic updates
    qtyInput.addEventListener("input", calculateSubtotal);
    discountInput.addEventListener("input", calculateSubtotal);
    paymentInput.addEventListener("input", updateBalance);
    document
      .getElementById("productId")
      .addEventListener("change", updateProductDetails);
  });




 // satart  Function to populate the modal with supplier data for editing
  // Function to show a confirmation dialog before deletion
  function confirmDelete(supplierId) {
    if (confirm("Are you sure you want to delete this supplier?")) {
      document.getElementById("deleteForm" + supplierId).submit();
    }
  }

  // Function to populate the modal with supplier data for editing
  function addSupplier(id, name, contact, email, company, address, dateAdded) {
    document.getElementById("supplierId").value = id;
    document.getElementById("name").value = name;
    document.getElementById("contact").value = contact;
    document.getElementById("email").value = email;
    document.getElementById("company").value = company;
    document.getElementById("address").value = address;
    document.getElementById("dateAdded").value = dateAdded;
    document.getElementById("supplierModalLabel").innerText = id
      ? "Edit Supplier"
      : "Add Supplier";
  }




















