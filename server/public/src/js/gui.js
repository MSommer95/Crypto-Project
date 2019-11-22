import $ from 'jquery';

export function showElement(element) {
    $(element).removeClass('hidden');
}

export function hideElement(element) {
    $(element).addClass('hidden');
}

export function scrollToID(element) {
    $('html, body').animate({scrollTop: element.offset().top}, 1000);
}

export function chooseLogin(button) {

    const registrationDiv = $('#registration-section');
    const loginDiv = $('#login-section');

    // Anzeigen/ausblenden der entsprechenden Container
    switch (button.id) {
        case 'registrationButton':
            showElement(registrationDiv);
            hideElement(loginDiv);
            break;
        case 'loginButton':
            hideElement(registrationDiv);
            showElement(loginDiv);
            break;
    }
}

$('.custom-file-input').on('change', function () {
    const fileName = $(this).val().split('\\').pop();
    $(this).siblings('.custom-file-label').addClass('selected').html(fileName);
});
$('#otp-popup').on('shown.bs.modal', function () {
    $('#confirm_otp').trigger('focus')
});
$('#device_nav-btn').on('click', function () {
    scrollToID($('#device-section'));
});
$('#otp_nav-btn').on('click', function () {
    scrollToID($('#otp-section'));
});
$('#file_nav-btn').on('click', function () {
    scrollToID($('#file-section'));
});
$(window).scroll(function () {
    if ($(this).scrollTop() > 50) {
        $('#back-to-top').fadeIn();
    } else {
        $('#back-to-top').fadeOut();
    }
});
// scroll body to 0px on click
$('#back-to-top').on('click', () => {
    $('body,html').animate({
        scrollTop: 0
    }, 800);
    return false;
});


