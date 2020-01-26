import * as gui from './gui';
import 'bootstrap/dist/css/bootstrap.min.css';
import 'bootstrap/js/dist/popover'
import 'bootstrap/js/dist/modal'
import '../css/custom.css';
import * as authhandler from "./authHandler";

gui.activatePopovers();
authhandler.invalidEmail();