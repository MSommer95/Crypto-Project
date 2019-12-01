import * as tables from './tables';
import * as qrCode from './qrGenerator';
import * as settHandle from "./settingsHandler";
import 'bootstrap'
import 'bootstrap/dist/css/bootstrap.min.css';
import '../css/custom.css';
import 'tabulator-tables/dist/css/tabulator.min.css';
import 'tabulator-tables/dist/css/semantic-ui/tabulator_semantic-ui.min.css';

const deviceTable = tables.initDeviceTable();
const otpTable = tables.initOtpTable();
const fileTable = tables.initFileTable();
const qrImage = qrCode.initDeviceQR();

settHandle.initSettings();
