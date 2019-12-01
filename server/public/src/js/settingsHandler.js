import $ from "jquery";
import * as servCon from "./serverConnector";
import * as gui from "./gui";

export function initSettings() {
    const url = '/get_user_settings';
    servCon.getData(url, (cb) => {
        const jsonCB = JSON.parse(cb.responseText);
        const email = jsonCB['email'];
        const emailOption = jsonCB['2FA-Mail'];
        const appOption = jsonCB['2FA-App'];
        $('#email-address').val(email);
        if (appOption || emailOption) {
            $('#2-fa').prop('checked', true);
            $('#2-fa-email').prop('checked', emailOption);
            $('#2-fa-app').prop('checked', appOption);
        } else {
            $('#2-fa').prop('checked', false);
            gui.enableGrayOverlay($('#2-fa-options-wrapper'));
        }
    });
}

export function saveAccInfo() {
    if (confirm('Do you want to save your account-info?')) {
        const url = '/update_account_info';
        const email = $('#email-address').val();
        const password = $('#create_password').val();
        const data = {
            email: email,
            password: password
        };
        servCon.postRequestWithData(url, data, (cb) => {
            if (cb.responseText === '') {
                gui.changeNotificationTextAndOpen('You didnt change your account-info');
            } else {
                gui.changeNotificationTextAndOpen(cb.responseText);
            }
        });
    }
}

export function saveSettings() {
    if (confirm('Do you want to save your settings?')) {
        const url = '/update_settings_sec_fa';
        const sec_fa = $('#2-fa').prop('checked');
        const sec_fa_email = $('#2-fa-email').prop('checked');
        const sec_fa_app = $('#2-fa-app').prop('checked');
        const data = {
            sec_fa: sec_fa,
            sec_fa_email: sec_fa_email,
            sec_fa_app: sec_fa_app
        };
        servCon.postRequestWithData(url, data, (cb) => {
            gui.changeNotificationTextAndOpen(cb.responseText);
        });
    }
}
