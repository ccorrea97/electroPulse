import sys
import tkinter as tk
from tkinter import ttk, Tk, Menu
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.animation as animation
import pyvisa as visa
import pandas as pd

class GraphMaker(Tk):
    def __init__(self):
        super().__init__()

        self.geometry("900x650")
        self.root_frame = ttk.Frame()
        self.root_frame.pack(fill='both', expand=True)

        self.myScope = self.open_oscilloscope()
        self.open_oscilloscope()
        self.canvas_plot()
        



    

   
    
    
    # Gráfico de curvas
    def canvas_plot(self):
        self.fig, ax = plt.subplots()
        ax.set_ylim(-10, 20) #Consultar cuál sería la escala ideal, si vamos a trabajar con pequeños voltajes o muy grandes
        ax.set_xlim(0, 500e-09) #Por esto muestra el e-07 por el 500
        self.fig.patch.set_facecolor('lightblue')
        #Contorno de grafico
        ax.spines['bottom'].set_color('darkblue')
        ax.spines['top'].set_color('darkblue')
        ax.spines['left'].set_color('darkblue')
        ax.spines['right'].set_color('darkblue')
        #Color de ejes
        ax.tick_params(axis='x', colors='darkblue')
        ax.tick_params(axis='y', colors='darkblue')
        plt.title("RIGOL MSO8204 Real Time", color= 'darkblue', size=18, family="Arial")
        plt.xlabel("Channel 2", color= 'darkblue', size=18, family="Arial")
        plt.ylabel("Channel 1", color= 'darkblue', size=18, family="Arial")

        self.graph, = ax.plot([], [], color='darkblue')

        self.canvas = FigureCanvasTkAgg(self.fig, master = self.root_frame)
        self.canvas.get_tk_widget().pack(padx = 2, pady = 0, expand = True, fill = 'x')
    
    # Gráfico de puntos
    def canvas_scatter(self, x, y):
        self.fig = plt.Figure(figsize=(5, 4), dpi=100)
        self.ax = self.fig.add_subplot(111)
        self.ax.scatter(x, y, color='g')
        scatter = FigureCanvasTkAgg(self.fig, self.root_frame)
        scatter.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH)
        self.ax.set_ylabel('Tensión')
        self.ax.set_xlabel('Corriente')
        self.ax.set_title('Gráficos en tiempo real')

        self.canvas = FigureCanvasTkAgg(self.fig, master = self.root_frame)
        self.canvas.get_tk_widget().pack(padx = 2, pady = 0, expand = True, fill = 'x')
    
    def draw_graph(self):
        
        if (True): #(curva plasma 2)
            self.curva_plasma2()
        elif (False): #(curva plasma 1)
            self.curva_plasma1()
        elif (False): #(curva potencia)
            self.curva_potencia()
        elif (False): #(curva per pulse)
            self.curva_per_pulse()
        elif (False): #(curva total)
            self.curva_energia_total()
        elif (False): #(curva diferencia)
            self.curva_diferencia_pulsos()
        elif (True): #(tensión vs corriente -default)
            self.curva_tension_corriente()
        
        #plt.scatter(x, y, c = "blue")
        #self.graph.set_data(x, y) #plt.show()
        
        animation.FuncAnimation(self.fig, self.draw_graph, interval = 10, blit = False)
        self.canvas.draw()

        if(False):
            animation.FuncAnimation(self.fig, self.draw_graph, interval = 10, blit = False)
            self.canvas.draw()

    def curva_plasma2(self):
        x = self.osciloscope_data(2)
        y = self.osciloscope_data(1)
        self.canvas_scatter(x, y)

    def curva_plasma1(self):
        x = self.osciloscope_data(1)
        y = self.osciloscope_data(2)
        self.canvas_scatter(x, y)

    def curva_potencia():
        a = ""
    
    def curva_per_pulse():
        a = ""
    
    def curva_energia_total():
        a = ""
    
    def curva_diferencia_pulsos():
        a = ""
    
    def curva_tension_corriente(self):
        y = self.osciloscope_data(1)

        self.myScope.write("WAV:SOUR CHAN1")
        xoffset = float(self.myScope.query(":TIM:OFFS?"))
        xscale = float(self.myScope.query(":TIM:SCAL?"))
        x = np.linspace(xoffset * xscale, 0.0000005+50e-09 * xscale, num=len(y))

        self.graph.set_data(x, y)



    def osciloscope_data(self, channel):
        self.myScope.write(":WAVEFORM:FORMAT ASCII")
        self.myScope.write(f"WAV:SOUR CHAN{channel}")
        data = self.myScope.query("WAV:DATA?") #Datos extraidos
        data = data.split(',')
        data = list(data)
        data = data[10:len(data)-1]
        muestra = np.array(data)
        lista_sample = []
        for k in range(len(muestra)-1):
            lista_sample.append(float(muestra[k]))

        return [float(i) for i in lista_sample]

    def open_oscilloscope(self):
        resource_manager = visa.ResourceManager()
        instruments = resource_manager.list_resources()
        usb = list(filter(lambda x: 'USB' in x, instruments))
        
        if len(usb) < 1:
            print('No se localiza osciloscopio (USB).', instruments)
            sys.exit(-1)
        
        OSC_NAME = usb[0]
        return resource_manager.open_resource(OSC_NAME)