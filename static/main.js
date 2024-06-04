$(document).ready(function () {
    // Function to show the spinner
    function showSpinner() {
        $('#navlogin').css('visibility', 'hidden');
        $('#searchbtn').css('visibility', 'hidden');
        $('.spinner-wrapper').css('opacity', '1');
        $('.spinner-wrapper').css('visibility', 'visible');
    }

    // Function to hide the spinner
    function hideSpinner() {
        $('#navlogin').css('visibility', 'visible');
        $('#searchbtn').css('visibility', 'visible');
        $('.spinner-wrapper').css('opacity', '0');
        $('.spinner-wrapper').css('visibility', 'hidden');
    }

    // Show the spinner when the page is loading
    $(window).on('load', function () {
        hideSpinner();
    });

    // Show the spinner when the document is loading
    $(document).ajaxStart(function () {
        showSpinner();
    });

    // Hide the spinner when the document has finished loading
    $(document).ajaxStop(function () {
        hideSpinner();
    });

    // Example of triggering the spinner manually
    $('form').on('submit', function (event) {
        showSpinner();
    });

    // Show the spinner when the page is reloading
    $(window).on('beforeunload', function () {
        showSpinner();
    });

});

$(document).ready(function () {

    $(window).scroll(function () {
        if ($(this).scrollTop() > 100) {
            $('#scrollToTopBtn').fadeIn();
        } else {
            $('#scrollToTopBtn').fadeOut();
        }
    });

    $('#scrollToTopBtn').click(function () {
        $('html, body').animate({
            scrollTop: 0
        }, 'slow');
        return false;
    });
})

$(document).ready(function () {
    $('#password').keyup(function () {
        if ($('#password').val() == '') {
            $('#eye').css('visibility', 'hidden');
        } else {
            $('#eye').css('visibility', 'visible');
        }
    });

    // Add click event listener to #eye element
    $('#eye').click(function () {
        if ($('#password').attr('type') == 'password') {
            $('#password').attr('type', 'text');
            $('#eye').removeClass('fa-eye').addClass('fa-eye-slash');
        } else {
            $('#password').attr('type', 'password');
            $('#eye').removeClass('fa-eye-slash').addClass('fa-eye');
        }
    });
});

const tooltipTriggerList = document.querySelectorAll('[data-bs-toggle="tooltip"]')
const tooltipList = [...tooltipTriggerList].map(tooltipTriggerEl => new bootstrap.Tooltip(tooltipTriggerEl))