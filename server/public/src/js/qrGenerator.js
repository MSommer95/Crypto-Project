import * as servCon from "./serverConnector";
import $ from "jquery";

export function initDeviceQR() {
    const url = '/request_qr';
    servCon.getData(url, (cb) => {
        const imgData = cb.responseText;
        console.log(imgData);
        const img = $('<img id="image_id" />');
        img.attr('src', 'data:image/png;base64,' + imgData);
        img.appendTo('#device-registration-qr');
    });
}
