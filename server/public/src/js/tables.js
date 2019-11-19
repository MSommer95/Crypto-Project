import Tabulator from 'tabulator-tables/dist/js/tabulator.min';
import lock from'../img/icons8-passwort-48.png';

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

    const encryptIcon = () => {
        const icon =  new Image();
        icon.src = lock;
        icon.height = 32;
        icon.width = 32;
        return icon
    };

    const testData = [
        {
            preview: 'Preview',
            id: 0,
            filename: 'Filename',
            description: 'Description',
        }
    ];

    const filesTable = new Tabulator('#files-table', {
        height: '100%',
        data: testData,
        columns: [
            {title: 'Preview', field: 'preview'},
            {title: 'id', field: 'id', sorter: 'number'},
            {title: 'filename', field: 'filename'},
            {title: 'description', field: 'description'},
            {title: 'encryption', field: 'isEncrypted', formatter: encryptIcon},
        ],
    });
    return filesTable
}