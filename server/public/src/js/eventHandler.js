import * as gui from "./gui";
import $ from "jquery";


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
        default:
            break;
    }
}