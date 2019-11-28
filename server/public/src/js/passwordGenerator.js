import $ from 'jquery';
import * as servConn from "./serverConnector";

let topPasswords = '';

servConn.getData('/request_top_password', (cb) => {
   topPasswords = cb.responseText;
});

function puncuateNumber(number) {
    return number.toLocaleString()
}

function checkIfPasswordContainsChar(password, string) {
    let contains = false;
    for (let i = 0; i < string.length; i += 1) {
        if (password.includes(string[i])) {
            contains = true;
            break;
        }
    }
    return contains
}

function checkIfTopPasswordIsSubstring(password) {
    const topPasswordList = topPasswords.split('\n');
    const subString = topPasswordList.filter((subString) => (password.includes(subString)));
    subString.sort(function(a, b) {
        if (a.length >= b.length) {
            return -1
        } else {
            return 1
    }
    });
    return subString
}

function changeRankDisplay(timeInDaysToCrack) {
    let passwordRank = 'High';
    const passwordRankPTag = $('#password-rank');
    const passwordBruteForceDisplay = $('#brute-force-days');
    if (timeInDaysToCrack >= 1000000) {
        console.log(`High rank: ${timeInDaysToCrack}`);
        passwordRank = 'High';
        passwordRankPTag.css('color', '#007F00');
    } else if (timeInDaysToCrack >= 1000) {
        console.log(`Medium rank: ${timeInDaysToCrack}`);
        passwordRank = 'Medium';
        passwordRankPTag.css('color', '#EFAF00');
    } else {
        console.log(`Low rank: ${timeInDaysToCrack}`);
        passwordRank = 'Low';
        passwordRankPTag.css('color', '#F90000');
    }
    passwordBruteForceDisplay.text(puncuateNumber(timeInDaysToCrack));
    passwordRankPTag.text(`${passwordRank}`);
}

function calculatePasswordRank(password) {
    const lowerCaseLetters = 'abcdefghijklmnopqrstuvwxyz';
    const upperCaseLetters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ';
    const digits = '0123456789';
    const specialCharacters = '!§$%&*+#üäöÜÄÖ';
    let numberOfCharacters = 0;
    const subStringPassword = checkIfTopPasswordIsSubstring(password)[0];
    const regEx = new RegExp(subStringPassword, 'g');
    password = password.replace(regEx, '') ;
    if (checkIfPasswordContainsChar(password, lowerCaseLetters)) {
        numberOfCharacters += lowerCaseLetters.length;
    }
    if (checkIfPasswordContainsChar(password, upperCaseLetters)) {
        numberOfCharacters += upperCaseLetters.length;
    }
    if (checkIfPasswordContainsChar(password, digits)) {
        numberOfCharacters += digits.length;
    }
    if (checkIfPasswordContainsChar(password, specialCharacters)) {
        numberOfCharacters += specialCharacters.length;
    }
    const passwordLength = password.length;
    const complexity = Math.pow(numberOfCharacters, passwordLength);
    const attemptsPerSec = 50000000000;
    let timeInDaysToCrack = complexity / attemptsPerSec / 3600 / 24;

    if (topPasswords.includes(password)) {
        timeInDaysToCrack = 0;
    }
    changeRankDisplay(timeInDaysToCrack);
}

export function generatePassword(lower, upper, digit, special, length) {
    let combinedString = '';
    let password = '';
    const lowerCaseLetters = 'abcdefghijklmnopqrstuvwxyz';
    const upperCaseLetters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ';
    const digits = '0123456789';
    const specialCharacters = '!§$%&*+#üäöÜÄÖ';
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
    calculatePasswordRank(password);
    return password
}

$('#secure_password-generate-btn').on('click', () => {
    const lowerCase = $('#secure_password-letters_lower').prop('checked');
    const upperCase = $('#secure_password-letters_upper').prop('checked');
    const digits = $('#secure_password-digits').prop('checked');
    const special = $('#secure_password-special_chars').prop('checked');
    const length = $('#secure_password-length_input').val();
    const password = generatePassword(lowerCase, upperCase, digits, special, length);
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

$('#secure_password-pwd').on('change', function() {
    calculatePasswordRank(this.value);
    $('#secure_password-length_slider').val(this.value.length);
    $('#secure_password-length_input').val(this.value.length);
});