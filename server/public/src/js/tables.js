import $ from 'jquery';
import Tabulator from 'tabulator-tables/dist/js/tabulator.min';
import locked from '../img/baseline_lock_black_18dp.png';
import unlocked from '../img/baseline_lock_open_black_18dp.png';
import downloadPng from '../img/baseline_cloud_download_black_18dp.png';
import uploadloadPng from '../img/baseline_cloud_upload_black_18dp.png';
import * as servCon from './serverConnector';

export function initDeviceTable() {
    const deviceTable = new Tabulator('#device-table', {
        height: '100%',
        layout: "fitColumns",
        columns: [
            {title: 'DeviceID', field: 'device_id'},
            {title: 'Device Name', field: 'device_name'},
        ],
    });

    deviceTable.setData('/get_user_devices');

    return deviceTable
}

export function initOtpTable() {
    const otpTable = new Tabulator('#otp-table', {
        height: '512px',
        layout: "fitColumns",
        columns: [
            {title: 'OTP', field: 'used_otp'},
            {title: 'Date', field: 'timestamp', sorter: 'number'},
        ],
    });

    otpTable.setData('/get_user_used_otps');

    return otpTable
}

export function initFileTable() {

    const encryptIcon = (cell, formatterParams, onRendered) => {
        const icon = new Image();
        icon.height = 32;
        icon.width = 32;
        if (cell.getRow().getData().is_encrypted) {
            icon.src = locked;
        } else {
            icon.src = unlocked;
        }
        return icon
    };
    const downloadIcon = (cell, formatterParams, onRendered) => {
        const icon = new Image();
        icon.src = downloadPng;
        icon.height = 32;
        icon.width = 32;
        return icon
    };
    const uploadIcon = (cell, formatterParams, onRendered) => {
        const icon = new Image();
        icon.src = uploadloadPng;
        icon.height = 32;
        icon.width = 32;
        return icon
    };

    function downloadFile(e, cell) {
        const rowData = cell.getRow().getData();
        const filepath = rowData.path;
        const url = '/file_download';
        const method = 'post';
        servCon.requestFile(url, filepath, method);
    }

    function uploadChanges(e, cell) {
        const rowData = cell.getRow().getData();
        const sendData = {
            file_id: rowData.id,
            file_description: rowData.file_description,
            path: rowData.path,
            file_name: rowData.file_name,
            is_encrypted: rowData.is_encrypted
        };
        const url = '/file_update';
        servCon.postDBData(url, sendData, (cb) => {
            console.log(cb)
        });
    }

    function encryption(e, cell) {
        const rowData = cell.getRow().getData();
        const filename = rowData.file_name;
        const fileID = rowData.id;
        const data = {
            file_id: fileID,
            file_name: filename
        };
        let url = '';
        if (rowData.is_encrypted) {
            url = '/file_decrypt';
        } else {
            url = '/file_encrypt';
        }
        servCon.postDBData(url, data, (cb) => {
            console.log(cb.responseText);
            if (cb.responseText.includes('worked')) {
                filesTable.setData('/get_user_files');
            } else if (cb.responseText.includes('wrong')) {
                alert(cb.responseText)
            }
        });
    }

    const filesTable = new Tabulator('#files-table', {
        height: '512px',
        layout: "fitColumns",
        columns: [
            {title: 'Preview', field: 'preview'},
            {title: 'Filename', field: 'file_name', editor: 'input'},
            {title: 'Description', field: 'file_description', editor: 'input'},
            {
                title: 'Encryption',
                field: 'is_encrypted',
                align: 'center',
                formatter: encryptIcon,
                cellClick: encryption
            },
            {
                title: 'Download File',
                field: 'downloadFile',
                align: 'center',
                formatter: downloadIcon,
                cellClick: downloadFile
            },
            {
                title: 'Save Changes',
                field: 'saveChanges',
                align: 'center',
                formatter: uploadIcon,
                cellClick: uploadChanges
            }
        ],
    });

    filesTable.setData('/get_user_files');

    $('#files-table-btn-save').on('click', () => {
    });

    return filesTable
}
