
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

#funcion para modificar los datos del susario segun el evento que se de
def updateFirebase(usuario, evento):
    campo = ''
    fb_user=db.collection('location').where('user','==', usuario).get()
    print(fb_user[0].to_dict())

    if evento==1:
        campo = 'subir'
    elif evento == 2:
        campo = 'levantar'
    elif evento == 3:
        campo = 'caer'

    db.collection('location').document(fb_user[0].id).update({campo:True})
#-----------------------------------------------------------------------------


cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred)
db = firestore.client()



