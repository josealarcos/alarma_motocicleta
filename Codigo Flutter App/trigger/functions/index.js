const functions = require('firebase-functions');
const admin = require('firebase-admin');

admin.initializeApp();



exports.alarmoto = functions.firestore
    .document('location/{docId}')
    .onUpdate((change, context) => {
        const doc = change.after.data();
        const prevDoc = change.before.data();
        var msg;
        const token = doc.devtoken;
        var isNotofication=false;

        if(doc.subir == true && prevDoc.subir == false){
            msg = 'Alguien se ha subido a tu moto';
            isNotofication=true;
        }
        if(doc.caer == true && prevDoc.caer == false){
            msg = 'Tu moto se ha caido';
            isNotofication=true;
        }
        if(doc.levantar == true && prevDoc.levantar == false){
            msg = 'Cuidado, han levantado tu moto del suelo. Puden estar robandola';
            isNotofication=true;
        }
        if(doc.location.latitude != prevDoc.location.latitude || doc.location.longitude != prevDoc.location.longitude){
            //si ademas de cambiar la localizacion se ha registrado uno de los eventyos anteriores
            //añadimos este a la notificacion junto al anterior
            if(isNotofication){
                msg += '. Ademas hemos detectado que ha cambiado la localización';
            }else{
                msg = 'Hemos detectado un cambio de localización en tu moto';
                isNotofication = true;
            }
        }
        const payload = {
            "notification": {
                "title": 'Alarmoto',
                "body": msg,
                "sound": "default"
            }
        };

        //si existe un evento por el que notificar retrnamos notificacion, si no devolvemos false
        if(isNotofication){
            return admin.messaging().sendToDevice(token, payload);
        }else{
            return isNotofication;
        }
        

    });
