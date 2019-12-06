import $ from 'jquery';
import * as gui from './gui';
import * as passGen from './passwordGenerator';
import * as settHandler from './settingsHandler';
import * as qrGen from './qrGenerator';
import * as authHandler from './authHandler';


export function onMouseClick(event) {
    switch (event.target.id) {
        case 'back-to-top':
            gui.scrollToTop();
            break;
        case 'upload-file-btn':
            $('#upload-file-close-btn').click();
            break;
        case 'files-table-btn-upload':
            $('#upload-file-popup').modal();
            break;
        case 'reset-settings-btn':
            $('#otp-close').click();
            $('#settings-reset-popup').modal();
            break;
        case 'back-to-main-btn':
            gui.toggleSettings(event.target);
            break;
        case 'settings-btn':
            gui.toggleSettings(event.target);
            break;
        case 'file_nav-btn':
            gui.scrollToElement($('#file-section'));
            break;
        case 'otp_nav-btn':
            gui.scrollToElement($('#otp-section'));
            break;
        case 'device_nav-btn':
            gui.scrollToElement($('#device-section'));
            break;
        case 'secure_password-copy':
            passGen.copyPassword();
            break;
        case 'secure_password-generate-btn':
            passGen.initiatePasswordGen();
            break;
        case 'registrationButton':
            gui.switchLoginCreate(event.target);
            break;
        case 'loginButton':
            gui.switchLoginCreate(event.target);
            break;
        case 'account_info-save-btn':
            settHandler.saveAccInfo();
            break;
        case 'settings-save-btn':
            settHandler.saveSettings();
            break;
        case 'open-password-generator-btn':
            passGen.openPassGen();
            break;
        case 'reg-device-btn':
            qrGen.toggleQRGen();
            break;
        case 'send_login-btn':
            authHandler.login();
            break;
        case 'logout-btn':
            authHandler.logout();
            break;
        case 'send_otp':
            authHandler.sendOTP();
            break;
        case 'send_reset-code':
            authHandler.sendResetCode();
            break;
        case 'reset-password-link':
            authHandler.openPasswordResetPopup();
            break;
        case 'request_password-reset-code':
            authHandler.requestPasswordReset();
            break;
        case 'open_new-password-passgen':
            passGen.openPassGen();
            break;
        case 'send_password-reset-code':
            authHandler.sendPasswordResetCode();
            break;
        case 'send_new-password':
            authHandler.sendNewPassword();
            break;
        default:
            break;
    }
}

export function onStateChange(event) {
    switch (event.target.id) {
        case 'file-upload-input':
            gui.filenameExtract(event.target);
            break;
        case '2-fa':
            gui.secfacStateChange(event.target);
            break;
        case 'secure_password-pwd':
            passGen.passInputchange(event.target);
            break;
        default:
            break;
    }
}

export function onInput(event) {
    switch (event.target.id) {
        case 'secure_password-length_slider':
            passGen.changeRangeInputVal();
            break;
        case 'secure_password-length_input':
            passGen.changeRangeSliderVal();
            break;
        default:
            break;
    }
}