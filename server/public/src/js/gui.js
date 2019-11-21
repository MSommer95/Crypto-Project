import $ from 'jquery';

export function showElement(element) {
    $(element).removeClass('hidden');
}

export function hideElement(element) {
    $(element).addClass('hidden');
}

export function chooseNavbar(button) {

    const hotpDiv = $('#hotp-section');
    const fileDiv = $('#file-section');
    const aboutDiv = $('#about-section');
    const settingDiv = $('#setting-section');
    const logoutDiv = $('#logout-section');

    // Anzeigen/ausblenden der entsprechenden Container
    switch (button.id) {
        case 'hotpButton':
            showElement(hotpDiv);
            showElement(fileDiv);
            hideElement(aboutDiv);
            hideElement(settingDiv);
            hideElement(logoutDiv);
            break;
        case 'fileButton':
            hideElement(hotpDiv);
            showElement(fileDiv);
            hideElement(aboutDiv);
            hideElement(settingDiv);
            hideElement(logoutDiv);
            break;
        case 'aboutButton':
            hideElement(hotpDiv);
            hideElement(fileDiv);
            showElement(aboutDiv);
            hideElement(settingDiv);
            hideElement(logoutDiv);
            break;
        case 'settingButton':
            hideElement(hotpDiv);
            hideElement(fileDiv);
            hideElement(aboutDiv);
            showElement(settingDiv);
            hideElement(logoutDiv);
            break;
        case 'logoutButton':
            hideElement(hotpDiv);
            hideElement(fileDiv);
            hideElement(aboutDiv);
            hideElement(settingDiv);
            showElement(logoutDiv);
            break;
    }
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

$(".custom-file-input").on("change", function () {
    const fileName = $(this).val().split("\\").pop();
    $(this).siblings(".custom-file-label").addClass("selected").html(fileName);
});
$('#otp-popup').on('shown.bs.modal', function () {
    $('#confirm_otp').trigger('focus')
});
$('#hotpButton').on('click', function () {
    chooseNavbar(this);
});
$('#fileButton').on('click', function () {
    chooseNavbar(this);
});
$('#aboutButton').on('click', function () {
    chooseNavbar(this);
});
$('#settingButton').on('click', function () {
    chooseNavbar(this);
});
$('#logoutButton').on('click', function () {
    chooseNavbar(this);
});