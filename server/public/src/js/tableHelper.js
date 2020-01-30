import $ from 'jquery';
import Tabulator from 'tabulator-tables/dist/js/tabulator.min';
import {getTokenFromField} from "./authHandler";
import * as servCon from "./serverConnector";
import * as gui from "./gui";
import * as settHandler from "./settingsHandler";


export function setActive(cell) {
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
                    gui.changeNotificationTextAndOpen(cb.responseJSON.message);
                    cell.getTable().setData('/get_user_devices', {auth_token: getTokenFromField()}, 'POST');

                    const url = '/get_user_settings';
                    servCon.postRequestWithData(url, {auth_token: getTokenFromField()}, (cb) => {
                       settHandler.updateSettings(cb.responseJSON);
                    });
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
                    const message = cb.responseJSON.message;
                    cell.getTable().setData('/get_user_devices', {auth_token: getTokenFromField()}, 'POST');
                    const url = '/get_user_settings';
                    servCon.postRequestWithData(url, {auth_token: getTokenFromField()}, (cb) => {
                       settHandler.updateSettings(cb.responseJSON);
                       if (cb.responseJSON['2FA-App'] === 0) {
                           $('#activate_sec_app-popup').modal();
                       } else {
                           gui.changeNotificationTextAndOpen(message);
                       }
                    });
                });
            } else {
                cell.setValue(cell.getOldValue());
            }
        }
    }

export function deleteDevice(e, cell) {
    if (confirm('Do you really want to delete the device?')) {
        const rowData = cell.getRow().getData();
        const url = '/delete_user_device';
        const data = {
            device_id: rowData.id,
            auth_token: getTokenFromField()
        };
        cell.getRow().delete();
        servCon.postRequestWithData(url, data, (cb) => {
            gui.changeNotificationTextAndOpen(cb.responseJSON.message)
        });
    }
}

export function downloadFile(e, cell) {
    const rowData = cell.getRow().getData();
    const fileID = rowData.id;
    const url = '/file_download';
    const method = 'post';
    servCon.requestFile(url, fileID, method);
}

export function saveChanges(e, cell) {
    const rowData = cell.getRow().getData();
    const data = {
        file_id: rowData.id,
        file_description: rowData.file_description,
        file_name: rowData.file_name,
        auth_token: getTokenFromField()
    };
    const url = '/file_update';
    servCon.postRequestWithData(url, data, (cb) => {
        gui.changeNotificationTextAndOpen(cb.responseJSON.message);
    });
}

export function encryption(e, cell) {
    const rowData = cell.getRow().getData();
    const fileID = rowData.id;
    const data = {
        file_id: fileID,
        auth_token: getTokenFromField()
    };
    let url = '';
    if (rowData.is_encrypted) {
        url = '/file_decrypt';
    } else {
        url = '/file_encrypt';
    }
    servCon.postRequestWithData(url, data, (cb) => {
        gui.changeNotificationTextAndOpen(cb.responseJSON.message);
        cell.getTable().setData('/get_user_files');
    });
}

export function deleteRow(e, cell) {
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
            gui.changeNotificationTextAndOpen(cb.responseJSON.message)
        });
    }
}
