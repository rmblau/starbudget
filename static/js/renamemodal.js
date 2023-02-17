var renameModal = document.getElementById('renameModal')
renameModal.addEventListener('show.bs.modal', function (event) {
    // Button that triggered the modal
    var button = event.relatedTarget
    //var category = button.dataset.category
    // Extract info from data-bs-* attributes
    var category = button.getAttribute('data-bs-name')
    // If necessary, you could initiate an AJAX request here
    // and then do the updating in a callback.
    //
    // Update the modal's content.
    var modalTitle = renameModal.querySelector('.modal-title')
    var modalBodyInput = renameModal.querySelector('.modal-body input')
    modalTitle.textContent = 'Rename Category ' + category
    modalBodyInput.value = category
})

var deleteModal = document.getElementById('deleteModal')
deleteModal.addEventListener('show.bs.modal', function (event) {
    // Button that triggered the modal
    var button = event.relatedTarget
    //var category = button.dataset.category
    // Extract info from data-bs-* attributes
    var category = button.getAttribute('data-bs-name')
    // If necessary, you could initiate an AJAX request here
    // and then do the updating in a callback.
    //
    // Update the modal's content.
    var modalTitle = deleteModal.querySelector('.modal-title')
    var modalBodyInput = deleteModal.querySelector('.modal-body input')
    modalTitle.textContent = 'Delete Category ' + category
    modalBodyInput.value = category
})

