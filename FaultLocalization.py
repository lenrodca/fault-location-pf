
#TRATAMIENTO DE INFORMACION#

import numpy as np
import pandas as pd 
import matplotlib.pyplot as plt

data = pd.read_csv("Prueba_Vol_Cor_V2.csv", delimiter=";")     

flag = data.loc[data['All calculations'] == '0,020000'].index[0]

data = data.replace(',','.', regex=True)

## SEÑALES DE CORRIENTE Y TENSIÓN#
currents = data.iloc[1:,0:4]
voltages = data.iloc[1:,[0,4,5,6]]


current_ss = data.iloc[1:flag, 0:4].astype(float)
voltage_ss = data.iloc[1:flag,[0,4,5,6]].astype(float)

current_delta = data.iloc[flag:, 0:4].astype(float)
voltage_delta =data.iloc[ flag:,[0,4,5,6]].astype(float)

# IMPEDANCIA CARACTERISTICA
Z = 20.631 + 89.93j
Y = 676.75e-06j

ZC = np.sqrt(Z/Y)

print(ZC)

# TRANSFORMACION MODAL
MT = [(1,1,1),(2,-1,-1),(0,1/np.sqrt(3),-1/np.sqrt(3))]
transform_Matrix = pd.DataFrame(data=MT)

print(transform_Matrix)
# ONDAS VIAJERAS DE LLEGADA Y SALIDA

current_delta_transform = (1/3)*current_delta.dot(transform_Matrix)
voltage_delta_transform = (1/3)*voltage_delta.dot(transform_Matrix)

S1 = voltage_delta_transform + ZC*current_delta_transform 
S2 = voltage_delta_transform - ZC*current_delta_transform 

print(voltage_delta_transform)


current_ss.plot( x= 'All calculations' )
current_delta.plot(x='All calculations' )
plt.xlabel('Time(s)')
plt.ylabel('Current(kA)')
plt.show()

