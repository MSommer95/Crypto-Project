import $ from 'jquery/dist/jquery.min';

// Get Funktion für die Server-Datenbank Abfragen
export function getDBData(url, cb) {
    $.ajax({
        type: 'GET',
        url: url,
        complete: function (jqXHR) {
            cb(jqXHR);
        }
    });
}

// Post Funktion für die Server-Datenbank Abfragen
export function postDBData(url, data, cb) {
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