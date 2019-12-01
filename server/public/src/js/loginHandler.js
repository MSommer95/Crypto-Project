import $ from "jquery";
import * as servCon from "./serverConnector";
import * as gui from "./gui";

function request_2fa_verified() {
    servCon.getData('/check_otp_verified', (cb) => {
        if (cb.responseText === '0') {
            setTimeout(request_2fa_verified, 5000);
        } else if(cb.responseText === 'Not logged in') {
            gui.changeNotificationTextAndOpen('Not logged in');
            window.location.href = '/sign';
        } else {
            window.location.href = '/index';
        }
    });
}

export function login() {
    let url = '/login_account';
    let data = {
        email: $('#login_email').val(),
        password: $('#login_password').val()
    };
    servCon.postRequestWithData(url, data, (cb) => {
        if (cb.responseText.includes('OTP')) {
            $('#otp-popup').modal();
            $('#request-new-otp-btn').on('click', () => {
                const url = '/request_new_otp';
                servCon.getData(url, (cb) => {
                });
            });
            setTimeout(request_2fa_verified, 5000);
        } else if (cb.responseText.includes('index')) {
            window.location.href = '/index'
        } else {
            gui.changeNotificationTextAndOpen(cb.responseText);
        }
    });
}

export function logout() {
    let url = '/logout_account';
    servCon.getData(url, (cb) => {
        console.log(cb.responseText);
        location.reload();
    });
}

export function sendOTP() {
    let otp = $('#confirm_otp').val();
    if (otp != null) {
        let url = '/verify_otp';
        let data = {
            otp: otp
        };
        servCon.postRequestWithData(url, data, (cb) => {
            console.log(cb.responseText);
            if (cb.responseText.includes('Verification valid')) {
                window.location.href = '/index';
            } else {
                gui.changeNotificationTextAndOpen('You entered the wrong OTP or the time expired, please login again.');
            }
        });
    }
}

export function sendResetCode() {
    const url = '/reset_settings_sec_fa';
    const data = {
        token: $('#confirm_reset-code').val()
    };
    servCon.postRequestWithData(url, data, (cb) => {
        gui.changeNotificationTextAndOpen(cb.responseText);
        if (cb.responseText === 'unauthorized') {
            $('#reset-close').click();
        }
    });
}
