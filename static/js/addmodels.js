// Submit customer form
// Submit customer form
function submitCustomerForm() {
    document.getElementById("customerForm").submit();
}

// Open modal for editing customer
function openModalForEditCustomer(button) {
    // Extract data attributes from the button
    const customerId = button.getAttribute("data-id");
    const customerName = button.getAttribute("data-name");
    const customerTel = button.getAttribute("data-tel");
    const customerEmail = button.getAttribute("data-email");
    const customerGender = button.getAttribute("data-gender");
    const customerDate = button.getAttribute("data-date");

    // Populate the form fields
    document.getElementById("customerName").value = customerName;
    document.getElementById("customerTel").value = customerTel;
    document.getElementById("customerEmail").value = customerEmail;
    document.getElementById("customerGender").value = customerGender;
    document.getElementById("customerDate").value = customerDate;
    document.getElementById("customerId").value = customerId;

    // Show the modal
    $("#addcustomer").modal("show");
}

// Reset customer form when modal is closed
document.addEventListener("DOMContentLoaded", function () {
    const customerModal = document.getElementById("addcustomer");
    customerModal.addEventListener("hidden.bs.modal", function () {
        document.getElementById("customerForm").reset();
        document.getElementById("customerId").value = ""; // Clear customerId
    });
});

// Confirm delete customer
function confirmDelete(customerId) {
    if (confirm("Are you sure you want to delete this customer?")) {
        const form = document.getElementById(`deleteForm${customerId}`);
        if (form) {
            form.submit();
        } else {
            console.error(`Form with ID deleteForm${customerId} not found.`);
        }
    }
}

  
// Submit user form
function submitUserForm() {
    document.getElementById("userForm").submit();
}
  // Open modal for editing user
  function openModalForEditUser(button) {
    const userId = button.getAttribute("data-id");
    const userName = button.getAttribute("data-name");
    const userTel = button.getAttribute("data-tel");
    const userEmail = button.getAttribute("data-email");
    const userPassword = button.getAttribute("data-password");
    const userRole = button.getAttribute("data-role");
    const userStatus = button.getAttribute("data-status");
    const userDate = button.getAttribute("data-date");
  
    document.getElementById("userName").value = userName;
    document.getElementById("userTel").value = userTel;
    document.getElementById("userEmail").value = userEmail;
    document.getElementById("userPassword").value = userPassword;
    document.getElementById("userRole").value = userRole;
    document.getElementById("userStatus").value = userStatus;
    document.getElementById("userDate").value = userDate;
    document.getElementById("userId").value = userId;
    $("#addUser").modal("show");
  }
  
  // Reset user form when modal is closed
  document.addEventListener("DOMContentLoaded", function () {
    const userModal = document.getElementById("addUser");
    userModal.addEventListener("hidden.bs.modal", function () {
      document.getElementById("userForm").reset();
      document.getElementById("userId").value = ""; // Clear userId
    });
  });
  
  // Open modal for editing supplier
  function openModalForEditSupplier(button) {
    const supplierId = button.getAttribute('data-id');
    const name = button.getAttribute('data-name');
    const contact = button.getAttribute('data-contact');
    const email = button.getAttribute('data-email');
    const company = button.getAttribute('data-company');
    const address = button.getAttribute('data-address');
    const date = button.getAttribute('data-date');
    
    const modal = document.getElementById('addSupplier'); // Use correct modal ID here
    modal.querySelector('input[name="supplierId"]').value = supplierId;
    modal.querySelector('input[name="supplierName"]').value = name;
    modal.querySelector('input[name="supplierContact"]').value = contact;
    modal.querySelector('input[name="supplierEmail"]').value = email;
    modal.querySelector('input[name="supplierCompany"]').value = company;
    modal.querySelector('input[name="supplierAddress"]').value = address;
    modal.querySelector('input[name="supplierDate"]').value = date;
    
    $("#addSupplier").modal('show');
  }
  
// Submit supplier form
function submitSupplierForm() {
    document.getElementById("supplierForm").submit();
}