import os
import time
import firebase_admin
from firebase_admin import credentials
from google.cloud import firestore
from firebase_admin import firestore

#funcion para resetear las variables booleanas que firebase(la ejecutaremos al princcipio)
def iniFirebase(usuario):
    try:
       fb_user=db.collection('location').where('user','==', usuario).get()
       db.collection('location').document(fb_user[0].id).update({'subir':False})
       db.collection('location').document(fb_user[0].id).update({'caer':False})
       db.collection('location').document(fb_user[0].id).update({'levantar':False})
    except:
       print("Error en fcs_firebase(iniFirebase)")




#funcion para modificar los datos del susario segun el evento que se de
def updateFirebase(usuario, evento):
    campo = ''
    try:
       fb_user=db.collection('location').where('user','==', usuario).get()

       if evento==1:
           campo = 'subir'
       elif evento == 2:
           campo = 'levantar'
       elif evento == 3:
           campo = 'caer'

       db.collection('location').document(fb_user[0].id).update({campo:True})
    except:
       print("Error en fcs_firebase (updateF..)")

#funcion para modificar la posicion gps en firebase
def  updatePosFb(usuario,lat,long):
    try:
       geop = firestore.GeoPoint(lat, long)
       fb_user=db.collection('location').where('user','==', usuario).get()
       db.collection('location').document(fb_user[0].id).update({'location':geop})
    except:
       print("Error en fcs_firebase (updatePosFb)")

#funcion para modificar el estado de ejecucion de la alarma: el campo "ejecucion" nrepresentará si la
#funcion principal() se encuentra en ejecucion, el campo "detenerEj" indicará si desde la aplicación se ha dado
#permiso para detener la ejecucion
def  updateEjecucion(usuario,mod,campo):
    if(campo==0):
    	campo="ejecucion"
    elif(campo==1):
    	campo="detenerEj"

    try:
       fb_user=db.collection('location').where('user','==', usuario).get()
       db.collection('location').document(fb_user[0].id).update({campo:mod})
       time.sleep(1)
    except:
       print("Error en fcs_firebase (updateEjecucion)")



#funcion para comprobar el estado de detenerEj en firebase
def  isEjecutando(usuario):
    try:
       fb_user=db.collection('location').where('user','==', usuario).get()
       p=fb_user[0].to_dict()
       return p['detenerEj']
    except:
       print("Error en fcs_firebase (isEjecucion)")




#-----------------------------------------------------------------------------


cred = credentials.Certificate("/home/pi/clasi_tiempoReal/serviceAccountKey.json")
firebase_admin.initialize_app(cred)
db = firestore.client()
#updateFirebase('jose.alarcosnavarro@gmail.com', 1)
#updatePosFb('jose.alarcosnavarro@gmail.com', 1.034,-3.56)
#iniFirebase('jose.alarcosnavarro@gmail.com')
