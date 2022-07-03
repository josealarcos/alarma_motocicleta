// ignore_for_file: prefer_const_constructors, deprecated_member_use, avoid_print, prefer_typing_uninitialized_variables

import 'package:flutter/material.dart';
import 'package:firebase_auth/firebase_auth.dart';
import 'package:google_maps_flutter/google_maps_flutter.dart';
import 'package:geolocator/geolocator.dart';
import 'package:cloud_firestore/cloud_firestore.dart';
import 'package:provider/provider.dart';
import 'package:prueba1/stream/user.dart';
import 'package:firebase_messaging/firebase_messaging.dart';
import 'package:clipboard/clipboard.dart';
//import 'package:flutter_local_notifications/flutter_local_notifications.dart';

class HomePage extends StatefulWidget {
  HomePage({Key? key}) : super(key: key);

  @override
  _HomePageState createState() => _HomePageState();
}

class _HomePageState extends State<HomePage> {
  //DECLARAMOS VARIABLES
  GoogleMapController? myController;
  bool isPosAct = false;
  var posicionActual;
  var auxi = [];
  var userActual = FirebaseAuth.instance.currentUser!.email;
  List<Marker> markers = [];

  //FUNCIONES AUXILIARES ANTES DE BUILD
  @override
  initState() {
    super.initState();
    //inicializamos posicion y usuario logeado
    Geolocator.getCurrentPosition().then((posAct) {
      //getUserLoc();
      setState(() {
        posicionActual = posAct;
        isPosAct = true;
      });
    });
    setToken();
  }

  addMarker(lat, lon) {
    markers = [];
    markers.add(Marker(
      icon: BitmapDescriptor.defaultMarker,
      infoWindow: InfoWindow(title: "Moto location"),
      markerId: MarkerId('Posicion ' + markers.length.toString()),
      draggable: false,
      onTap: () {
        print("marker tocado");
        FlutterClipboard.copy(lat.toString() + ', ' + lon.toString());
      },
      position: LatLng(lat, lon),
    ));
  }

  void crearMapa(controller) {
    setState(() {
      myController = controller;
    });
  }

  aux(lat, long) {
    myController!.animateCamera(
      CameraUpdate.newCameraPosition(
        CameraPosition(target: LatLng(lat, long), zoom: 15.5),
      ),
    );
  }

  cargarPos(lat, long) {
    addMarker(lat, long);
    CameraPosition cameraPos =
        CameraPosition(target: LatLng(lat, long), zoom: 15.5);
    if (myController != null) {
      aux(lat, long);
    }
    return Container(
        height: MediaQuery.of(context).size.height * 0.5,
        width: double.infinity,
        child: GoogleMap(
          //si tenemos posicion entonces..
          initialCameraPosition: cameraPos,
          markers: Set.from(markers),
          onMapCreated: (GoogleMapController controller) async {
            myController = controller;
          },
        ));
  }

  getUserLoc() {
    //almacenamos las coordenadas de firebase en auxi
    FirebaseFirestore.instance
        .collection('location')
        .where('user', isEqualTo: userActual)
        .get()
        .then((QuerySnapshot querySnapshot) {
      for (var doc in querySnapshot.docs) {
        auxi.add(doc["location"].latitude);
        auxi.add(doc["location"].longitude);
        addMarker(doc["location"].latitude, doc["location"].longitude);
      }
    });
  }

  setToken() async {
    //fc para establecer el token del dispositivo en firestore del usuario
    String? token = await FirebaseMessaging.instance.getToken();
    FirebaseFirestore.instance
        .collection('location')
        .where('user', isEqualTo: userActual)
        .get()
        .then((QuerySnapshot querySnapshot) {
      for (var doc in querySnapshot.docs) {
        String id = doc.id;
        FirebaseFirestore.instance
            .collection('location')
            .doc(id)
            .update({'devtoken': token});
      }
    });
  }

  //stream para escuchar escuchar cambios en la base de datos de firebase
  Stream<QuerySnapshot> get events {
    return FirebaseFirestore.instance.collection('location').snapshots();
  }

