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
