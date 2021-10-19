from zipfile import ZIP_MAX_COMMENT
import numpy as np
from numpy.core.fromnumeric import transpose
from numpy.lib.npyio import zipfile_factory
import pandas as pd 
import matplotlib.pyplot as plt
from scipy import signal
import tkinter
from tkinter import StringVar, filedialog, Canvas, ttk
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
# Implement the default Matplotlib key bindings.
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure

import csv
global filename
filename = ""
global delta_t
delta_t = 1
global velprop
velprop = 1
global Zc
Zc = 1
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

win.geometry("1280x720")
win.title("Aplicación para localización de fallas - PF202130")


label1 = tkinter.Label(win,text = "Ingrese el valor de la frecuencia de muestreo:").place(x = 20, y = 50)  
label2 = tkinter.Label(win,text = "Ingrese el valor de la velocidad de propagación:").place(x = 20, y = 80) 
label3 = tkinter.Label(win,text = "Ingrese el valor de la impedancia característica:").place(x = 20, y = 110) 
label4 = tkinter.Label(win,text = "Ingrese la distancia de falla:").place(x = 20, y = 140) 
label5 = tkinter.Label(win,text = "Programa para la localización de fallas utilizando ondas viajeras:", font=('Helvetica', 18, 'bold')).place(x = 360, y = 10)  


entry = tkinter.Entry(win)
entry.place(x = 280, y = 50)
entry2 = tkinter.Entry(win)
entry2.place(x = 280, y = 80)
entry3 = tkinter.Entry(win)
entry3.place(x = 280, y = 110)
entry4 = tkinter.Entry(win)
entry4.place(x = 280, y = 140)

def VarReading():
    global delta_t
    global velprop
    global Zc
    global faultdistance
    
    delta_t = entry.get()
    velprop = entry2.get()
    Zc = entry3.get()
    faultdistance = entry4.get()
    
button = tkinter.Button(win, text='Abrir archivo .csv', command=UploadAction)
button.place(x = 1120, y = 50)
buttonrun = tkinter.Button(win, text='Ejecutar Script', command=lambda:[VarReading(), FaultLoc()])
buttonrun.place(x = 1130, y = 80)


widget_var = tkinter.StringVar()
combo = ttk.Combobox(win,textvariable=widget_var,values=["Señales de entrada", "Señales transformadas", "Ondas Viajeras", "Correlación"], state="readonly")
combo.set("Seleccione la gráfica...")
combo.place(x = 1100, y = 140)

def Graph():
    value = combo.get()
    if value == "Señales de entrada":
        print(value)
        fig = Figure(figsize=(6, 6), dpi=100)
        t = np.arange(0, 3, .01)
        plot1 = fig.add_subplot(111)
        plot1.plot(t, 2 * np.sin(2 * np.pi * t), 'r', t,2 * np.cos(2 * np.pi * t), 'b')
        canvas1 = FigureCanvasTkAgg(fig, master=win)  # A tk.DrawingArea.
        canvas1.draw()
        canvas1.get_tk_widget().pack(padx=350, pady=180)
        toolbar = NavigationToolbar2Tk(canvas1, win)
        toolbar.update()
        canvas1.get_tk_widget().pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=1)

    elif value == "Señales transformadas":
        print(value)
        fig = Figure(figsize=(6, 6), dpi=100)
        t = np.arange(0, 3, .01)
        plot1 = fig.add_subplot(111)
        plot1.plot(t, 2 * np.tan(2 * np.pi * t))
        canvas1 = FigureCanvasTkAgg(fig, master=win)  # A tk.DrawingArea.
        canvas1.draw()
        canvas1.get_tk_widget().pack(padx=350, pady=150)
        toolbar = NavigationToolbar2Tk(canvas1, win)
        toolbar.update()
        canvas1.get_tk_widget().pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=1)

    elif value == "Ondas Viajeras":
        print(value)
    elif value == "Correlación":
        print(value)


buttongraph = tkinter.Button(win, text='Realizar Gráfica', command=Graph)
buttongraph.place(x = 1125, y = 110)

win.mainloop()




