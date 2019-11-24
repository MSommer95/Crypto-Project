import $ from 'jquery';
import Tabulator from 'tabulator-tables/dist/js/tabulator.min';
import locked from '../img/baseline_lock_black_18dp.png';
import unlocked from '../img/baseline_lock_open_black_18dp.png';
import downloadPng from '../img/baseline_cloud_download_black_18dp.png';
import savePng from '../img/baseline_save_black_18dp.png';
import deletePng from '../img/baseline_delete_forever_black_18dp.png';
import * as servCon from './serverConnector';
import * as gui from './gui';

const saveIcon = (cell, formatterParams, onRendered) => {
    const icon = new Image();
    icon.src = savePng;
    icon.height = 32;
    icon.width = 32;
    return icon
};
const deleteIcon = (cell, formatterParams, onRendered) => {
    const icon = new Image();
    icon.src = deletePng;
    icon.height = 32;
    icon.width = 32;
    return icon
};

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

    function downloadFile(e, cell) {
        const rowData = cell.getRow().getData();
        const filepath = rowData.path;
        const url = '/file_download';
        const method = 'post';
        servCon.requestFile(url, filepath, method);
    }
    function saveChanges(e, cell) {
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
            gui.changeNotificationTextAndOpen(cb.responseText);
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
            gui.changeNotificationTextAndOpen(cb.responseText);
            filesTable.setData('/get_user_files');
        });
    }
    function deleteRow(e, cell) {
        const rowData = cell.getRow().getData();
        cell.getRow().delete();
        const url = '/file_delete';
        const data = {
            file_id: rowData.id,
            path: rowData.path,
            is_encrypted: rowData.is_encrypted
        };
        servCon.postDBData(url, data, (cb) => {
            gui.changeNotificationTextAndOpen(cb.responseText)
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
                width: 128,
                formatter: encryptIcon,
                cellClick: encryption
            },
            {
                title: 'Download',
                field: 'downloadFile',
                align: 'center',
                width: 128,
                formatter: downloadIcon,
                cellClick: downloadFile
            },
            {
                title: 'Save',
                field: 'saveChanges',
                align: 'center',
                width: 128,
                formatter: saveIcon,
                cellClick: saveChanges
            },
            {
                title: 'Delete',
                field: 'delete',
                align: 'center',
                width: 128,
                formatter: deleteIcon,
                cellClick: deleteRow
            }
        ],
    });

    filesTable.setData('/get_user_files');

    $('#files-table-btn-save').on('click', () => {
    });

    return filesTable
}
