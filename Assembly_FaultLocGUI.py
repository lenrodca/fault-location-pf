import numpy as np
from numpy.core.fromnumeric import transpose
import pandas as pd 
import matplotlib.pyplot as plt
from scipy import signal

import tkinter
from tkinter import filedialog
import csv
win = tkinter.Tk()


def UploadAction(delta_t):
    global strfilename
    filename = filedialog.askopenfilename()
    FaultLoc(filename)
    print(delta_t)


win.geometry("400x300")
win.title("Aplicación para localización de fallas - PF202130")
entry = tkinter.Entry(win)
entry.place(x = 50, y = 50)
delta_t = entry.get
button = tkinter.Button(win, text='Open', command=UploadAction(delta_t))
button.pack()

def FaultLoc(filename):
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
    
    # # ADC
    # k = 1/ (1.56e06/2)
    # theta = 0

    
    # ZC = np.sqrt(Z/Y)

    # # print(ZC)

    # #  TRANSFORMACION MODAL

    # w = 2*np.pi*60
    # t = time_vector

    

win.mainloop()



