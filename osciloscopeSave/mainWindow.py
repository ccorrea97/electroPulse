import sys
from tkinter import ttk, Tk, Menu
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.animation as animation
import pyvisa as visa

class MainWindow(Tk):
    def __init__(self):
        super().__init__()

        self.wm_title("Real Time Oscilloscope")  # wm_title o title
        self.geometry('1600x650') # tendrá que ser responsive?

        # Variables
        self.status = 0
        self.counter = 0 # Porque queremos guardar los distintos .csv
        self.myScope = None
        self.tiemposave = []
        self.voltage = []
        self.frame_plasma1, self.frame_plasma2, self.frame_power, self.frame_energy_per_pulse, self.frame_total_energy = None, None, None, None, None

        # Llamada a las Funciones
        self.create_notebook_and_tabs()
        self.create_menu()
        self.oscilloscope_config()
        self.open_oscilloscope()
    
    def create_notebook_and_tabs(self):
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(pady=10, expand=True)

        self.frame_plasma1 = ttk.Frame(self.notebook)
        self.frame_plasma2 = ttk.Frame(self.notebook)
        self.frame_power = ttk.Frame(self.notebook, width=1400, height=490)
        self.frame_energy_per_pulse = ttk.Frame(self.notebook, width=1400, height=490)
        self.frame_total_energy = ttk.Frame(self.notebook, width=1400, height=490)

        #Para que sea responsive
        self.frame_plasma1.pack(fill='both', expand=True)
        self.frame_plasma2.pack(fill='both', expand=True)
        self.frame_power.pack(fill='both', expand=True)
        self.frame_energy_per_pulse.pack(fill='both', expand=True)
        self.frame_total_energy.pack(fill='both', expand=True)

        self.notebook.add(self.frame_plasma1, text='Plasma Curve 2') #channel1(channel2) - y, x
        self.notebook.add(self.frame_plasma2, text='Plasma Curve 1') #channel2(channel1) 
        self.notebook.add(self.frame_power, text='Power Curve') #channel1 * channel2
        self.notebook.add(self.frame_energy_per_pulse, text='Energy per Pulse Curve') #energía por pulso, integral Simpson
        self.notebook.add(self.frame_total_energy, text='Total Energy Curve') #energía total, sumatoria Ep

    def create_menu(self):
        menubar = Menu(self)
        self.config(menu=menubar)

        commands_menu = Menu(menubar, tearoff=0)
        commands_menu.add_command(label='Start', command=self.start)
        commands_menu.add_command(label='Stop',  command=self.stop)
        commands_menu.add_command(label='Save',  command=self.save)
        commands_menu.add_separator()
        commands_menu.add_command(label='Exit', command=self.destroy)
        menubar.add_cascade(label="Commands", menu=commands_menu)

    def start(self):
        self.status = 1
    
    def stop(self):
        self.status = 0

    def save(self):
        self.counter = self.counter + 1
        np.savetxt("datos" + str(self.counter) + ".csv", (self.tiemposave, self.voltage), delimiter=";")

    def selected_tab(self):
        return self.notebook.index("current")

    def oscilloscope_config(self):
       
        # self.info_footer=Label(frame, text="Digital Oscilloscope 2GHz 10GSa/s", bg = 'lightblue', font = ('Arial',9), fg = "darkblue")
        # self.info_footer.place(x = 1250, y = 515)
        
        ################# #1 PLASMA 2 (CH1(CH2))
        
        self.fig, ax = plt.subplots()
        #Color de fondo
        #ax2.set_ylim(-100, 1000) -original
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

        self.plasma_curve2, = ax.plot([], [], color='darkblue')

        self.canvas = FigureCanvasTkAgg(self.fig, master = self.frame_plasma1)
        self.canvas.get_tk_widget().pack(padx = 2, pady = 0, expand = True, fill = 'x')

        #################

        ################# #2 PLASMA 1 (CH2(CH1))
        self.fig2, axs = plt.subplots()
        #Color de fondo
        #ax2.set_ylim(-100, 1000) -original
        axs.set_ylim(-10, 20) #Consultar cuál sería la escala ideal, si vamos a trabajar con pequeños voltajes o muy grandes
        axs.set_xlim(0, 500e-09) #Por esto muestra el e-07 por el 500
        self.fig.patch.set_facecolor('lightblue')
        #Contorno de grafico
        axs.spines['bottom'].set_color('darkblue')
        axs.spines['top'].set_color('darkblue')
        axs.spines['left'].set_color('darkblue')
        axs.spines['right'].set_color('darkblue')
        #Color de ejes
        axs.tick_params(axis='x', colors='darkblue')
        axs.tick_params(axis='y', colors='darkblue')
        plt.title("RIGOL MSO8204 Real Time", color= 'darkblue', size=18, family="Arial")
        plt.xlabel("Channel 1", color= 'darkblue', size=18, family="Arial")
        plt.ylabel("Channel 2", color= 'darkblue', size=18, family="Arial")

        self.plasma_curve1, = axs.plot([], [], color='darkblue')

        self.canvas2 = FigureCanvasTkAgg(self.fig2, master = self.frame_plasma2)
        self.canvas2.get_tk_widget().pack(padx = 2, pady = 0, expand = True, fill = 'x')

        #################

        ################# #3 POWER (CH1XCH2)

        self.fig3, ax3 = plt.subplots()
        #Color de fondo
        #ax2.set_ylim(-100, 1000) -original
        ax3.set_ylim(-10, 20) #Consultar cuál sería la escala ideal, si vamos a trabajar con pequeños voltajes o muy grandes
        ax3.set_xlim(0, 500e-09)
        self.fig3.patch.set_facecolor('lightblue')
        #Contorno de grafico
        ax3.spines['bottom'].set_color('darkblue')
        ax3.spines['top'].set_color('darkblue')
        ax3.spines['left'].set_color('darkblue')
        ax3.spines['right'].set_color('darkblue')
        #Color de ejes
        ax3.tick_params(axis='x', colors='darkblue')
        ax3.tick_params(axis='y', colors='darkblue')
        plt.title("RIGOL MSO8204 Real Time", color= 'darkblue', size=18, family="Arial")
        plt.xlabel("Time [ns]", color= 'darkblue', size=18, family="Arial")
        plt.ylabel("Voltage [V]", color= 'darkblue', size=18, family="Arial")

        self.power_curve, = ax3.plot([], [], color='darkblue')

        self.canvas3 = FigureCanvasTkAgg(self.fig3, master = self.frame_power)
        self.canvas3.get_tk_widget().pack(padx = 2, pady = 0, expand = True, fill = 'x')

        #################

        ################# #4 ENERGY PER PULSE (SIMPSON INTEGRAL)
        self.fig4, ax4 = plt.subplots()
        #Color de fondo
        #ax2.set_ylim(-100, 1000) -original
        ax4.set_ylim(-10, 20) #Consultar cuál sería la escala ideal, si vamos a trabajar con pequeños voltajes o muy grandes
        ax4.set_xlim(0, 500e-09)
        self.fig4.patch.set_facecolor('lightblue')
        #Contorno de grafico
        ax4.spines['bottom'].set_color('darkblue')
        ax4.spines['top'].set_color('darkblue')
        ax4.spines['left'].set_color('darkblue')
        ax4.spines['right'].set_color('darkblue')
        #Color de ejes
        ax4.tick_params(axis='x', colors='darkblue')
        ax4.tick_params(axis='y', colors='darkblue')
        plt.title("RIGOL MSO8204 Real Time", color= 'darkblue', size=18, family="Arial")
        plt.xlabel("Time [ns]", color= 'darkblue', size=18, family="Arial")
        plt.ylabel("Voltage [V]", color= 'darkblue', size=18, family="Arial")

        self.energy_per_pulse_curve, = ax4.plot([], [], color='darkblue')

        self.canvas4 = FigureCanvasTkAgg(self.fig4, master = self.frame_energy_per_pulse)
        self.canvas4.get_tk_widget().pack(padx = 2, pady = 0, expand = True, fill = 'x')
        
        #################

        ################# #5 TOTAL ENERGY (SUM Ep)
        self.fig5, ax2 = plt.subplots()
        #Color de fondo
        #ax2.set_ylim(-100, 1000) -original
        ax2.set_ylim(-10, 20) #Consultar cuál sería la escala ideal, si vamos a trabajar con pequeños voltajes o muy grandes
        ax2.set_xlim(0, 500e-09)
        self.fig5.patch.set_facecolor('lightblue')
        #Contorno de grafico
        ax2.spines['bottom'].set_color('darkblue')
        ax2.spines['top'].set_color('darkblue')
        ax2.spines['left'].set_color('darkblue')
        ax2.spines['right'].set_color('darkblue')
        #Color de ejes
        ax2.tick_params(axis='x', colors='darkblue')
        ax2.tick_params(axis='y', colors='darkblue')
        plt.title("RIGOL MSO8204 Real Time", color= 'darkblue', size=18, family="Arial")
        plt.xlabel("Time [ns]", color= 'darkblue', size=18, family="Arial")
        plt.ylabel("Voltage [V]", color= 'darkblue', size=18, family="Arial")

        self.total_energy_curve, = ax2.plot([], [], color='darkblue')

        self.canvas5 = FigureCanvasTkAgg(self.fig5, master = self.frame_total_energy)
        self.canvas5.get_tk_widget().pack(padx = 2, pady = 0, expand = True, fill = 'x')
        
        #################

    def open_oscilloscope(self):
        resource_manager = visa.ResourceManager()
        instruments = resource_manager.list_resources()
        usb = list(filter(lambda x: 'USB' in x, instruments))
        
        if len(usb) < 1:
            print('No se localiza osciloscopio (USB).', instruments)
            sys.exit(-1)
        
        OSC_NAME = usb[0]
        print(OSC_NAME)
        self.myScope = resource_manager.open_resource(OSC_NAME)    

    def draw_graphic(self): # TODO: hacer una función con parámetros para evitar la repetición de código
        
        self.myScope.write(":WAVEFORM:FORMAT ASCII") #Para tener el encoding correcto
        

        ############### Curva Plasma 2 (Toma el ch1 como 'y' y ch2 como 'x' - (y, x))
        self.myScope.write("WAV:SOUR CHAN1")

        data_y = self.myScope.query("WAV:DATA?") #Datos extraidos
        #print(data) #TODO: eliminar
        data_y = data_y.split(',')
        data_y = list(data_y)
        data_y = data_y[10:len(data_y)-1]
        muestra = np.array(data_y)
        lista_sample = []
        for k in range(len(muestra)-1):
            lista_sample.append(float(muestra[k]))

        #Parametros Y graficar limpiar - Voltage
        y = [float(x) for x in lista_sample]

        self.myScope.write("WAV:SOUR CHAN2")
        data_x = self.myScope.query("WAV:DATA?") #Datos extraidos
        print(data_x) #TODO: eliminar
        data_x = data_x.split(',')
        data_x = list(data_x)
        data_x = data_x[10:len(data_x)-1]
        muestra = np.array(data_x)
        lista_sample = []
        for k in range(len(muestra)-1):
            lista_sample.append(float(muestra[k]))

        x = [float(i) for i in lista_sample]
        #Parametros Y graficar limpiar - Voltage
        #x = np.linspace([float(y) for y in lista_sample], num=len(y))
        # xoffset = float(self.myScope.query(":TIM:OFFS?"))
        # print(xoffset)
        # xscale = float(self.myScope.query(":TIM:SCAL?"))
        # print(xscale)
        # print(xoffset * xscale)
        # print(0.0000005+50e-09 * xscale)
        # x = np.linspace(xoffset * xscale, 0.0000005+50e-09 * xscale, num=len(y))

        # x =[5, 7, 8, 7, 2, 17, 2, 9,
        # 4, 11, 12, 9, 6] 
    
        # y =[5, 7, 8, 7, 2, 17, 2, 9,
        # 4, 11, 12, 9, 6]
        
        # plt.scatter(x, y, c ="blue")
        # plt.show()
        #self.plasma_curve2.set_data(x, y)
        ###############

        ############### Curva Plasma 1 (Toma el ch2 como 'y' y el ch1 (z) como 'x' - (y, x))
        self.myScope.write("WAV:SOUR CHAN2")

        data_y = self.myScope.query("WAV:DATA?") #Datos extraidos
        #print(data) #TODO: eliminar
        data_y = data_y.split(',')
        data_y = list(data_y)
        data_y = data_y[10:len(data_y)-1]
        muestra = np.array(data_y)
        lista_sample = []
        for k in range(len(muestra)-1):
            lista_sample.append(float(muestra[k]))

        #Parametros Y graficar limpiar - Voltage
        y = [float(x) for x in lista_sample]

        self.myScope.write("WAV:SOUR CHAN1")
        xoffset = float(self.myScope.query(":TIM:OFFS?"))
        xscale = float(self.myScope.query(":TIM:SCAL?"))
        x = np.linspace(xoffset * xscale, 0.0000005+50e-09 * xscale, num=len(y))
        self.plasma_curve1.set_data(x, y)
        ###############

        ############### Curva Potencia ((ch1 * ch2) como 'y' y el tiempo como 'x' - (y, x))
        # Tomar el Y del ch1 y el Y del ch2
        self.myScope.write("WAV:SOUR CHAN2")

        data_y = self.myScope.query("WAV:DATA?") #Datos extraidos
        #print(data) #TODO: eliminar
        data_y = data_y.split(',')
        data_y = list(data_y)
        data_y = data_y[10:len(data_y)-1]
        muestra = np.array(data_y)
        lista_sample = []
        for k in range(len(muestra)-1):
            lista_sample.append(float(muestra[k]))

        #Parametros Y graficar limpiar - Voltage
        y = [float(x) for x in lista_sample]

        self.myScope.write("WAV:SOUR CHAN1")
        xoffset = float(self.myScope.query(":TIM:OFFS?"))
        xscale = float(self.myScope.query(":TIM:SCAL?"))
        x = np.linspace(xoffset * xscale, 0.0000005+50e-09 * xscale, num=len(y))
        self.power_curve.set_data(x, y)
        ###############

        ############### Genérico para los otros tres gráficos que falta armar
        self.myScope.write("WAV:SOUR CHAN2")
        data_y = self.myScope.query("WAV:DATA?")
        data_y = data_y.split(',')
        data_y = list(data_y)
        data_y = data_y[10:len(data_y)-1] #Para quitar el header y el footer, que son qué¿?
        muestra = np.array(data_y)
        lista_sample = []
        
        for k in range(len(muestra)-1):
            lista_sample.append(float(muestra[k]))
        
        #Parametros Y graficar limpiar - Voltage
        y = [float(x) for x in lista_sample]
        #Parametros de tiempo
        timeoffset = float(self.myScope.query(":TIM:OFFS?"))
        timescale = float(self.myScope.query(":TIM:SCAL?"))
        time = np.linspace(timeoffset * timescale, 0.0000005+50e-09 * timescale, num=len(y))

        self.voltage = y
        self.tiemposave = time

        self.power_curve.set_data(time,y) #Importante, es el que pone la data
        self.energy_per_pulse_curve.set_data(time, y)
        self.total_energy_curve.set_data(time, y)
        
        if(self.status == 1):
            if(self.selected_tab() == 0):
                animation.FuncAnimation(self.fig, self.draw_graphic, interval = 10, blit = False)
                self.canvas.draw()
                print("Estoy en el 0") #TODO: eliminar
            elif(self.selected_tab() == 1):
                animation.FuncAnimation(self.fig2, self.draw_graphic, interval = 10, blit = False)
                self.canvas2.draw()
                print("Estoy en el 1") #TODO: eliminar
            elif(self.selected_tab() == 2):
                animation.FuncAnimation(self.fig3, self.draw_graphic, interval = 10, blit = False)
                self.canvas3.draw()
                print("Estoy en el 2") #TODO: eliminar
            elif(self.selected_tab() == 3):
                animation.FuncAnimation(self.fig4, self.draw_graphic, interval = 10, blit = False)
                self.canvas4.draw()
                print("Estoy en el 3") #TODO: eliminar
            elif(self.selected_tab() == 4):
                animation.FuncAnimation(self.fig5, self.draw_graphic, interval = 10, blit = False)
                self.canvas5.draw()
                print("Estoy en el 4") #TODO: eliminar
