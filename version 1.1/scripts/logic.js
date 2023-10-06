var newlabels = [0]
var ip = "10.31.110.91";
var ton = document.getElementById('ton').value
var toff = document.getElementById('toff').value
var pulso = document.getElementById('pulso').value
var newdatay = [0, 800, 800, 800, 0, 0, 800, 800, 0, 0, 800, 800, 0, 0, 800, 800, 0, 0, 800, 800, 0, 0, 800, 800, 0, 0, 800, 800, 0, 0, 800, 800, 0, 0, 800, 800, 0, 0, 800, 800, 0, 0, 800, 800, 0, 0, 800, 800, 0, 0, 800, 800, 0, 0] //ejey
ton = parseInt(ton)
toff = parseInt(toff)
pulso = parseInt(pulso)
    ///////////////////////////sonido/////////////////////////////////
var sonido = new Audio();
sonido.src = "pip.mp3";
var status = 0
    //////////////////////////////////////////////////////////////////////////////////////////////
function statusConection() {
    fetch('http://' + ip + '/status') //url consulta continua de estado
        .then(response => response.text())
        .then(data => console.log(status = 1)) // OK 1
        .catch(err => console.log(status = 0)); //error  0
    if (status == 1) {
        document.getElementById("myDiv").style.background = "#8DC63F"; //CHANGE COLOR
        document.getElementById('text').innerText = "Connected to... " + ip //CHANGE TEXT
        document.getElementById("sectionWave").style.opacity = "1";
    } else {
        document.getElementById("myDiv").style.background = "#FF6174";
        document.getElementById('text').innerText = "Disconnected...";
        document.getElementById("sectionWave").style.opacity = "0.4";
    }
}
setInterval(statusConection, 100);
///Configurar estilo
Chart.defaults.font.family = "Didact Gothic";
Chart.defaults.font.size = 20;
Chart.defaults.color = "#545454";
//Datos  configuration
const data = {
    labels: newlabels, //valores del ejex
    datasets: [{
        label: 'Voltaje', //nombre del dataset
        data: newdatay, //valores del eje y
        borderWidth: 7, //ancho de linea
        tension: 0, //este parametro es para hacer curvo
        fill: true,
        pointHitRadius: 10,
        pointBorderWidth: 0,
        pointHoverRadius: 4,
        pointHoverBorderColor: 'white',
        pointHoverBorderWidth: 2,
        pointRadius: 0,
        backgroundColor: 'rgba(0, 99, 132, 0.6)',
        borderColor: '#1776BD',
        lineTension: 0.01, //ajuste de contorno
        borderJoinStyle: 'miter',
    }]
};
//Data opciones
const opcions = {
        maintainAspectRatio: false, //parametro para controlar ancho y alto del grafico
        responsive: true,
        plugins: {
            legend: {
                display: false
            },
            title: {
                display: false,
                text: 'Voltaje vs Tiempo'
            }
        },
        scales: {
            x: {
                display: true,
                type: 'linear',
                title: {
                    display: true,
                    text: 'Time [ns]',
                    color: '#1776BD',
                    font: {
                        family: 'Didact Gothic',
                        size: 25,
                        weight: 'bold',
                        lineHeight: 2
                    } //,
                    // padding: {top: 20, left: 0, right: 0, bottom: 0}
                },
                grid: {
                    display: false,

                    drawBorder: false
                },
                ticks: {

                    autoSkip: false,
                    callback: (value, index, values) => {
                        //    console.log('valueskol', values)
                        return value
                    },
                    beginAtZero: true,
                    padding: 2
                },
                min: -100,
                max: 1800 //ajuste de eje min max fuera del tick
            },
            y: {

                display: true,
                title: {
                    display: true,
                    text: 'Voltage [V]',
                    color: '#1776BD',
                    font: {
                        family: 'Didact Gothic',
                        size: 25,
                        weight: 'bold',
                        lineHeight: 2
                    }
                },
                grid: {
                    display: false,
                    drawBorder: false
                },
                min: 0,
                max: 1000,
                ticks: {
                    padding: 0,
                }
            }
        },
        radius: 0 //disminuir el radio de cada punto
    }
    //////////////////////////Grafico vizualizar///////////////////////////
var ctx = document.getElementById('myChart')
    //Se declara un nuevo objeto tipo CHART (objetohtml, {caracteristicadel objeto});
var chart = new Chart(ctx, {
    type: 'line', //Tipo de linea
    data: data,
    options: opcions
});
///////////////////////////////////////////////////////////////////////// POST TO THE IP /////////////////////////////////////////
//Recarga
function updatey() {
    formElem.onsubmit = async(e) => {
        e.preventDefault();

        let response = await fetch('http://' + ip + '/changevalue', {
            method: 'POST',
            body: new FormData(formElem)
        });
        console.log(response)
    };
    newlabels = [0]
    ton = document.getElementById('ton').value
    toff = document.getElementById('toff').value
    pulso = document.getElementById('pulso').value
    toff = parseInt(toff)
    ton = parseInt(ton)
    pulso = parseInt(pulso)
        /////////////////////////////////////////////////////////////////// TODO: Delete this, replace for the actual graphic charts
    for (var p = 1; p <= pulso; p++) {
        A = (ton * (p - 1)) + toff * (p - 1)
        B = (ton * (p - 1)) + (toff * (p - 1) + 1)
        C = (ton * p) + ((p - 1) * toff) + 1
        D = (ton * p) + ((p - 1) * toff) + 1
        newlabels.push(A)
        newlabels.push(B)
        newlabels.push(C)
        newlabels.push(D)
    }
    newlabels.push((ton + toff) * 50)
        /////////////////////////////////////////7
    if (ton <= 100 && pulso == 1) {
        newdatay = [0, 0, 800, 800, 0, 0, 800, 800, 0, 0, 800, 800, 0, 0, 0] //eje y 
        newlabels = [-1, 0, ton, ton, ton + 1, (ton + toff) * 50] //eje x
    } else if (ton > 100 && pulso == 1) {
        newlabels = [-1, 0, ton, ton, ton + 1, (ton + toff) * 50] //eje x
    } else if (ton >= 1 && pulso > 1) {
        newlabels
    } else if (pulso == 0) {
        newlabels = []
    }
    //////////////////////////////////////////////////////////
    newdatay = [0, 800, 800, 800, 0, 0, 800, 800, 0, 0, 800, 800, 0, 0, 800, 800, 0, 0, 800, 800, 0, 0, 800, 800, 0, 0, 800, 800, 0, 0, 800, 800, 0, 0, 800, 800, 0, 0, 800, 800, 0, 0, 800, 800, 0, 0, 800, 800, 0, 0, 800, 800, 0, 0] //ejey
        //llamo al objeto
    chart.data.datasets[0].data = newdatay; //selecciono el primer data set data de eje y
    chart.data.labels = newlabels //seleciono los labels eje x
    chart.update(); //recargo al grafico con la funcion
    // console.log(newdatay)
    // console.log(newlabels)
};

function ipconfig() {

    swal("Ingrese IP ejemplo 192.168.1.13 :", {
            content: "input",
        })
        .then((value) => {
            swal(`Ip: ${value}`);
            ip = value

        });
}
