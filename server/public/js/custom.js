$('#send_login-btn').on('click', () => {
    let url = '/login_account';
    let data = {
        email: $('#login_email').val(),
        password: $('#login_password').val()
    };
    postDBData(url, data, (cb) => {

    });

});

$('#decrypt-btn').on('click', () => {
    let url = '/file_decrypt';
    let data = {
        file_id: 1572687529258,
        filename: 'Tabellen-Differenzen.pdf'
    };
    postDBData(url, data, () => {

    });
});

$('#encrypt-btn').on('click', () => {
    let url = '/file_encrypt';
    let data = {
        file_id: 1572687529253,
        filename: 'Tabellen-Differenzen.pdf'
    };
    postDBData(url, data, () => {

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