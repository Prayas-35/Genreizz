$(document).ready(function() {
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
    $(window).on('load', function() {
        hideSpinner();
    });

    // Show the spinner when the document is loading
    $(document).ajaxStart(function() {
        showSpinner();
    });

    // Hide the spinner when the document has finished loading
    $(document).ajaxStop(function() {
        hideSpinner();
    });

    // Example of triggering the spinner manually
    $('form').on('submit', function(event) {
        showSpinner();
    });

    // Show the spinner when the page is reloading
    $(window).on('beforeunload', function() {
        showSpinner();
    });

});