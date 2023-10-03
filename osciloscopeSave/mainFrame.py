from tkinter import StringVar, Tk, Frame, Button, Label, ttk, PhotoImage
import tkinter as tk
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

#Pyvisa Osciloscopio
import pyvisa as visa
import numpy

class MainFrame(Frame): #Clase principal llamada de las funciones secundarias
    def __init__(self, master,*args):
        super().__init__(master,*args)  # Especif.Ventana
        self.Layaout() 
        self.button_config()
        self.Config_osci()
        self.status = 0
        self.tiemposave=[]
        self.voltage=[]
        self.counter=0
    def Layaout(self):
        global frame4  #CAMARA
        global frame1 #Osciloscopio
        #Separo el layaout
 ########Seccion 1########################################
     
########Seccion2########################################### 
        frame1 = Frame(self.master,bg='lightblue',bd=2)
        frame1.grid(column=2,row=0, sticky='nsew')
   ###Seccion3###########################################
      
########Seccion4########################################### 
        frame4=Frame(self.master,bg='steelblue',bd=2) 
        frame4.grid(column=0,columnspan=2,row=0,sticky='nsew')
########Configuro columnas y filas del layout################
        self.master.columnconfigure(0,weight=1)
        self.master.columnconfigure(2,weight=6)
        self.master.rowconfigure(0,weight=8)
    def start(self):
        self.status=1
    def stop(self):
        self.status=0
    def save(self):
        self.counter=self.counter + 1
      #  print("Save archivo")
      #  print(self.voltage)
      #  print(self.tiemposave)
        numpy.savetxt("datos"+str(self.counter) + ".csv", (self.tiemposave, self.voltage), delimiter=";")
    def button_config(self):
        global frame4
        self.title=Label(frame4, text="  Setup",bg='steelblue',font=('Arial',15,'bold'),fg="white")
        self.title.place(x=0,y=3)
        self.start = Button(frame4,text='Start',font=('Arial',12,'bold'),width=12,bg='teal',fg='white',command=self.start)
        self.start.place(x=0,y=40)
        self.stop = Button(frame4,text='Stop',font=('Arial',12,'bold'),width=12,bg='teal',fg='white',command=self.stop)
        self.stop.place(x=0,y=90)
        self.save = Button(frame4,text='Save',font=('Arial',12,'bold'),width=12,bg='teal',fg='white',command=self.save)
        self.save.place(x=0,y=140)
    def Config_osci(self):
        global frame1,myScope

        self.fig2,ax2 = plt.subplots()
        #Color de fondo
        ax2.set_ylim(-100,1000)
        ax2.set_xlim(0,500e-09)
        self.fig2.patch.set_facecolor('lightblue')
        #Contorno de grafico
        ax2.spines['bottom'].set_color('darkblue')
        ax2.spines['top'].set_color('darkblue')
        ax2.spines['left'].set_color('darkblue')
        ax2.spines['right'].set_color('darkblue')
        #Color de ejes
        ax2.tick_params(axis='x', colors='darkblue')
        ax2.tick_params(axis='y', colors='darkblue')
        plt.title("RiGOL MSO8204 Real Time",color= 'darkblue',size=18,family="Arial")
        plt.xlabel("Time [ns]",color= 'darkblue',size=18,family="Arial" )
        plt.ylabel("Voltage [V]",color= 'darkblue',size=18,family="Arial" )

        self.line2, = ax2.plot([],[],color='darkblue')
        #Abre comuncicacion con osciloscopio 
        rm=visa.ResourceManager()
        #Direccionamiento osciloscopio
        osc='USB0::0x1AB1::0x0516::DS8A234200645::INSTR'
        #Abrir intrumento
        myScope = rm.open_resource(osc)
        self.canvas2= FigureCanvasTkAgg(self.fig2,master=frame1)
        self.canvas2.get_tk_widget().pack(padx=2,pady=0,expand=True,fill='x')
        self.info_footer=Label(frame1, text="Digital Oscilloscope 2GHz 10GSa/s",bg='lightblue',font=('Arial',9),fg="darkblue")
        self.info_footer.place(x=1250,y=515)

    def animate_osc(self):
        global myScope
        #Peticion de datos osciloscopio
        data=myScope.query("WAV:DATA?")#Datos extraidos
        data=data.split(',') #Datos array separación
        data= list(data) #Datos del osciloscopio 
      #  print(data)
        data=data[10:len(data)-1]
        muestra=np.array(data)
        lista_sample=[]
        for k in range(len(muestra)-1):
            lista_sample.append(float(muestra[k]))
        #Parametros Y graficar limpiar - Voltage
        y= [float(x) for x in lista_sample]
        #Parametros de tiempo
        timeoffset = float(myScope.query(":TIM:OFFS?")[0])
        timescale = float(myScope.query(":TIM:SCAL?"))
        time = numpy.linspace(timeoffset  * timescale, 0.0000005+50e-09 * timescale, num=len(y))
        self.line2.set_data(time,y)
        self.voltage = y
        self.tiemposave= time
       # print(self.voltage)
       # print(self.tiemposave)
        if(self.status == 1):
             animation.FuncAnimation(self.fig2,self.animate_osc,interval=10,blit=False)
             self.canvas2.draw()
