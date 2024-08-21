
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
  const editButtons = document.querySelectorAll('.edit-btn');

  editButtons.forEach(button => {
    button.addEventListener('click', function() {
      const orderId = this.getAttribute('data-order_id');
      const invoice_number = this.getAttribute('data-invoice_number');
      const product_name = this.getAttribute('data-product_name');
      const supplier = this.getAttribute('data-supplier');
      const qty = this.getAttribute('data-qty');
      const price = this.getAttribute('data-price');
      const subtotal = this.getAttribute('data-subtotal');
      const status = this.getAttribute('data-status');
      const date_order = this.getAttribute('data-date_order');
      // Populate the form fields in the modal
      document.getElementById('orderId').value = orderId;
      document.getElementById('invoice_number').value = invoice_number;
      document.getElementById('product_name').value = product_name;
      document.getElementById('supplier').value = supplier;
      document.getElementById('qty').value = qty;
      document.getElementById('price').value = price;
      document.getElementById('subtotal').value = subtotal;
      document.getElementById('status').value = status;
      document.getElementById('date_order').value = date_order;
      // Show the modal
      const editOrderModal = new bootstrap.Modal(document.getElementById('editOrderModal'));
      editOrderModal.show();
    });
  });
});

function submitOrderForm() {
  document.getElementById('orderForm').submit();
}
document.getElementById("orderForm").addEventListener("input", function () {
  const qty = parseFloat(document.getElementById("qty").value) || 0;
  const price = parseFloat(document.getElementById("price").value) || 0;
  const subtotal = qty * price;
  document.getElementById("subtotal").value = subtotal.toFixed(2);
});