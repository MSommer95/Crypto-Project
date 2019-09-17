

$(document).ready(function () {

    /*$('#submit-btn').on('click', function (e) {

        let url = "/encryption";
        let username = $('#username').val();
        let file_input = $('#file');
        let file = file_input[0].files[0];

        let reader = new FileReader();
        reader.readAsDataURL(file);
        reader.onload = shipOff;


        function shipOff(event){

            let test = JSON.stringify({ "dataURL": reader.result });

            // View the file
            let fileURL = JSON.parse(test).dataURL;
            $("#display-pdf").empty();
            $("#display-pdf").append(`<object data="${fileURL}"
              type="application/pdf" width="400px" height="200px">
            </object>`);

            let result = event.target.result;
            let filename = $('#file').prop('files')[0].name;
            let data = {
                username : username,
                file : result,
                filename: filename
            };

            postDBData(url, data, function (e) {
                console.log(e);
            });
        }

    });*/



});


// Get Funktion für die Server-Datenbank Abfragen
function getDBData(url, cb) {
    $.ajax({
        type: 'GET',
        url: url,
        dataType: 'json',
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