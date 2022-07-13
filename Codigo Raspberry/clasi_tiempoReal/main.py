from mpu6050 import mpu6050
import time
import numpy as np
import RPi.GPIO as GPIO
from datetime import datetime as dt
import fcs_firebase as frb
import fcs_clasi_randomTree as cl
import fcs_gps as gps
import alarma



#FUNCION PRINCIPAL DE EJECUCION DE LA ALARMA EN TIEMPO REAL
def principal():
	global user
	print("COMIENZA PRINCIPAL")
	#modificamos ambas variables en firebase
	frb.updateEjecucion(user,ejecucion,0) #0 para modificar "ejecucion" en firebase
	frb.updateEjecucion(user,ejecucion,1) #1 para modificar "detenerEj" en firebase
	#reseteamos variables de firebase
	frb.iniFirebase(user)
	#definimos acelerometo con su address
	mpu = mpu6050(0x68)
	#definimos la constante que servirá como amplificador de los datos del acelerometro
	amp=2
	#establecemos los offsets para c)
	accel_data = mpu.get_accel_data()
	gyro_data = mpu.get_gyro_data()
	ax_o = accel_data['x']**amp
	ay_o = accel_data['y']**amp
	az_o = accel_data['z']**amp
	gx_o = gyro_data['x']**amp
	gy_o = gyro_data['y']**amp
	gz_o = gyro_data['z']**amp
	#definimo arrays para alamcenar los datos captados
	ax=[];ay=[];az=[]
	gx=[];gy=[];gz=[]
	#obtenemos la posicion actual mediante el modulo gps y la modificamos en firebase
	try:
		posicion = gps.getPosGps()
		frb.updatePosFb(user, posicion[0],posicion[1])
		print(str(posicion[0])+str(posicion[1]))
	except:
		print('Error puerto USB0(GPS)')

	#creamos bucle infinito que vaya captando datos y realizanod los test
	while ejecucion:
		accel_data = mpu.get_accel_data()
		gyro_data = mpu.get_gyro_data()
		if len(ax)<40: #llenamos el array hasta 28 elementos, asi se ajustará a nuestro modelo entrenado
			ax.append(accel_data['x']**amp-ax_o)
			ay.append(accel_data['y']**amp-ay_o)
			az.append(accel_data['z']**amp-az_o)
		if len(gx)<40:
			gx.append(gyro_data['x']**amp-gx_o)
			gy.append(gyro_data['y']**amp-gy_o)
			gz.append(gyro_data['z']**amp-gz_o)

		print(str(ax[len(ax)-1]) +', '+ str(ay[len(ay)-1]) +', '+ str(az[len(az)-1]) +'  ||  '
        	+ str(gx[len(gx)-1]) +', '+ str(gy[len(gy)-1]) +', '+ str(gz[len(gz)-1]))

		if len(ax)==40 and len(gx)==40:
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
	        	- 1º activaremos alarma
	        	- 2º modificaremos el campo correspondiente en firebase (llamando a
	        	    la funcion creada en el archivo fcs_firebase)
	        	- 3ºactualizamos la posicion gps y la modificamos en firebase'''
			if predi[0]==1:
				alarma.alarma(predi[0])
				frb.updateFirebase(user, 1)
				posicion = gps.getPosGps()
				frb.updatePosFb(user, posicion[0],posicion[1])
			elif predi[0]==2:
				alarma.alarma(predi[0])
				frb.updateFirebase(user, 2)
				posicion = gps.getPosGps()
				frb.updatePosFb(user, posicion[0],posicion[1])
			elif predi[0]==3:
				alarma.alarma(predi[0])
				frb.updateFirebase(user, 3)
				posicion = gps.getPosGps()
				frb.updatePosFb(user, posicion[0],posicion[1])
		time.sleep(0.1)

#funcion para iniciar la deteccion en tiempo real de la alarma o detenerla
def iniFin(channel):
	global ejecucion
	if(ejecucion):
		if(not frb.isEjecutando(user)): #si el pulsador esta desbloqueado en fb
			ejecucion=False
			alarma.activar(3)
			print("TERMINA PROGRAMA")
			frb.updateEjecucion(user,ejecucion,0) #0 para modificar "ejecucion" en firebase
	else:
		ejecucion=True
		alarma.activar(2)
		print("EMPIEZA PROGRAMA")





#-----------------------------------------------------------
#MAIN:
#usuario de firebase sobre el que modificaremos
user = "jose.alarcosnavarro@gmail.com"
#establecemos los valores de jecuciond e la alarma inciales el firebase
frb.updateEjecucion(user,False,0) #0 para modificar "ejecucion" en firebase
frb.updateEjecucion(user,False,1) #1 para modificar "detenerEj" en firebase

ejecucion = False #True si principal() se está ejecutando
pulsador=26
buzz=21
GPIO.setmode(GPIO.BCM)
GPIO.setup(pulsador, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(buzz, GPIO.OUT)
GPIO.add_event_detect(pulsador, GPIO.RISING, callback = iniFin,bouncetime=10000)
alarma.activar(4) #para saber que ya ha arrancado el porgrama

while True:
	if(ejecucion):
		principal()
