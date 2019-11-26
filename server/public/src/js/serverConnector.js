import $ from 'jquery';

// Get Funktion für die Server(-Datenbank) Abfragen
export function getData(url, cb) {
    $.ajax({
        type: 'GET',
        url: url,
        complete: function (jqXHR) {
            cb(jqXHR);
        }
    });
}

// Post Funktion für die Server-Datenbank Abfragen
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

export function requestFile(url, filepath, method) {
    let inputs = '<input type="hidden" name="file_path" value="' + filepath + '" />';
    //send request
    $('<form action="' + url + '" method="' + (method || 'post') + '">' + inputs + '</form>')
        .appendTo('body').submit().remove();
}
