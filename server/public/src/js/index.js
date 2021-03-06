import * as tables from './tables';
import * as qrCode from './qrGenerator';
import * as settHandle from './settingsHandler';
import * as authHandler from './authHandler';
import * as gui from './gui';
import 'bootstrap/js/dist/popover'
import 'bootstrap/js/dist/modal'
import 'bootstrap/js/dist/dropdown'
import 'bootstrap/dist/css/bootstrap.min.css';
import '../css/custom.css';
import 'tabulator-tables/dist/css/tabulator.min.css';
import 'tabulator-tables/dist/css/semantic-ui/tabulator_semantic-ui.min.css';

const deviceTable = tables.initDeviceTable();
const otpTable = tables.initOtpTable();
const fileTable = tables.initFileTable();
const qrImage = qrCode.initDeviceQR();
gui.activatePopovers();
settHandle.initSettings();
