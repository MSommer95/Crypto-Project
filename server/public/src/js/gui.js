import $ from 'jquery';
import * as eventHandler from './eventHandler';
import savePng from '../img/baseline_save_black_18dp.png';
import deletePng from '../img/baseline_delete_forever_black_18dp.png';
import locked from '../img/baseline_lock_black_18dp.png';
import unlocked from '../img/baseline_lock_open_black_18dp.png';
import downloadPng from '../img/baseline_cloud_download_black_18dp.png';
import encryptedFile from '../img/encrypted-file.png';
import pdfFile from '../img/baseline_picture_as_pdf_black_18dp.png';
import videoFile from '../img/baseline_videocam_black_18dp.png';
import imageFile from '../img/baseline_insert_photo_black_18dp.png';
import musicFile from '../img/baseline_queue_music_black_18dp.png';
import docFile from '../img/file.png';
import * as th from "./tableHelper";


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

export const previewIcon = (cell, formatterParams, onRendered) => {
    const icon = new Image();
    const fileExtension = th.preparePreview(cell);
    const documentExtension = ['txt', 'doc', 'docx', 'odt', 'rtf'];
    const musicExtensions = ['mp3', 'ogg', 'wav'];
    const videoExtensions = ['mp4', 'avi', 'flv', 'wmv'];
    const imageExtensions = ['jpg', 'jpeg', 'png', 'gif', 'svg'];
    if (documentExtension.includes(fileExtension)) {
        icon.src = docFile;
    } else if (musicExtensions.includes(fileExtension)) {
        icon.src = musicFile;
    } else if (videoExtensions.includes(fileExtension)) {
        icon.src = videoFile;
    } else if (imageExtensions.includes(fileExtension)) {
        icon.src = imageFile;
    } else if ('pdf' === fileExtension) {
        icon.src = pdfFile;
    } else if ('encrypted' === fileExtension) {
        icon.src = encryptedFile;
    }
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

export function validateEmail(email, emailField) {
    const emailRegExp = /^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)*$/;
    if (emailRegExp.test(email)) {
        emailField[0].setCustomValidity('');
        return true
    } else {
        emailField[0].setCustomValidity('Please confirm that the email has the correct format.');
        return false
    }
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

function switchUI(elementsToShow, elementsToHide) {
    elementsToShow.forEach(element => showElement(element));
    elementsToHide.forEach(element => hideElement(element))
}

export function toggleSettings(element) {
    const elementsMainPage = [$('#hash-message-section'), $('#device-section'), $('#otp-section'), $('#file-section')];
    const elementsSettings = [$('#settings-section')];
    if (element.id === 'settings-btn') {
        switchUI(elementsSettings, elementsMainPage);
    } else {
        switchUI(elementsMainPage, elementsSettings);
    }
}

export function toggleCipherDisplay(element) {
    if (element.value === 'Caesar Cipher') {
        hideElement($('#vigenere_card-body'));
        hideElement($('#vigenere_card-footer'));
        showElement($('#caesar_card-body'));
        showElement($('#caesar_card-footer'));
    } else {
        hideElement($('#caesar_card-body'));
        hideElement($('#caesar_card-footer'));
        showElement($('#vigenere_card-body'));
        showElement($('#vigenere_card-footer'));
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

export function activatePopovers() {
    $('[data-toggle="popover"]').popover();
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

$('#secure_password-copy').on('shown.bs.popover', function() {
    setTimeout(function() {
        $('#secure_password-copy').popover('hide');
    }, 2000);
});



document.addEventListener('click', eventHandler.onMouseClick, false);
document.addEventListener('change', eventHandler.onStateChange, false);
document.addEventListener('input', eventHandler.onInput, false);
