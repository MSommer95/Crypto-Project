

$(document).ready(function () {

    $('#send_login-btn').on('click', function (btn) {

        let url = '/sign_in';
        let data = {



        };

    });

});


// Get Funktion für die Server-Datenbank Abfragen
function getDBData(url, cb) {
    $.ajax({
        type: 'GET',
        url: url,
        complete: function (jqXHR) {
            cb(jqXHR.responseJSON);
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
            cb(jqXHR.responseJSON);
        }
    });
}