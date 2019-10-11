$('#send_login-btn').on('click', ()=>{
    let url = '/login_account';
    let data = {
        email: $('#login_email').val(),
        password: $('#login_password').val()
    };
    postDBData(url, data, (cb)=>{
        if(cb.responseText.includes('HOTP')){
            showElement($('#hotp-container'));
        } else {
            window.location.href = '../index.html'
        }
    });

});


$('#send_hotp').on('click', ()=>{
    let hotp = $('#confirm_hotp').val();
    if(hotp != null) {
        let url = '/verify_hotp';
        let data = {
            hotp: hotp
        };
        postDBData(url, data, (cb) => {
            console.log(cb.responseText)
        });
    }
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
            cb(jqXHR);
        }
    });
}

// show function
function showElement(element) {
    $(element).removeClass('hidden');
}

// hide function
function hideElement(element) {
    $(element).addClass('hidden');
}