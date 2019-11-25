import $ from 'jquery';
import Tabulator from 'tabulator-tables/dist/js/tabulator.min';
import locked from '../img/baseline_lock_black_18dp.png';
import unlocked from '../img/baseline_lock_open_black_18dp.png';
import downloadPng from '../img/baseline_cloud_download_black_18dp.png';
import * as servCon from './serverConnector';
import {postDBData} from './serverConnector';
import * as gui from './gui';

export function initDeviceTable() {
    function setActive(cell) {
        const cellValue = cell.getValue();
        if (cellValue === false) {
            if (confirm('Do you really want to deactivate the device? There must be at least one active device! (If there is none the second factor will be your Email)')) {
                const rowData = cell.getRow().getData();
                const url = '/deactivate_user_device';
                const data = {
                    device_id: rowData.id
                };
                postDBData(url, data, (cb) => {
                    gui.changeNotificationTextAndOpen(cb.responseText);
                    deviceTable.setData('/get_user_devices');
                });
            } else {
                cell.setValue(cell.getOldValue());
            }
        } else if (cellValue === true) {
            if (confirm('Do you really want to activate the device? There can only be one active device! (The other one will be deactivated)')) {
                const rowData = cell.getRow().getData();
                const url = '/activate_user_device';
                const data = {
                    device_id: rowData.id
                };
                postDBData(url, data, (cb) => {
                    gui.changeNotificationTextAndOpen(cb.responseText);
                    deviceTable.setData('/get_user_devices');
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
                device_id: rowData.id
            };
            cell.getRow().delete();
            servCon.postDBData(url, data, (cb) => {
                gui.changeNotificationTextAndOpen(cb.responseText)
            });
        }
    }

    const deviceTable = new Tabulator('#device-table', {
        height: '100%',
        layout: "fitColumns",
        columns: [
            {title: 'DeviceID', field: 'device_id'},
            {title: 'Device Name', field: 'device_name'},
            {
                title: 'Active',
                field: 'device_is_active',
                width: 90,
                align: "center",
                formatter: "tickCross",
                sorter: "boolean",
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
        if (confirm('Do you really want to delete the file?')) {
            const rowData = cell.getRow().getData();
            const url = '/file_delete';
            const data = {
                file_id: rowData.id,
                path: rowData.path,
                is_encrypted: rowData.is_encrypted
            };
            cell.getRow().delete();
            servCon.postDBData(url, data, (cb) => {
                gui.changeNotificationTextAndOpen(cb.responseText)
            });
        }
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

    filesTable.setData('/get_user_files');

    $('#files-table-btn-save').on('click', () => {
    });

    return filesTable
}
