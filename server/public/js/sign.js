$('#send_login-btn').on('click', () => {
    let url = '/login_account';
    let data = {
        email: $('#login_email').val(),
        password: $('#login_password').val()
    };
    postDBData(url, data, (cb) => {
        if (cb.responseText.includes('HOTP')) {
            showElement($('#otp-container'));
            setTimeout(request_2fa_verified, 5000);
        } else if (cb.responseText.includes('index')) {
            window.location.href = '/index'
        } else if (cb.responseText.includes('sign')) {
            window.location.href = '/sign'
        }
    });

});

function generatePassword(lower, upper, digit, special, length) {
    let combinedString = '';
    let password = '';
    let lowerCaseLetters = 'abcdefghijklmnopqrstuvwxyz';
    let upperCaseLetters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ';
    let digits = '0123456789';
    let specialCharacters = '!§$%&*+#üäöÜÄÖ';

    if (lower) {
        combinedString += lowerCaseLetters;
    }
    if (upper) {
        combinedString += upperCaseLetters;
    }
    if (digit) {
        combinedString += digits;
    }
    if (special) {
        combinedString += specialCharacters;
    }

    let array = new Uint32Array(length);
    window.crypto.getRandomValues(array);

    for (let i = 0; i < array.length; i += 1) {
        const randomNum = array[i] % combinedString.length;
        password += combinedString.substring(randomNum, randomNum + 1);
    }

    return password
}


$('#send_otp').on('click', () => {
    let otp = $('#confirm_otp').val();
    if (otp != null) {
        let url = '/verify_otp';
        let data = {
            otp: otp
        };
        postDBData(url, data, (cb) => {
            console.log(cb.responseText);

            if(cb.responseText.includes('Varification valid')) {
                window.location.href = '/index';
            }
            else {
                alert('You entered the wrong HOTP or the time expired, please login again');
            }
        });
    }
});

function request_2fa_verified() {
    getDBData('/check_otp_verified', (cb) => {
        if(cb === '0') {
            setTimeout(request_2fa_verified, 5000);
        } else {
            window.location.href = '/index';
        }
    });
}

// Get Funktion für die Server-Datenbank Abfragen
function getDBData(url, cb) {
    $.ajax({
        type: 'GET',
        url: url,
        complete: function (jqXHR) {
            cb(jqXHR.responseText);
        }
    });
}

// Post Funktion für die Server-Datenbank Abfragen
function postDBData(url, data, cb) {
    $.ajax({
        type: 'POST',
        enctype: 'multipart/form-data',
        url: url,
        data: data,
        dataType: 'json',
        complete: function (jqXHR) {
            cb(jqXHR);
        }
    });
}

$('#secure_password-generator').on('click', () => {
    showElement($('#secure_password-popup'));
    let password = generatePassword(true, true, true, true, 16);
    $('#secure_password-pwd').val(password);
    $('#create_password').val(password);
});

$('#secure_password-generate-btn').on('click', () => {
    let lowerCase = $('#secure_password-letters_lower').prop('checked');
    let upperCase = $('#secure_password-letters_upper').prop('checked');
    let digits = $('#secure_password-digits').prop('checked');
    let special = $('#secure_password-special_chars').prop('checked');
    let length = $('#secure_password-length_input').val();
    let password = generatePassword(lowerCase, upperCase, digits, special, length);
    $('#secure_password-pwd').val(password);
    $('#create_password').val(password);
});

$('#secure_password-copy').on('click', () => {
    let password = $('#secure_password-pwd');
    password.select();
    document.execCommand('copy');
});

$('#secure_password-length_slider').on('input', ()=>{
    let rangeVal = $('#secure_password-length_slider').val();
    $('#secure_password-length_input').val(rangeVal);
    console.log(`Change range Val: ${rangeVal}`);
});

$('#secure_password-length_input').on('input', ()=>{
    let inputVal = $('#secure_password-length_input').val();
    $('#secure_password-length_slider').val(inputVal);
    console.log(`Change input Val: ${inputVal}`);
});

// show function
function showElement(element) {
    $(element).removeClass('hidden');
}

// hide function
function hideElement(element) {
    $(element).addClass('hidden');
}