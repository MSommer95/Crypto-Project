import $ from 'jquery';
import * as servCon from './serverConnector';
import * as gui from './gui';
import {getTokenFromField} from './authHandler';

export function initSettings() {
    if (!$('#2-fa-status').is(':checked')) {
        gui.enableGrayOverlay($('#2-fa-options-wrapper'));
    }
}

export function saveAccInfo() {
    if (confirm('Do you want to save your account-info?')) {
        const url = '/update_account_info';
        const email = $('#email-address').val();
        const password = $('#create_password').val();
        const oldPassword = $('#old_password').val();
        const data = {
            email: email,
            password: password,
            old_password: oldPassword,
            auth_token: getTokenFromField()
        };
        servCon.postRequestWithData(url, data, (cb) => {
            if (cb.responseJSON.message === '') {
                gui.changeNotificationTextAndOpen('You didnt change your account-info');
            } else {
                gui.changeNotificationTextAndOpen(cb.responseJSON.message);
            }
        });
    }
}

export function saveSettings() {
    if (confirm('Do you want to save your settings?')) {
        const url = '/update_settings_sec_fa';
        const sec_fa = $('#2-fa-status').prop('checked');
        const sec_fa_email = $('#2-fa-email').prop('checked');
        const sec_fa_app = $('#2-fa-app').prop('checked');
        const data = {
            sec_fa: sec_fa,
            sec_fa_email: sec_fa_email,
            sec_fa_app: sec_fa_app,
            auth_token: getTokenFromField()
        };
        servCon.postRequestWithData(url, data, (cb) => {
            if (cb.responseJSON.message.includes('No active device found!')) {
                $('#device-register-text-popup').modal();
            } else {
                gui.changeNotificationTextAndOpen(cb.responseJSON.message);
            }
        });
    }
}

export function updateSettings(settings) {
    if (settings['2FA-Mail'] === 0 && settings['2FA-App'] === 0){
        gui.enableGrayOverlay($('#2-fa-options-wrapper'));
        $('#2-fa-status').prop('checked', false);
        $('#2-fa-email').prop('checked', false);
        $('#2-fa-app').prop('checked', false);
    } else {
        gui.disableGrayOverlay($('#2-fa-options-wrapper'));
        $('#2-fa-status').prop('checked', true);
        $('#2-fa-email').prop('checked', settings['2FA-Mail']);
        $('#2-fa-app').prop('checked', settings['2FA-App']);

    }
}