  //COMIENZA FC BUILD
  @override
  Widget build(BuildContext context) {
    List<Usuario> userList = Provider.of<List<Usuario>>(context);

    return Scaffold(
      appBar: AppBar(
        shadowColor: Colors.blueGrey,
        backgroundColor: Colors.black54,
        title: Text("Alarmoto"),
      ),
      body: Center(
        child: ListView.builder(
          itemCount: userList.length + 2,
          itemBuilder: (BuildContext context, int index) {
            if (index == userList.length + 1) {
              //último widget que aparecerá
              return OutlineButton(
                borderSide: BorderSide(
                    color: Colors.red, style: BorderStyle.solid, width: 3.0),
                child: Text('Log out'),
                onPressed: () {
                  FirebaseAuth.instance.signOut().then((value) {
                    Navigator.of(context).pushReplacementNamed('/landingpage');
                  }).catchError((e) {
                    print(e);
                  });
                },
              );
              //penúltimo widget
            } else if (index == userList.length) {
              return Container(
                  height: MediaQuery.of(context).size.height * 0.5,
                  width: double.infinity,
                  child: userList.isEmpty
                      ? Center(
                          child: Text("Cargando posicion..."), //si no esto
                        )
                      : userList[0].latitud == 0 && userList[0].longitud == 0
                          ? Center(
                              child: Text("Gps no disponible..."), //si no esto
                            )
                          : cargarPos(
                              userList[0].latitud, userList[0].longitud));
              //widgets antes del último
            } else {
              var dic;
              String ejecucion_text = "Alarma desactivada";
              String detenerEj_text = "Pulsador desbloqueado";
              String caer_text = "";
              String subir_text = "";
              String levantar_text = "";
              Color color_caer = Colors.green;
              Color color_subir = Colors.green;
              Color color_levantar = Colors.green;
              Color color_ejecucion = Colors.red;
              Color color_detenerEj = Colors.green;
              if (userList[index].caer) color_caer = Colors.red;
              if (userList[index].subir) color_subir = Colors.red;
              if (userList[index].levantar) color_levantar = Colors.red;
              if (userList[index].ejecucion) {
                color_ejecucion = Colors.green;
                ejecucion_text = "Alarma activa";
              }
              if (userList[index].detenerEj) {
                color_detenerEj = Colors.red;
                detenerEj_text = "Desbloquear pulsador";
              }

              return Column(
                children: [
                  SizedBox(
                    height: 10,
                  ),
                  RaisedButton(
                    //BOTON ENTER
                    color: color_subir,
                    onPressed: () => {},
                    child: Text(
                      "Subir",
                      style: TextStyle(
                          color: Colors.white, fontWeight: FontWeight.bold),
                    ),
                  ),
                  SizedBox(
                    height: 10,
                  ),
                  RaisedButton(
                    //BOTON ENTER
                    color: color_caer,
                    onPressed: () => {},
                    child: Text(
                      "Caer",
                      style: TextStyle(
                          color: Colors.white, fontWeight: FontWeight.bold),
                    ),
                  ),
                  SizedBox(
                    height: 10,
                  ),
                  RaisedButton(
                    //BOTON ENTER
                    color: color_levantar,
                    onPressed: () => {},
                    child: Text(
                      "Levantar",
                      style: TextStyle(
                          color: Colors.white, fontWeight: FontWeight.bold),
                    ),
                  ),
                  SizedBox(
                    height: 10,
                  ),
                  RaisedButton(
                    //BOTON ENTER
                    color: color_ejecucion,
                    onPressed: () => {},
                    child: Text(
                      ejecucion_text,
                      style: TextStyle(
                          color: Colors.white, fontWeight: FontWeight.bold),
                    ),
                  ),
                  SizedBox(
                    height: 10,
                  ),
                  RaisedButton(
                    //BOTON ENTER
                    color: color_detenerEj,
                    onPressed: () => {
                      dic = FirebaseFirestore.instance
                          .collection('location')
                          .where('user', isEqualTo: userActual)
                          .get()
                          .then((querySnapshot) {
                        for (var doc in querySnapshot.docs) {
                          FirebaseFirestore.instance
                              .collection('location')
                              .doc(doc.id)
                              .update({"detenerEj": false});
                        }
                      }),
                      FirebaseFirestore.instance
                          .collection('location')
                          .doc()
                          .update({"detenerEj": false})
                    },
                    child: Text(
                      detenerEj_text,
                      style: TextStyle(
                          color: Colors.white, fontWeight: FontWeight.bold),
                    ),
                  ),
                  SizedBox(height: 20)
                ],
              );
            }
          },
        ),
      ),
    );
  }
}
