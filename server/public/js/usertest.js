$(document).ready(function () {
    $('#user-btn').on('click', function (e) {
        getUsers('/get_users', function (cb) {
            console.log(cb);

            cb.forEach(user => {
                let table = document.getElementById("user-table");
                table.innerHTML += `<tr id="tableRow" style="visibility:hidden">`;
                table.innerHTML += `<td bgcolor=\"#F0E5CC\" id=\"id\"><h3>${user.id}</h3></td>
                                    <td bgcolor=\"#F0E5CC\" id=\"email\"><h3>${user.email}</h3></td>
                                    <td bgcolor=\"#F0E5CC\" id=\"password\"><h3>${user.password}</h3></td>`;
                table.innerHTML += `</tr>`;

                table.style.visibility = 'visible';
            });
        });
    });
});

function getUsers(url, cb) {
    $.ajax({
        type: 'GET',
        url: url,
        complete: function (xmlHTTP) {
            cb(xmlHTTP.responseJSON);
        }
    });
}