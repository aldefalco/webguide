var utils = require('sdk/tabs/utils'),
    win = require('sdk/window/utils');


function captureTab() {
    var tab = utils.getActiveTab(win.getMostRecentBrowserWindow());
    var contentWindow = utils.getTabContentWindow(tab);
    var document = contentWindow.document;

    let w = contentWindow.innerWidth;
    let h = contentWindow.innerHeight;
    let x = contentWindow.scrollX;
    let y = contentWindow.scrollY;

    let canvas = document.createElementNS('http://www.w3.org/1999/xhtml', 'canvas');

    canvas.width = w;
    canvas.height = h;

    let ctx = canvas.getContext('2d');

    ctx.drawWindow(contentWindow, x, y, w, h, '#000');

    let dataURL = canvas.toDataURL();

    canvas = null;

    return dataURL;
}

exports.tab = captureTab;