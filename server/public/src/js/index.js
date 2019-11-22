import * as servCon from './serverConnector';
import $ from 'jquery';
import * as tables from './tables';
import * as qrCode from "./qrGenerator";
import * as gui from './gui';
import 'bootstrap'
import 'bootstrap/dist/css/bootstrap.min.css';
import '../css/custom.css';
import 'tabulator-tables/dist/css/tabulator.min.css';
import 'tabulator-tables/dist/css/semantic-ui/tabulator_semantic-ui.min.css';

const deviceTable = tables.initDeviceTable();
const otpTable = tables.initOtpTable();
const fileTable = tables.initFileTable();
const qrImage = qrCode.initDeviceQR();

$('#reg-device-btn').on('click', () => {
    const registerDiv = $('#qr-wrapper');
    const registerBtn = $('#reg-device-btn');

    if(registerDiv.css('display') === 'none') {
        registerDiv.toggle();
        registerBtn.html("Hide registration QR");
    }
    else if(registerDiv.css('display') === 'block') {
        registerDiv.toggle();
        registerBtn.html("Register new Device");
    }
});

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

$('#logout-btn').on('click', function () {
    let url = '/logout_account';
    servCon.getData(url, (cb) => {
        console.log(cb.responseText);
        location.reload();
    });
});
