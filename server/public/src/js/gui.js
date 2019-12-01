import $ from 'jquery';
import * as eventHandler from './eventHandler';
import savePng from "../img/baseline_save_black_18dp.png";
import deletePng from "../img/baseline_delete_forever_black_18dp.png";
import locked from "../img/baseline_lock_black_18dp.png";
import unlocked from "../img/baseline_lock_open_black_18dp.png";
import downloadPng from "../img/baseline_cloud_download_black_18dp.png";

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

export const encryptIcon = (cell, formatterParams, onRendered) => {
    const icon = new Image();
    icon.height = 32;
    icon.width = 32;
    if (cell.getRow().getData().is_encrypted) {
        icon.src = locked;
    } else {
        icon.src = unlocked;
    }
    return icon
};
export const downloadIcon = (cell, formatterParams, onRendered) => {
    const icon = new Image();
    icon.src = downloadPng;
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

// scroll body to 0px on click
export function scrollToTop() {
    $('body,html').animate({
        scrollTop: 0
    }, 800);
    return false;
}

export function scrollToElement(element) {
    $('html, body').animate({scrollTop: element.offset().top}, 1000);
}

export function enableGrayOverlay(element) {
    $(element).addClass('disabled-div');
    $('#2-fa-email').attr('disabled', true);
    $('#2-fa-app').attr('disabled', true);
}

export function disableGrayOverlay(element) {
    $(element).removeClass('disabled-div');
    $('#2-fa-email').attr('disabled', false);
    $('#2-fa-app').attr('disabled', false);
}

export function switchLoginCreate(button) {
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

export function toggleSettings(element) {
    const deviceElement = $('#device-section');
    const otpElement = $('#otp-section');
    const fileElement = $('#file-section');
    const settingsElement = $('#settings-section');
    switch (element.id) {
        case 'settings-btn':
            hideElement(deviceElement);
            hideElement(otpElement);
            hideElement(fileElement);
            showElement(settingsElement);
            break;
        case 'back-to-main-btn':
            showElement(deviceElement);
            showElement(otpElement);
            showElement(fileElement);
            hideElement(settingsElement);
            break;
    }
}

export function filenameExtract(input) {
    const fileName = $(input).val().split('\\').pop();
    $('#file-upload-label').addClass('selected').html(fileName);
}

export function secfacStateChange(checkbox) {
    if (checkbox.checked) {
       disableGrayOverlay($('#2-fa-options-wrapper'));
   } else {
       enableGrayOverlay($('#2-fa-options-wrapper'));
   }
}

$('#otp-popup').on('shown.bs.modal', function () {
    $('#confirm_otp').trigger('focus');
});

$(window).scroll(function () {
    if ($(this).scrollTop() > 50) {
        $('#back-to-top').fadeIn();
    } else {
        $('#back-to-top').fadeOut();
    }
});

document.addEventListener('click', eventHandler.onMouseClick, false);
document.addEventListener('change', eventHandler.onStateChange, false);
document.addEventListener('input', eventHandler.onInput, false);
