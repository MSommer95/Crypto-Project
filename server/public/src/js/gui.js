import $ from 'jquery';
import savePng from "../img/baseline_save_black_18dp.png";
import deletePng from "../img/baseline_delete_forever_black_18dp.png";

export const saveIcon = (cell, formatterParams, onRendered) => {
    const icon = new Image();
    icon.src = savePng;
    icon.height = 32;
    icon.width = 32;
    return icon
};
export const deleteIcon = (cell, formatterParams, onRendered) => {
    const icon = new Image();
    icon.src = deletePng;
    icon.height = 32;
    icon.width = 32;
    return icon
};

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

export function changeNotificationTextAndOpen(text) {
    $('#notification-text').text(text);
    $('#notification-popup').modal();
}

$('.custom-file-input').on('change', function () {
    const fileName = $(this).val().split('\\').pop();
    $(this).siblings('.custom-file-label').addClass('selected').html(fileName);
});
$('#otp-popup').on('shown.bs.modal', function () {
    $('#confirm_otp').trigger('focus');
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


