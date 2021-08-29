
#TRATAMIENTO DE INFORMACION#

import numpy as np
import pandas as pd 
import matplotlib.pyplot as plt
from scipy import signal

data = pd.read_csv("Prueba_Vol_Cor_V2.csv", delimiter=";")     

flag = data.loc[data['All calculations'] == '0,020000'].index[0]

data = data.replace(',','.', regex=True)

## SEÑALES DE CORRIENTE Y TENSIÓN#
current_deltaA = data.iloc[flag:, [0,2]].astype(float).to_numpy()
voltage_deltaA =data.iloc[ flag:,[0,4]].astype(float).to_numpy()

current_deltaB = data.iloc[flag:, [0,3]].astype(float).to_numpy()
voltage_deltaB =data.iloc[ flag:,[0,5]].astype(float).to_numpy()

current_deltaC = data.iloc[flag:, [0,4]].astype(float).to_numpy()
voltage_deltaC =data.iloc[ flag:,[0,6]].astype(float).to_numpy()


#FILTER
#   # Cut-off frequency of the filter
w = 0.8 # Normalize the frequency
b1, a1 = signal.butter(5, w, 'low')
outputA = signal.filtfilt(b1, a1, current_deltaA,axis=0)

b2, a2 = signal.butter(5, w, 'low')
outputB = signal.filtfilt(b2, a2, current_deltaB,axis=0)

b3, a3 = signal.butter(5, w, 'low')
outputC = signal.filtfilt(b3, a3, current_deltaC,axis=0)

#ADC
delta_t = 1e-04
k = 1/ (1.56e06/2)
theta = 0

# IMPEDANCIA CARACTERISTICA
Z = 20.631 + 89.93j
Y = 676.75e-06j

# ZC = np.sqrt(Z/Y)

# print(ZC)

#  TRANSFORMACION MODAL

phi = k*delta_t*2*np.pi*60 + theta

T_dq0 = (2/3) * np.array([[0.5, 0.5, 0.5],[np.cos(phi),np.cos(phi-np.pi), np.cos(phi+np.pi) ],
[-np.sin(phi),-np.sin(phi-np.pi), -np.sin(phi+np.pi)]])

outputA_fft = np.fft.fft(outputA[:,1])
outputB_fft = np.fft.fft(outputB[:,1])
outputC_fft = np.fft.fft(outputC[:,1])

w = 2*np.pi*60
t = outputA[:,0]
print(outputA_fft)

outputA_sym = np.abs(outputA_fft)*np.cos(w*t+np.angle(outputA_fft))
outputB_sym = np.abs(outputB_fft)*np.cos(w*t+np.angle(outputB_fft))
outputC_sym = np.abs(outputC_fft)*np.cos(w*t+np.angle(outputC_fft))


# output_modal = output*T_dq0

# print(output_modal)



# print(transform_Matrix)
# # ONDAS VIAJERAS DE LLEGADA Y SALIDA

# current_delta_transform = (1/3)*current_delta.dot(transform_Matrix)
# voltage_delta_transform = (1/3)*voltage_delta.dot(transform_Matrix)

# S1 = voltage_delta_transform + ZC*current_delta_transform 
# S2 = voltage_delta_transform - ZC*current_delta_transform 

# print(voltage_delta_transform)

# plt.plot(current_deltaA[:,0],current_deltaA[:,1])
# plt.plot(outputA[:,0],outputA[:,1])

plt.plot(t, current_deltaB[:,1])
plt.plot(t,outputB[:,1])
plt.xlabel('Time(s)')
plt.ylabel('Current(kA)')
plt.show()

# Comentario de Prueba #2


