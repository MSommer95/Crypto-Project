import {chooseLogin, showElement} from "./gui";
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
            $('#otp-popup').modal();
            setTimeout(request_2fa_verified, 5000);
        } else if (cb.responseText.includes('index')) {
            window.location.href = '/index'
        } else if (cb.responseText.includes('sign')) {
            window.location.href = '/sign'
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
    chooseLogin(this);
});

$('#loginButton').on('click', function () {
    chooseLogin(this);
});
