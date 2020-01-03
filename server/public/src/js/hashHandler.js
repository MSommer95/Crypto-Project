import $ from 'jquery';
import * as servCon from "./serverConnector";
import * as authHandler from "./authHandler";


export function requestHashing() {
    const url = '/hash_message';
    const data = {
        hash_function: $('#hash-function').val(),
        message: $('#hash-message').val(),
        auth_token: authHandler.getTokenFromField()
    };
    servCon.postRequestWithData(url, data, (cb) => {
        $('#hashed-message').val(cb.responseJSON.message);
    });
}

export function requestCaesarEncryption() {
    const url = '/caesar_cipher';
    const data = {
        message: $('#caesar_plaintext-message').val(),
        shift: $('#caesar_shift-encrypt').val(),
        option: 'encrypt',
        auth_token: authHandler.getTokenFromField()
    };
    servCon.postRequestWithData(url, data, (cb) => {
        $('#caesar_cipher-message').val(cb.responseJSON.message);
    });
}

export function requestCaesarDecrypion() {
    const url = '/caesar_cipher';
    const data = {
        message: $('#caesar_cipher-message').val(),
        shift: $('#caesar_shift-decrypt').val(),
        option: 'decrypt',
        auth_token: authHandler.getTokenFromField()
    };
    servCon.postRequestWithData(url, data, (cb) => {
        $('#caesar_plaintext-message').val(cb.responseJSON.message);
    });
}

export function requestCaesarCrack() {
    const url = '/caesar_cipher_crack';
    const data = {
        message: $('#caesar_cipher-message').val(),
        auth_token: authHandler.getTokenFromField()
    };
    servCon.postRequestWithData(url, data, (cb) => {
        $('#caesar_shift-decrypt').val(cb.responseJSON.message);
        $('#caesar_decrypt-message-btn').click();
    });
}

export function requestVigenereEncryption() {
    const url = '/vigenere_cipher';
    const data = {
        message: $('#vigenere_plaintext-message').val(),
        key: $('#vigenere_key-encrypt').val(),
        option: 'encrypt',
        auth_token: authHandler.getTokenFromField()
    };
    servCon.postRequestWithData(url, data, (cb) => {
        $('#vigenere_cipher-message').val(cb.responseJSON.message);
    });
}

export function requestVigenereDecrypion() {
    const url = '/vigenere_cipher';
    const data = {
        message: $('#vigenere_cipher-message').val(),
        key: $('#vigenere_key-decrypt').val(),
        option: 'decrypt',
        auth_token: authHandler.getTokenFromField()
    };
    servCon.postRequestWithData(url, data, (cb) => {
        $('#vigenere_plaintext-message').val(cb.responseJSON.message);
    });
}

export function requestVigenereCrack() {
    const url = '/vigenere_cipher_crack';
    const data = {
        message: $('#vigenere_cipher-message').val(),
        auth_token: authHandler.getTokenFromField()
    };
    servCon.postRequestWithData(url, data, (cb) => {
        $('#vigenere_key-decrypt').val(cb.responseJSON.message);
        $('#vigenere_decrypt-message-btn').click();
    });
}

