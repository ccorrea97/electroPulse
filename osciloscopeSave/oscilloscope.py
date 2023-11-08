import sys
import pyvisa as visa
import numpy as np

class Oscilloscope:
    def __init__(self, oscilloscope):
        self.oscilloscope = oscilloscope #self.open_oscilloscope()
        self.oscilloscope.write(":WAVEFORM:FORMAT ASCII")
        self.channel

    def open_oscilloscope():
        resource_manager = visa.ResourceManager()
        instruments = resource_manager.list_resources()
        usb = list(filter(lambda x: 'USB' in x, instruments))
        
        if len(usb) < 1:
            print('No se localiza osciloscopio (USB).', instruments)
            sys.exit(-1)
        
        OSC_NAME = usb[0]
        print(OSC_NAME)
        
        return resource_manager.open_resource(OSC_NAME)

    def channel1_data(self):
        self.channel = 1
        self.oscilloscope_data()
    def channel2_data(self):
        self.channel = 2
        self.oscilloscope_data()
    
    def oscilloscope_data(self):
        source = f"WAV:SOUR CHAN{self.channel}"
        self.oscilloscope.write(source)

        data = self.oscilloscope.query("WAV:DATA?") #Datos extraidos
        data = data.split(',')
        data = list(data)
        data = data[10:len(data)-1]
        muestra = np.array(data)
        lista_sample = []
        for k in range(len(muestra)-1):
            lista_sample.append(float(muestra[k]))

        return [float(x) for x in lista_sample]
    