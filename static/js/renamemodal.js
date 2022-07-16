var exampleModal = document.getElementById('renameModal')
exampleModal.addEventListener('show.bs.modal', function (event) {
    // Button that triggered the modal
    var button = event.relatedTarget
    //var category = button.dataset.category
    // Extract info from data-bs-* attributes
    var category = button.getAttribute('data-bs-whatever')
    // If necessary, you could initiate an AJAX request here
    // and then do the updating in a callback.
    //
    // Update the modal's content.
    var modalTitle = exampleModal.querySelector('.modal-title')
    var modalBodyInput = exampleModal.querySelector('.modal-body input')
    modalTitle.textContent = 'Rename Category ' + category
    modalBodyInput.value = category
})