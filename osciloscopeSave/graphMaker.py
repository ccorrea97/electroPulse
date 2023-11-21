import sys
import tkinter as tk
from tkinter import ttk, Tk
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.animation as animation
import pyvisa as visa

class GraphMaker(Tk):
    def __init__(self):
        super().__init__()

        self.geometry("900x650")
        self.root_frame = ttk.Frame()
        self.root_frame.pack(fill='both', expand=True)

        self.myScope = self.open_oscilloscope()
        self.open_oscilloscope()
        self.fig, self.ax = plt.subplots()
        self.canvas = FigureCanvasTkAgg(self.fig, master = self.root_frame)
        self.canvas.get_tk_widget().pack(padx = 2, pady = 0, expand = True, fill = 'x')
        #self.create_plot() #TODO: delete
        self.axs = self.fig.add_subplot(111)
        self.graph, = self.ax.plot([], [], color='darkblue')

    #TODO: delete
    #No lo estoy llamando en ningún lado y anda
    # Gráfico de curvas
    def create_plot(self):
        self.fig, self.ax = plt.subplots()
        
        self.ax.set_ylim(-10, 20) #Consultar cuál sería la escala ideal, si vamos a trabajar con pequeños voltajes o muy grandes
        self.ax.set_xlim(0, 500e-09) #Por esto muestra el e-07 por el 500
        self.fig.patch.set_facecolor('lightblue')
        #Contorno de grafico
        self.ax.spines['bottom'].set_color('darkblue')
        self.ax.spines['top'].set_color('darkblue')
        self.ax.spines['left'].set_color('darkblue')
        self.ax.spines['right'].set_color('darkblue')
        #Color de ejes
        self.ax.tick_params(axis='x', colors='darkblue')
        self.ax.tick_params(axis='y', colors='darkblue')
        plt.title("RIGOL MSO8204 Real Time", color= 'darkblue', size=18, family="Arial")
        plt.xlabel("Channel 2", color= 'darkblue', size=18, family="Arial")
        plt.ylabel("Channel 1", color= 'darkblue', size=18, family="Arial")

        self.graph, = self.ax.plot([], [], color='darkblue')

        self.canvas = FigureCanvasTkAgg(self.fig, master = self.root_frame)
        self.canvas.get_tk_widget().pack(padx = 2, pady = 0, expand = True, fill = 'x')
    
    def draw_graph(self): 
        
        if (True): #(curva plasma 2)
            self.curva_plasma2() #Bien
        elif (False): #(curva plasma 1)
            self.curva_plasma1() #Bien
        elif (False): #(curva potencia)
            self.curva_potencia()
        elif (False): #(curva per pulse)
            self.curva_per_pulse()
        elif (False): #(curva total)
            self.curva_energia_total()
        elif (False): #(curva diferencia)
            self.curva_diferencia_pulsos()
        elif (True): #(tensión vs corriente -default)
            self.curva_tension_corriente() #No hace el gráfico correspondiente
        
        #TODO: delete
        if(False):
            animation.FuncAnimation(self.fig, self.draw_graph, interval = 10, blit = False)
            self.canvas.draw()

    def curva_plasma2(self):
        x = self.osciloscope_data(2)
        y = self.osciloscope_data(1)
        self.axs.cla()
        self.axs.scatter(x, y, color='darkblue')
        self.canvas.draw()

    def curva_plasma1(self):
        x = self.osciloscope_data(1)
        y = self.osciloscope_data(2)
        self.axs.cla()
        self.axs.scatter(x, y, color='darkblue')
        self.canvas.draw()

    def curva_potencia():
        a = ""
    
    def curva_per_pulse():
        a = ""
    
    def curva_energia_total():
        a = ""
    
    def curva_diferencia_pulsos():
        a = ""
    
    def curva_tension_corriente(self):
        #Todo en el canal 1
        y = self.osciloscope_data(1)
        x = self.get_time_axis(1)

        self.graph.set_data(x, y)
        animation.FuncAnimation(self.fig, self.draw_graph, interval = 10, blit = False)
        self.canvas.draw()

    def get_time_axis(self, channel):
        y = self.osciloscope_data(channel)
        self.myScope.write(f"WAV:SOUR CHAN{channel}")
        xoffset = float(self.myScope.query(":TIM:OFFS?"))
        xscale = float(self.myScope.query(":TIM:SCAL?"))
        print(f"xscale: {xscale}")
        print(f"xoffset: {xoffset}")
        return np.linspace(xoffset * xscale, 0.0000005+50e-09 * xscale, num=len(y))

    def osciloscope_data(self, channel):
        self.myScope.write(":WAVEFORM:FORMAT ASCII")
        self.myScope.write(f"WAV:SOUR CHAN{channel}")
        data = self.myScope.query("WAV:DATA?") #Marco: ver acá tema de formato, para ver cuántos puntos tomar -por
        #print(data)
        data = data.split(',')
        data = list(data)
        data = data[10:len(data)-1]
        #Idea Marco: pasar directamente al float con numpy y evitar pasar a mano
        #muestra = np.fromstring(data, dtype = float, sep = ',') #ver cómo estaba
        muestra = np.array(data).astype(float)
        print(muestra)
        # lista_sample = [] #TODO: delete
        # for k in range(len(muestra)-1): #TODO: delete
        #     lista_sample.append(float(muestra[k])) #TODO: delete
        #print([float(i) for i in lista_sample]) #TODO: delete
        return muestra

        #TODO: delete
        
        # self.myScope.write(":WAVEFORM:FORMAT ASCII")
        # self.myScope.write(f"WAV:SOUR CHAN{channel}")
        # data = self.myScope.query("WAV:DATA?") #Datos extraidos
        # data = data.split(',')
        # data = list(data)
        # data = data[10:len(data)-1]
        # muestra = np.array(data)
        # lista_sample = []
        # for k in range(len(muestra)-1):
        #     lista_sample.append(float(muestra[k]))

        # return [float(i) for i in lista_sample]

    def open_oscilloscope(self):
        resource_manager = visa.ResourceManager()
        instruments = resource_manager.list_resources()
        print(instruments)
        usb = list(filter(lambda x: 'USB' in x, instruments))
        
        if len(usb) < 1:
            print('No se localiza osciloscopio (USB).', instruments)
            sys.exit(-1)
        
        OSC_NAME = usb[0]
        return resource_manager.open_resource(OSC_NAME)