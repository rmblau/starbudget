var updateModal = document.getElementById('updateModal')
updateModal.addEventListener('show.bs.modal', function (event) {
    // Button that triggered the modal
    var button = event.relatedTarget
    //var category = button.dataset.category
    // Extract info from data-bs-* attributes
    var description = button.getAttribute('data-bs-description')
    var category = button.getAttribute('data-bs-category')
    var date = button.getAttribute('data-bs-date')
    var submitTime = button.getAttribute('data-bs-submit-time')
    var recipient = button.getAttribute('data-bs-recipient')
    var amount = button.getAttribute('data-bs-amount')
    // If necessary, you could initiate an AJAX request here
    // and then do the updating in a callback.
    //
    // Update the modal's content.
    var modalTitle = updateModal.querySelector('#modal-title');
    var modalBodyInput = updateModal.querySelector('.modal-body input');
    var oldName = updateModal.querySelector("#oldname");
    var newName = updateModal.querySelector('#newname');
    var dateInput = updateModal.querySelector('#date');
    var oldDate = updateModal.querySelector('#olddate');
    var amountInput = updateModal.querySelector('#oldamount');
    var newAmountInput = updateModal.querySelector('#newamount')
    var oldcategory = updateModal.querySelector('#old-category').value = category;
    var categoryInput = updateModal.querySelector('#category');
    var receipientInput = updateModal.querySelector("#old_recipient");
    var newRecipientInput = updateModal.querySelector('#newrecipient');
    var submitTimeInput = updateModal.querySelector('#submitTime').value = submitTime;

    modalTitle.textContent = 'Update Expense ' + description
    modalBodyInput.value = description
    oldName.value = description
    newName.value = description
    dateInput.value = date
    oldDate.value = date
    amountInput.value = amount
    newAmountInput.value = amount
    oldcategory.value = category
    categoryInput.value = category
    receipientInput.value = recipient
    newRecipientInput.value = recipient
})

var categoryBalance = document.getElementById('balanceModal')
categoryBalance.addEventListener('show.bs.modal', function (event){
    var button = event.relatedTarget
    var balance = button.getAttribute('data-bs-remaining-balance');
    console.log(balance)
    var modalBodyInput = deleteModal.querySelector('.modal-body input')
    modalBodyInput.value = balance
    var modalTitle = deleteModal.querySelector('.modal-title')
    modalTitle.textContent = 'Delete Category ' + balance
    var oldBalance = updateModal.querySelector('#oldbalance');
    oldBalance.value = balance

})