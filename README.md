# ElectroPulse

IDE utilizado Visual Studio Code 

En la carpeta denominada "Versión 1.1", se encuentra el contenido correspondiente al software de Einsted, diseñado para el controlador del electroporador Nanopulso y desarrollado en el framework Electron JS.

-La carpeta "image" contiene las imágenes utilizadas en el diseño del software.

-La carpeta "scripts" alberga la lógica necesaria para generar el gráfico, utilizando la biblioteca de Chart.js, así como la comunicación con el microcontrolador.

-La carpeta "styles" contiene los estilos aplicados a los archivos index.html e inicio.html.

# Setup

Recomendado usar la terminal (tanto en Linux/macOS como en Windows).

Primero instalar Node.js (recomiendo con nvm, que permite manejar distintas versiones). Tener en cuenta que al instalarse Node.js, se instala npm que es un manejador de paquetes. Se utiliza npm para hacer las siguientes instalaciones. 

Instalar Electron.js (con npm install [...biblioteca-que-corresponda]), lo mismo con Chart.js.

Si no se tiene Python instalado, instalar también Python.

# Ejecutar la aplicación

Antes que nada se deben instalar todas las dependencias. Para esto, moverse hasta el directorio 'version 1.1' y ejecutar:

npm install

Ahora sí, en el mismo directorio, ejecutar:

npm start

Sugerencias: 
Preparar VS Code con las extensiones correspondientes para el debugging (Live Server, etc.)

-extensiones VCode.txt (Angie)

# Crear un archivo ejecutable

npm run build

|pantalla 1920x1080 "

-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Diseño de la versión 2.0 :

Actualizaciones agregar se encuentra en la carpeta design

figma (finalizado):

https://www.figma.com/file/8ml8qeQpXv2vmgATINp71k/Electroporation-V2?type=design&node-id=0%3A1&mode=design&t=OvASemqDTbMfxPL3-1

https://www.figma.com/proto/8ml8qeQpXv2vmgATINp71k/Electroporation-V2?page-id=0%3A1&type=design&node-id=1-4&viewport=952%2C265%2C0.23&scaling=scale-down&starting-point-node-id=1%3A4&mode=design

# Diagrama de flujo:

https://www.figma.com/file/raj7aIOXpUMuRkGqP5z59x/Diagrama-de-flujos-Electroporador-Nano-Pulso?type=whiteboard&node-id=0%3A1&t=CD8iPQ1XYHl9wc4d-1


-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Osciloscopio:

Se encuentra una aplicación realizada en python para extraer datos del osciloscopio RIGOL DSO138. 

Sugerencia: instalar la biblioteca pyvisa
