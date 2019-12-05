import $ from "jquery";
import * as servCon from "./serverConnector";
import * as gui from "./gui";

let authToken = '';

function request_2fa_verified(token) {
    const url = '/check_otp_verified';
    const data = {
      auth_token: token
    };
    servCon.postRequestWithData(url, data, (cb) => {
        if (cb.responseText === '0') {
            setTimeout(request_2fa_verified, 5000, token);
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
        if (cb.responseJSON.message.includes('OTP')) {
            authToken = cb.responseJSON.token;
            $('#otp-popup').modal();
            $('#request-new-otp-btn').on('click', () => {
                const url = '/request_new_otp';
                const data = {
                    auth_token: authToken
                };
                servCon.postRequestWithData(url, data, (cb) => {
                });
            });
            setTimeout(request_2fa_verified, 5000, authToken);
        } else if (cb.responseJSON.message.includes('index')) {
            window.location.href = '/index'
        } else {
            gui.changeNotificationTextAndOpen(cb.responseJSON.message);
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
            otp: otp,
            auth_token: authToken
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

export function openPasswordResetPopup() {
    $('#password-reset-popup').modal();
}

export function requestPasswordReset() {
    const url = '/request_password_reset';
    if ($('#input_password-reset-email').val() !== '') {
        const data = {
          email: $('#input_password-reset-email').val()
        };
        servCon.postRequestWithData(url, data, (cb) => {
            gui.changeNotificationTextAndOpen(cb.responseText)
        });
    } else {
        gui.changeNotificationTextAndOpen('Please insert your Email Address')
    }
}

export function sendPasswordResetCode() {
    const url = '/password_reset';
    if ($('#input_password-reset-email').val() !== '') {
        const token = $('#input_password-reset-code').val();
        const email = $('#input_password-reset-email').val();
        const data = {
            token: token,
            email: email
        };
        servCon.postRequestWithData(url, data, (cb) => {
            if (cb.responseText === 'valid token') {
                $('#password-reset-close').click();
                $('#new-password-popup').modal();
                $('#new-password-email-input').val(email);
                $('#new-password-token-input').val(token);
            }
        });
    } else {
        gui.changeNotificationTextAndOpen('Please insert your Email Address')
    }
}

export function sendNewPassword() {
    const url = '/new_password';
    const data = {
        password: $('#new-password-input').val(),
        token: $('#new-password-token-input').val(),
        email: $('#new-password-email-input').val()
    };
    servCon.postRequestWithData(url, data, (cb) => {
        if (cb.responseText === 'Successfully updated password') {
            gui.changeNotificationTextAndOpen(cb.responseText);
        } else {
            $('#new-password-close').click();
            gui.changeNotificationTextAndOpen(cb.responseText);
        }
    });
}

export async function getTokenFromServer() {
    const response = await fetch('/get_auth_token');
    await response.text().then(function (text) {
        $('#hidden-token').val(text)
    });

}

export function getTokenFromField() {
    return $('#hidden-token').val();
}
