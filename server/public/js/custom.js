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
var table = new Tabulator("#hotp-table", {
    height:"311px",
    columns:[
    {title:"ID", field:"id", sorter:"number"},
    {title:"HOTP", field:"hotp"},
    {title:"Date", field:"date", sorter:"number", align:"center"},
    ],
});

var table = new Tabulator("#device-table", {
    height:"100px",
    columns:[
    {title:"ID", field:"id", sorter:"number"},
    {title:"Device", field:"device"},
    ],
});


$('#hotpButton').on('click', function(){
  chooseNavbar(this);
});
$('#fileButton').on('click', function(){
  chooseNavbar(this);
});
$('#aboutButton').on('click', function(){
  chooseNavbar(this);
});
$('#settingButton').on('click', function(){
  chooseNavbar(this);
});
$('#logoutButton').on('click', function(){
  chooseNavbar(this);
});


function showElement(element) {
    $(element).removeClass('hidden');
}

function hideElement(element) {
    $(element).addClass('hidden');
}


function chooseNavbar(button) {


    const hotpDiv = $('#hotp-section');
    const fileDiv = $('#file-section');
    const aboutDiv = $('#about-section');
    const settingDiv = $('#setting-section');
    const logoutDiv = $('#logout-section');


    // Anzeigen/ausblenden der entsprechenden Container
    switch (button.id) {
        case 'hotpButton':
        showElement(hotpDiv);
        showElement(fileDiv);
        hideElement(aboutDiv);
        hideElement(settingDiv);
        hideElement(logoutDiv);
        break;
    case 'fileButton':
        hideElement(hotpDiv);
        showElement(fileDiv);
        hideElement(aboutDiv);
        hideElement(settingDiv);
        hideElement(logoutDiv);
        break;
    case 'aboutButton':
        hideElement(hotpDiv);
        hideElement(fileDiv);
        showElement(aboutDiv);
        hideElement(settingDiv);
        hideElement(logoutDiv);
        break;
    case 'settingButton':
        hideElement(hotpDiv);
        hideElement(fileDiv);
        hideElement(aboutDiv);
        showElement(settingDiv);
        hideElement(logoutDiv);
        break;
    case 'logoutButton':
        hideElement(hotpDiv);
        hideElement(fileDiv);
        hideElement(aboutDiv);
        hideElement(settingDiv);
        showElement(logoutDiv);
        break;
    }
}
