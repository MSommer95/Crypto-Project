import $ from 'jquery/dist/jquery.min';

export function generatePassword(lower, upper, digit, special, length) {
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

$('#secure_password-length_slider').on('input', () => {
    let rangeVal = $('#secure_password-length_slider').val();
    $('#secure_password-length_input').val(rangeVal);
    console.log(`Change range Val: ${rangeVal}`);
});

$('#secure_password-length_input').on('input', () => {
    let inputVal = $('#secure_password-length_input').val();
    $('#secure_password-length_slider').val(inputVal);
    console.log(`Change input Val: ${inputVal}`);
});