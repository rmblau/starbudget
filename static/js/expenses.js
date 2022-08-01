var updateModal = document.getElementById('updateModal')
updateModal.addEventListener('show.bs.modal', function (event) {
    // Button that triggered the modal
    var button = event.relatedTarget
    //var category = button.dataset.category
    // Extract info from data-bs-* attributes
    var description = button.getAttribute('data-bs-description')
    var category = button.getAttribute('data-bs-category')
    var oldcategory = updateModal.querySelector('#oldcategory')
    var date = button.getAttribute('data-bs-date')
    var submitTime = button.getAttribute('data-bs-submit-time')
    var recipient = button.getAttribute('data-bs-recipient')
    var amount = button.getAttribute('data-bs-amount')
    // If necessary, you could initiate an AJAX request here
    // and then do the updating in a callback.
    //
    // Update the modal's content.
    var modalTitle = updateModal.querySelector('.modal-title')
    var modalBodyInput = updateModal.querySelector('.modal-body input')
    var oldName = updateModal.querySelector("#oldname");
    var dateInput = updateModal.querySelector('#date')
    var oldDate = updateModal.querySelector('#olddate')
    var amountInput = updateModal.querySelector('#amount')
    var categoryInput = updateModal.querySelector('#category')
    var receipientInput = updateModal.querySelector("#recipient")
    var submitTimeInput = updateModal.querySelector('#submitTime').value = submitTime

    modalTitle.textContent = 'Update Expense ' + category
    modalBodyInput.value = description
    oldName.value = description
    dateInput.value = date
    oldDate.value = date
    amountInput.value = amount
    oldcategory.value = category
    categoryInput.value = category
    receipientInput.value = recipient
    //submitTimeInput.value = submitTime
})