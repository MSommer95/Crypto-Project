import $ from "jquery";
import * as servCon from "./serverConnector";


let qrUpdateInterval;
let intervalPaused = false;

export function initDeviceQR() {
    const url = '/request_qr';
    servCon.getData(url, (cb) => {
        const imgData = cb.responseText;
        const img = $('<img class="mx-auto mb-5" id="qr-img-container" width="50%"/>');

        img.attr('src', 'data:image/png;base64,' + imgData);
        img.appendTo('#device-registration-qr');
    });
}

export function updateDeviceQR() {
    const url = '/request_qr';

    servCon.getData(url, (cb) => {
       const img = $('#qr-img-container');
       const imgData = cb.responseText;

       img.attr('src', 'data:image/png;base64,' + imgData);
    });
}

export function toggleQRGen() {
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
                updateDeviceQR();
            }, 60000);
        }
    } else if (registerDiv.css('display') === 'block') {
        registerDiv.toggle();
        registerBtn.html("Register new Device");
        if(qrUpdateInterval) {
            intervalPaused = true;
        }
    }
}
