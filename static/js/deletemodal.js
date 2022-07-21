var updateModal = document.getElementById('updateModal')
updateModal.addEventListener('show.bs.modal', function (event) {
    // Button that triggered the modal
    var button = event.relatedTarget
    //var category = button.dataset.category
    // Extract info from data-bs-* attributes
    var category = button.getAttribute('data-bs-description')
    var date = button.getAttribute('data-bs-date')
    var amount = button.getAttribute('data-bs-amount')
    // If necessary, you could initiate an AJAX request here
    // and then do the updating in a callback.
    //
    // Update the modal's content.
    var modalTitle = updateModal.querySelector('.modal-title')
    var modalBodyInput = updateModal.querySelector('.modal-body input')
    var dateInput = updateModal.querySelector('#date')
    var amountInput = updateModal.querySelector('#amount')
    modalTitle.textContent = 'Update Expense ' + category
    modalBodyInput.value = category
    dateInput.value = date
    amountInput.value = amount
})