import $ from 'jquery';
import * as authHandler from './authHandler';

export function getData(url, cb) {
    $.ajax({
        type: 'GET',
        url: url,
        complete: function (jqXHR) {
            cb(jqXHR);
        }
    });
}

export function postRequestWithData(url, data, cb) {
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

export function requestFile(url, fileID, method) {
    let filepathInput = '<input type="hidden" name="file_id" value="' + fileID + '" />';
    let tokenInput = '<input type="hidden" name="auth_token" value="' + authHandler.getTokenFromField() + '" />';
    $('<form action="' + url + '" method="' + (method || 'post') + '">' + filepathInput + tokenInput + '</form>')
        .appendTo('body').submit().remove();
}
