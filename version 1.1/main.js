const electron = require('electron')
const {app, BrowserWindow} = electron
const path = require('path')
const url  = require('url')

let win

function createWindow(){
	win = new BrowserWindow ({
		width: 1480,
    	height: 925,
    	minWidth: 1480,
    	minHeight: 950,
		maxWidth: 1480,
    	maxHeight: 950,
		frame:true,      // quita los bordes en la ventana
		transparent: false, // hace la ventana trasparente

    	webPreferences: {
      	nodeIntegration: true},
		icon: 'image/logo.png'   // Icono de la aplicación

	})
	win.loadURL(url.format({
		pathname: path.join(__dirname, 'index.html'),
		protocol: 'file',
		slashes: true
	}))
	win.removeMenu();
	win.setMenu(null);           // Elimina el menu de la aplicación

	//win.webContents.openDevTools()



	
}
app.on('ready', createWindow)