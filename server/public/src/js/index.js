import * as servCon from './serverConnector';
import $ from 'jquery/dist/jquery.min';
import Tabulator from 'tabulator-tables/dist/js/tabulator.min';

import '../css/bootstrap.css'
import '../css/custom.css'
import '../css/main.css'
import '../css/tabulator.css'

$('#decrypt-btn').on('click', () => {
    let url = '/file_decrypt';
    let data = {
        file_id: 1573047199622,
        filename: 'AR-Kickoff.pptx'
    };
    servCon.postDBData(url, data, () => {

    });
});

$('#encrypt-btn').on('click', () => {
    let url = '/file_encrypt';
    let data = {
        file_id: 1573047070495,
        filename: 'AR-Kickoff.pptx'
    };
    servCon.postDBData(url, data, () => {

    });
});

const otpTable = new Tabulator("#hotp-table", {
    height: "311px",
    columns: [
        {title: "ID", field: "id", sorter: "number"},
        {title: "HOTP", field: "hotp"},
        {title: "Date", field: "date", sorter: "number", align: "center"},
    ],
});

const deviceTable = new Tabulator("#device-table", {
    height: "100px",
    columns: [
        {title: "ID", field: "id", sorter: "number"},
        {title: "Device", field: "device"},
    ],
});

$('#logoutButton').on('click', function () {
    let url = '/logout_account';
    servCon.getDBData(url, (cb) => {
        console.log(cb.responseText);
        location.reload();
    });
});
