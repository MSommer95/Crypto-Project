import * as servCon from './serverConnector';
import $ from 'jquery/dist/jquery.min';
import * as tables from './tables';
import 'bootstrap'
import 'bootstrap/dist/css/bootstrap.min.css';
import '../css/custom.css';
import 'tabulator-tables/dist/css/tabulator.min.css';
import 'tabulator-tables/dist/css/semantic-ui/tabulator_semantic-ui.min.css';

const deviceTable = tables.initDeviceTable();
const otpTable = tables.initOtpTable();
const fileTable = tables.initFileTable();

$('#decrypt-btn').on('click', () => {
    let url = '/file_decrypt';
    let data = {
        file_id: 1573047199622,
        filename: 'AR-Kickoff.pptx'
    };
    servCon.postDBData(url, data, () => {

    });
});

$('#encrypt-btn').on('click', () => {
    let url = '/file_encrypt';
    let data = {
        file_id: 1573047070495,
        filename: 'AR-Kickoff.pptx'
    };
    servCon.postDBData(url, data, () => {

    });
});

$('#logoutButton').on('click', function () {
    let url = '/logout_account';
    servCon.getDBData(url, (cb) => {
        console.log(cb.responseText);
        location.reload();
    });
});
