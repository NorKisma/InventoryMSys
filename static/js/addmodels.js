
// Handle form submission for customers
function submitCustomerForm() {
  document.getElementById('customerForm').submit();
}

// Handle form submission for users
function submitUserForm() {
  document.getElementById('userForm').submit();
}

// Handle form submission for suppliers
function submitSupplierForm() {
  document.getElementById('supplierForm').submit();
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