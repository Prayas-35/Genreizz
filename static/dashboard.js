$(document).ready(function () {
    $('.add-book-form').on('submit', function (event) {
        event.preventDefault();

        const form = $(this);
        const cardBody = form.closest('.card-body');
        const alert = cardBody.find('.alert');
        const data = form.serialize();

        $.ajax({
            url: '/add',
            method: 'POST',
            data: data,
            success: function (response) {
                alert.text(response.message);
                alert.show();
                alert.css('color', 'green');
                setTimeout(() => {
                    alert.hide();
                }, 3000);
            },
            error: function () {
                alert.text('An error occurred while adding the book.');
                alert.show();
                alert.css('color', 'red');
                setTimeout(() => {
                    alert.hide();
                }, 3000);
            }
        });
    });
});

$(document).ready(function () {
    $('.add-book-readlist').on('submit', function (event) {
        event.preventDefault();

        const form = $(this);
        const cardBody = form.closest('.card-body');
        const alert = cardBody.find('.alert');
        const data = form.serialize();

        $.ajax({
            url: '/add_read',
            method: 'POST',
            data: data,
            success: function (response) {
                alert.text(response.message);
                alert.show();
                setTimeout(() => {
                    alert.hide();
                }, 3000);
            },
            error: function () {
                alert.text('An error occurred while adding the book.');
                alert.show();
                setTimeout(() => {
                    alert.hide();
                }, 3000);
            }
        });
    });
});