document.addEventListener('DOMContentLoaded', function() {
    var backToTopButton = document.getElementById("backToTop");

    function toggleBackToTopButton() {
        if (window.scrollY > 300) {
            backToTopButton.classList.add("show");
        } else {
            backToTopButton.classList.remove("show");
        }
    }

    window.addEventListener("scroll", toggleBackToTopButton);

    backToTopButton.addEventListener("click", function() {
        window.scrollTo({ top: 0, behavior: 'smooth' });
    });
});

$(document).ready(function () {
    // Handle Edit Ticket Modal
    $('#editModal').on('show.bs.modal', function (event) {
        var button = $(event.relatedTarget);
        var ticketId = button.data('id');
        var subject = button.data('subject');
        var description = button.data('description');
        var modal = $(this);
        modal.find('#editSubject').val(subject);
        modal.find('#editDescription').val(description);
        modal.find('#editTicketForm').attr('action', '/update_ticket/' + ticketId);
    });

    // Handle Delete Ticket Modal
    $('#deleteModal').on('show.bs.modal', function (event) {
        var button = $(event.relatedTarget);
        var ticketId = button.data('id');
        var modal = $(this);
        modal.find('#deleteTicketForm').attr('action', '/delete_ticket/' + ticketId);
    });

    // Handle Status Change Modal
    $('#statusModal').on('show.bs.modal', function (event) {
        var button = $(event.relatedTarget);
        var ticketId = button.data('id');
        var status = button.data('status');
        var modal = $(this);
        modal.find('#statusSelect').val(status);
        modal.find('#statusForm').attr('action', '/update_ticket_status/' + ticketId);
    });

    // Display flash messages
    $('.alert').alert();
});
