const electron = require('electron')
const {app, BrowserWindow} = electron
const path = require('path')
const url  = require('url')

let win

function createWindow(){
	win = new BrowserWindow ({ //el problema no es en sí el tamaño de la pantalla, sino que el contenido no es responsive
		
		width: 1300,
    	height: 890, 
    	minWidth: 1300,
    	minHeight: 890,
		maxWidth: 1920,
    	maxHeight: 1080,
		frame: true,      // quita los bordes en la ventana
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

	// win.webContents.openDevTools()



	
}
app.on('ready', createWindow)