from zipfile import ZIP_MAX_COMMENT
import numpy as np
from numpy.core.fromnumeric import transpose
from numpy.lib.npyio import zipfile_factory
import pandas as pd 
import matplotlib.pyplot as plt
from scipy import signal
import tkinter
from tkinter import StringVar, filedialog
from tkinter import ttk
import csv
global filename
filename = ""
global delta_t
delta_t = 1
global velprop
velprop = 1
global Zc
Zc = 1+2j
global faultdistance
faultdistance = 20
global combo


win = tkinter.Tk()


def UploadAction():
    global filename
    filename = filedialog.askopenfilename()
    

def FaultLoc():
    data = pd.read_csv(filename, delimiter=",") 

    print(data)

    data = data.replace(',','.', regex=True)

    ## SEÑALES DE CORRIENTE Y TENSIÓN#

    # Vector de tiempos
    time_vector = data.iloc[:,0].astype(float).to_numpy()

    # Señales de tensión/corriente
    current_deltaA = data.iloc[:, 1].astype(float).to_numpy()
    voltage_deltaA =data.iloc[ :,4].astype(float).to_numpy()

    current_deltaB = data.iloc[:, 2].astype(float).to_numpy()
    voltage_deltaB =data.iloc[ :,5].astype(float).to_numpy()

    current_deltaC = data.iloc[:, 3].astype(float).to_numpy()
    voltage_deltaC =data.iloc[ :,6].astype(float).to_numpy()

    print(voltage_deltaA)
    
    # ADC
    k = 1/(1.56e06/2)
    theta = 0

    # IMPEDANCIA CARACTERISTICA
    Z = (20.631 + 89.93j)/110
    Y = (676.75e-06j)/110

    # ZC = Zc
    ZC = np.sqrt(Z/Y)
    
    #  TRANSFORMACION MODAL

    w = 2*np.pi*60
    t = time_vector
    
    plt.plot(t, current_deltaB)
    plt.plot(t, current_deltaA)
    plt.plot(t, current_deltaC)

win.geometry("400x300")
win.title("Aplicación para localización de fallas - PF202130")

entry = tkinter.Entry(win)
entry.place(x = 50, y = 50)
entry2 = tkinter.Entry(win)
entry2.place(x = 50, y = 80)
entry3 = tkinter.Entry(win)
entry3.place(x = 50, y = 110)
entry4 = tkinter.Entry(win)
entry4.place(x = 50, y = 140)

def VarReading():
    global delta_t
    global velprop
    global Zc
    global faultdistance
    
    delta_t = entry.get()
    velprop = entry2.get()
    Zc = entry3.get()
    faultdistance = entry4.get()
    
button = tkinter.Button(win, text='Open', command=UploadAction)
button.pack()
buttonrun = tkinter.Button(win, text='Execute Program', command=lambda:[VarReading(), FaultLoc()])
buttonrun.pack()


widget_var = tkinter.StringVar()
combo = ttk.Combobox(win,textvariable=widget_var,values=["Señales de entrada", "Señales transformadas", "Ondas Viajeras", "Correlación"], state="readonly")
combo.set("Seleccione la gráfica...")
combo.place(x = 100, y = 140)

def Graph():
    value = combo.get()
    print(value)


buttongraph = tkinter.Button(win, text='Graficar', command=Graph)
buttongraph.pack()

win.mainloop()




