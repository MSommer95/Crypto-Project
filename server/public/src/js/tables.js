import Tabulator from 'tabulator-tables/dist/js/tabulator.min';
import locked from '../img/baseline_lock_black_18dp.png';
import unlocked from '../img/baseline_lock_open_black_18dp.png';
import dlIcon from '../img/baseline_cloud_download_black_18dp.png';
import * as servCon from './serverConnector';

export function initDeviceTable() {
    const deviceTable = new Tabulator('#device-table', {
        height: '100%',
        columns: [
            {title: 'ID', field: 'id', sorter: 'number'},
            {title: 'Device', field: 'device'},
        ],
    });
    return deviceTable
}

export function initOtpTable() {
    const otpTable = new Tabulator('#otp-table', {
        height: '100%',
        columns: [
            {title: 'ID', field: 'id', sorter: 'number'},
            {title: 'OTP', field: 'otp'},
            {title: 'Date', field: 'date', sorter: 'number', align: 'center'},
        ],
    });
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
        icon.src = dlIcon;
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
        height: '100%',
        columns: [
            {title: 'Preview', field: 'preview'},
            {title: 'Filename', field: 'file_name'},
            {title: 'Description', field: 'description'},
            {title: 'Encryption', field: 'is_encrypted', formatter: encryptIcon, cellClick: encryption},
            {title: 'Download File', field: 'downloadFile', formatter: downloadIcon, cellClick: downloadFile}
        ],
    });

    filesTable.setData('/get_user_files');

    return filesTable
}
