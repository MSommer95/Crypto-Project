import * as servCon from './serverConnector';
import $ from 'jquery';
import * as tables from './tables';
import * as qrCode from './qrGenerator';
import * as settHandle from "./settingsHandler";
import * as secPass from "./passwordGenerator";
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
let qrUpdateInterval;
let intervalPaused = false;
settHandle.initSettings();

$('#reg-device-btn').on('click', () => {
    const registerDiv = $('#qr-wrapper');
    const registerBtn = $('#reg-device-btn');

    if (registerDiv.css('display') === 'none') {
        registerDiv.toggle();
        registerBtn.html("Hide registration QR");

        if(intervalPaused) {
            intervalPaused = false;
        }

        if(!qrUpdateInterval) {
            qrUpdateInterval = setInterval(() => {
                if (intervalPaused)
                    return;

                qrCode.updateDeviceQR();
            }, 60000);
        }
    } else if (registerDiv.css('display') === 'block') {
        registerDiv.toggle();
        registerBtn.html("Register new Device");

        if(qrUpdateInterval) {
            intervalPaused = true;
        }
    }
});

$('#open-password-generator-btn').on('click', () => {
    $('#secure_password-popup').modal();
    let password = secPass.generatePassword(true, true, true, true, 16);
    $('#secure_password-pwd').val(password);
    $('#create_password').val(password);
});

$('#logout-btn').on('click', function () {
    let url = '/logout_account';
    servCon.getData(url, (cb) => {
        console.log(cb.responseText);
        location.reload();
    });
});
