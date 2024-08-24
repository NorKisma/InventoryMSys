
// Handle form submission for customers
function submitCustomerForm() {
  document.getElementById('customerForm').submit();
}

// Handle form submission for users
function submitUserForm() {
  document.getElementById('userForm').submit();
}

// Handle form submission for suppliers

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





function openOrderEditModal(button) {
  const modal = new bootstrap.Modal(
    document.getElementById("editOrderModal")
  );

  document.getElementById("orderId").value =
    button.getAttribute("data-order_id");
  document.getElementById("invoice_number").value = button.getAttribute(
    "data-invoice_number"
  );
  document.getElementById("supplier").value =
    button.getAttribute("data-supplier");
  document.getElementById("product_name").value =
    button.getAttribute("data-product_name");
    document.getElementById("product_unit").value =
    button.getAttribute("data-product_unit");
  document.getElementById("qty").value = button.getAttribute("data-qty");
  document.getElementById("price").value =
    button.getAttribute("data-price");
  document.getElementById("subtotal").value =
    button.getAttribute("data-subtotal");
  document.getElementById("status").value =
    button.getAttribute("data-status");
  document.getElementById("date_order").value =
    button.getAttribute("data-date_order");

  // Update form action to the edit route
  document.getElementById(
    "editOrderForm"
  ).action = `/edit_order/${button.getAttribute("data-order_id")}`;

  modal.show();
}

document.querySelectorAll(".edit-btn").forEach((button) => {
  button.addEventListener("click", () => openOrderEditModal(button));
});

function calculateSubtotal() {
  const qty = parseFloat(document.getElementById("qty").value) || 0;
  const price = parseFloat(document.getElementById("price").value) || 0;
  const subtotal = qty * price;
  document.getElementById("subtotal").value = subtotal.toFixed(2);
}

document.getElementById("qty").addEventListener("input", calculateSubtotal);
document
  .getElementById("price")
  .addEventListener("input", calculateSubtotal);

  // Show the modal CategoryEditModal
function openCategoryEditModal(button) {
  const modal = new bootstrap.Modal(document.getElementById("addCategory"));

  document.getElementById("categoryId").value =
    button.getAttribute("data-id");
  document.getElementById("categoryName").value =
    button.getAttribute("data-name");
    document.getElementById("category_unit").value =
    button.getAttribute("data-unit");
  document.getElementById(
    "editCategoryForm"
  ).action = `/update_category/${button.getAttribute("data-id")}`;

  modal.show();
}





