import * as gui from "./gui";
import * as servCon from './serverConnector';
import {generatePassword} from "./passwordGenerator";
import $ from 'jquery';
import 'bootstrap/dist/css/bootstrap.min.css';
import 'bootstrap';
import '../css/custom.css';

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

$('#send_otp').on('click', () => {
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
});


$('#send_login-btn').on('click', () => {
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
});

$('#secure_password-generator').on('click', () => {
    $('#secure_password-popup').modal();
    let password = generatePassword(true, true, true, true, 16);
    $('#secure_password-pwd').val(password);
    $('#create_password').val(password);
});

$('#registrationButton').on('click', function () {
    gui.chooseLogin(this);
});

$('#loginButton').on('click', function () {
    gui.chooseLogin(this);
});
