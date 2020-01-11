import Tabulator from 'tabulator-tables/dist/js/tabulator.min';
import * as gui from './gui';
import {getTokenFromField} from './authHandler';
import * as th from "./tableHelper";

export function initDeviceTable() {
    const deviceTable = new Tabulator('#device-table', {
        height: '256px',
        layout: 'fitColumns',
        placeholder: 'No Data Available',
        tooltips:true,
        persistence: true,
        columns: [
            {title: 'DeviceID', field: 'device_id'},
            {title: 'Device Name', field: 'device_name'},
            {
                title: 'Active',
                field: 'device_is_active',
                width: 90,
                align: 'center',
                formatter: 'tickCross',
                sorter: 'boolean',
                editor: true,
                cellEdited: th.setActive
            },
            {
                title: 'Delete',
                field: 'delete',
                align: 'center',
                width: 128,
                formatter: gui.deleteIcon,
                cellClick: th.deleteDevice
            }

        ],
    });
    deviceTable.setData('/get_user_devices', {auth_token: getTokenFromField()}, 'POST');
    return deviceTable
}

export function initOtpTable() {
    const otpTable = new Tabulator('#otp-table', {
        height: '512px',
        layout: 'fitColumns',
        placeholder: 'No Data Available',
        tooltips: true,
        persistence: true,
        columns: [
            {title: 'OTP', field: 'used_otp'},
            {title: 'Date', field: 'timestamp', sorter: 'number'},
        ],
    });
    otpTable.setData('/get_user_used_otps', {auth_token: getTokenFromField()}, 'POST');
    return otpTable
}

export function initFileTable() {
    const filesTable = new Tabulator('#files-table', {
        height: '512px',
        layout: 'fitColumns',
        placeholder: 'No Data Available',
        tooltips: true,
        persistence: true,
        columns: [
            {
                title: 'Type',
                field: 'type',
                align: 'center',
                width: 128,
                formatter: gui.previewIcon
            },
            {
                title: 'Filename',
                field: 'file_name',
                editor: 'input',
                validator: 'required'
            },
            {
                title: 'Description',
                field: 'file_description',
                editor: 'input'
            },
            {
                title: 'Encryption',
                field: 'is_encrypted',
                align: 'center',
                width: 128,
                formatter: gui.encryptIcon,
                cellClick: th.encryption
            },
            {
                title: 'Download',
                field: 'downloadFile',
                align: 'center',
                width: 128,
                formatter: gui.downloadIcon,
                cellClick: th.downloadFile
            },
            {
                title: 'Save',
                field: 'saveChanges',
                align: 'center',
                width: 128,
                formatter: gui.saveIcon,
                cellClick: th.saveChanges
            },
            {
                title: 'Delete',
                field: 'delete',
                align: 'center',
                width: 128,
                formatter: gui.deleteIcon,
                cellClick: th.deleteRow
            }
        ],
    });
    filesTable.setData('/get_user_files', {auth_token: getTokenFromField()}, 'POST');
    return filesTable
}
