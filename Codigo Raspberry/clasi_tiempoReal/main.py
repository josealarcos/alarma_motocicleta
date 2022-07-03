import fcs_clasi_randomTree as cl
import fcs_firebase as frb
import serial
import time
import numpy as np
#usuario de firebase sobre el que modificaremos 
user = "jose.alarcosnavarro@gmail.com"


'''1ª PARTE: cogemos datos para formar lista test.
Lista test tendra que tener las suigientes caractrísticas:
    ax,ay,az --> length = 28
    gx,gy,gz --> length = 29
Al unirlas deberá quedar una lista(que representará los datos de la moto en ese momento) de 
171 elementos con la que pasaremos el test al modelo entrenado en el archivo fcs_clasi_randomTree
'''
#definimo arrays para alamcenar los datos captados
ax=[];ay=[];az=[]
gx=[];gy=[];gz=[]
#creamos conexion serie con arduino
arduino = serial.Serial("COM4",57600)
time.sleep(1)
#creamos bucle infinito que vaya captando datos y realizanod los test
while True:
    val = arduino.readline().decode('ascii')
    val = val[:-2]#para quitarle los caracteres de fin de linea \r\n
    cad = val.split(",")
    if cad[0] == "a" and len(ax) < 28:
        ax.append(cad[1])
        ay.append(cad[2])
        az.append(cad[3])
        print(val)
    elif cad[0] == "g" and len(gx) < 29:
        gx.append(cad[1])
        gy.append(cad[2])
        gz.append(cad[3])
        print(val)
    if len(ax)==28 and len(gx)==29:
        #creamos matriz para test
        aux = ax+ay+az+gx+gy+gz
        aux1 = [aux,aux]
        test = np.array(aux1)
        predi = cl.rf.predict(test)
        print("-----PREDICCION MOVIMIENTO:---------> " + str(predi[0])) 
        #reseteamos las listas
        ax=[];ay=[];az=[]
        gx=[];gy=[];gz=[]
        '''Si la prediccion es 1, 2 o 3 signofica que se ha producido un evento:
                - 1º enviaremos el evento al arduino
                - 2º modificaremos el campo correspondiente en firebase (llamando a
                    la funcion creada en el archivo fcs_firebase)'''
        if predi[0]==1: 
            arduino.write(b'1')
            frb.updateFirebase(user, 1)
        elif predi[0]==2:
            arduino.write(b'2')
            frb.updateFirebase(user, 2)
        elif predi[0]==3:
            arduino.write(b'3')
            frb.updateFirebase(user, 3)









'''2ª PARTE: una vez creada la matriz realizamos el test con nuestro modelo de forma que 
prediga el tipo de evento que se está dando'''
y_predi = cl.rf.predict(cl.x_test) 
#ahora vamos a evaluar los aciertos y fallos de nuestro modelo
from sklearn.metrics import accuracy_score
acc = accuracy_score(cl.y_test,y_predi)
print(acc)
comp = cl.pd.DataFrame({'real': cl.y_test, 'preds':y_predi})
print(comp)
