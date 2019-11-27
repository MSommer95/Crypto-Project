import * as servCon from "./serverConnector";
import $ from "jquery";

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
