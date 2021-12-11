const {app, BrowserWindow} = require('electron');

let win = null

const createWindow = () => {
    win = new BrowserWindow({
        width: 620,
        height: 420,
        //resizable: false,
        minimizable: false,
        maximizable: false,
        autoHideMenuBar: true,
        webPreferences: {
            nodeIntegration: true
        }
    });

    win.loadFile("index.html");
}

app.whenReady().then(createWindow)
