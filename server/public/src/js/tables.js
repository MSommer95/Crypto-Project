import $ from 'jquery';
import Tabulator from 'tabulator-tables/dist/js/tabulator.min';
import * as servCon from './serverConnector';
import * as gui from './gui';
import {getTokenFromField} from './authHandler';

export function initDeviceTable() {
    function setActive(cell) {
        const cellValue = cell.getValue();
        if (cellValue === false) {
            if (confirm('Do you really want to deactivate the device? There must be at least one active device! (If there is none the second factor will be your Email)')) {
                const rowData = cell.getRow().getData();
                const url = '/deactivate_user_device';
                const data = {
                    device_id: rowData.id,
                    auth_token: getTokenFromField()
                };
                servCon.postRequestWithData(url, data, (cb) => {
                    gui.changeNotificationTextAndOpen(cb.responseText);
                    deviceTable.setData('/get_user_devices', {auth_token: getTokenFromField()}, 'POST');
                });
            } else {
                cell.setValue(cell.getOldValue());
            }
        } else if (cellValue === true) {
            if (confirm('Do you really want to activate the device? There can only be one active device! (The other one will be deactivated)')) {
                const rowData = cell.getRow().getData();
                const url = '/activate_user_device';
                const data = {
                    device_id: rowData.id,
                    auth_token: getTokenFromField()
                };
                servCon.postRequestWithData(url, data, (cb) => {
                    gui.changeNotificationTextAndOpen(cb.responseText);
                    deviceTable.setData('/get_user_devices', {auth_token: getTokenFromField()}, 'POST');
                });
            } else {
                cell.setValue(cell.getOldValue());
            }
        }
    }

    function deleteDevice(e, cell) {
        if (confirm('Do you really want to delete the device?')) {
            const rowData = cell.getRow().getData();
            const url = '/delete_user_device';
            const data = {
                device_id: rowData.id,
                auth_token: getTokenFromField()
            };
            cell.getRow().delete();
            servCon.postRequestWithData(url, data, (cb) => {
                gui.changeNotificationTextAndOpen(cb.responseText)
            });
        }
    }

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
                cellEdited: setActive
            },
            {
                title: 'Delete',
                field: 'delete',
                align: 'center',
                width: 128,
                formatter: gui.deleteIcon,
                cellClick: deleteDevice
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

    function downloadFile(e, cell) {
        const rowData = cell.getRow().getData();
        const fileID = rowData.id;
        const url = '/file_download';
        const method = 'post';
        servCon.requestFile(url, fileID, method);
    }

    function saveChanges(e, cell) {
        const rowData = cell.getRow().getData();
        const data = {
            file_id: rowData.id,
            file_description: rowData.file_description,
            file_name: rowData.file_name,
            is_encrypted: rowData.is_encrypted,
            auth_token: getTokenFromField()
        };
        const url = '/file_update';
        servCon.postRequestWithData(url, data, (cb) => {
            gui.changeNotificationTextAndOpen(cb.responseText);
        });
    }

    function encryption(e, cell) {
        const rowData = cell.getRow().getData();
        const filename = rowData.file_name;
        const fileID = rowData.id;
        const data = {
            file_id: fileID,
            file_name: filename,
            auth_token: getTokenFromField()
        };
        let url = '';
        if (rowData.is_encrypted) {
            url = '/file_decrypt';
        } else {
            url = '/file_encrypt';
        }
        servCon.postRequestWithData(url, data, (cb) => {
            gui.changeNotificationTextAndOpen(cb.responseText);
            filesTable.setData('/get_user_files');
        });
    }

    function deleteRow(e, cell) {
        if (confirm('Do you really want to delete the file?')) {
            const rowData = cell.getRow().getData();
            const url = '/file_delete';
            const data = {
                file_id: rowData.id,
                is_encrypted: rowData.is_encrypted,
                auth_token: getTokenFromField()
            };
            cell.getRow().delete();
            servCon.postRequestWithData(url, data, (cb) => {
                gui.changeNotificationTextAndOpen(cb.responseText)
            });
        }
    }

    const filesTable = new Tabulator('#files-table', {
        height: '512px',
        layout: 'fitColumns',
        placeholder: 'No Data Available',
        tooltips: true,
        persistence: true,
        columns: [
            {title: 'Preview', field: 'preview'},
            {title: 'Filename', field: 'file_name', editor: 'input'},
            {title: 'Description', field: 'file_description', editor: 'input'},
            {
                title: 'Encryption',
                field: 'is_encrypted',
                align: 'center',
                width: 128,
                formatter: gui.encryptIcon,
                cellClick: encryption
            },
            {
                title: 'Download',
                field: 'downloadFile',
                align: 'center',
                width: 128,
                formatter: gui.downloadIcon,
                cellClick: downloadFile
            },
            {
                title: 'Save',
                field: 'saveChanges',
                align: 'center',
                width: 128,
                formatter: gui.saveIcon,
                cellClick: saveChanges
            },
            {
                title: 'Delete',
                field: 'delete',
                align: 'center',
                width: 128,
                formatter: gui.deleteIcon,
                cellClick: deleteRow
            }
        ],
    });

    filesTable.setData('/get_user_files', {auth_token: getTokenFromField()}, 'POST');

    return filesTable
}
