import {chooseLogin, hideElement, showElement} from "./gui";
import * as servCon from './serverConnector';
import {generatePassword} from "./passwordGenerator";
import $ from 'jquery/dist/jquery.min';

import '../css/bootstrap.css'
import '../css/custom.css'
import '../css/main.css'

function request_2fa_verified() {
    servCon.getDBData('/check_otp_verified', (cb) => {
        if (cb.responseText === '0') {
            setTimeout(request_2fa_verified, 5000);
        } else {
            window.location.href = '/index';
        }
    });
}

$('#send_otp').on('click', () => {
    let otp = $('#confirm_otp').val();
    if (otp != null) {
        let url = '/verify_otp';
        let data = {
            otp: otp
        };
        servCon.postDBData(url, data, (cb) => {
            console.log(cb.responseText);

            if (cb.responseText.includes('Varification valid')) {
                window.location.href = '/index';
            } else {
                alert('You entered the wrong HOTP or the time expired, please login again');
            }
        });
    }
});



$('#send_login-btn').on('click', () => {
    let url = '/login_account';
    let data = {
        email: $('#login_email').val(),
        password: $('#login_password').val()
    };
    servCon.postDBData(url, data, (cb) => {
        if (cb.responseText.includes('HOTP')) {
            showElement($('#otp-popup'));
            setTimeout(request_2fa_verified, 5000);
        } else if (cb.responseText.includes('index')) {
            window.location.href = '/index'
        } else if (cb.responseText.includes('sign')) {
            window.location.href = '/sign'
        }
    });
});

$('#secure_password-generator').on('click', () => {
    showElement($('#secure_password-popup'));
    let password = generatePassword(true, true, true, true, 16);
    $('#secure_password-pwd').val(password);
    $('#create_password').val(password);
});

$('#close-btn_otp-popup').on('click', (button) => {
    hideElement($('#otp-popup'));
});

$('#registrationButton').on('click', function () {
    chooseLogin(this);
});

$('#loginButton').on('click', function () {
    chooseLogin(this);
});