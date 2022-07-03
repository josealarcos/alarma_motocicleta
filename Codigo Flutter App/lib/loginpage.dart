// ignore_for_file: prefer_const_constructors, prefer_const_literals_to_create_immutables, deprecated_member_use, avoid_print

import 'package:flutter/material.dart';
import 'package:firebase_auth/firebase_auth.dart';
import 'package:firebase_messaging/firebase_messaging.dart';
import 'package:cloud_firestore/cloud_firestore.dart';
import 'package:clipboard/clipboard.dart';

class LoginPage extends StatefulWidget {
  LoginPage({Key? key}) : super(key: key);

  @override
  _LoginPageState createState() => _LoginPageState();
}

class _LoginPageState extends State<LoginPage> {
  String _user = "";
  String _pwd = "";

  void initState() {
    super.initState();
    setUser();
  }

  //funcion rellenar obtener el usuario si el token del disposititvo esta en firebase
  setUser() async {
    //fc para establecer el token del dispositivo en firestore del usuario
    String? token = await FirebaseMessaging.instance.getToken();
    String user = '';
    FirebaseFirestore.instance
        .collection('location')
        .where('devtoken', isEqualTo: token)
        .get()
        .then((QuerySnapshot querySnapshot) {
      for (var doc in querySnapshot.docs) {
        user = doc['user'];
        FlutterClipboard.copy(doc['user']);
      }
    });
    return user;
  }

//--------------------------------------------------------------------------------------
  @override
  Widget build(BuildContext context) {
    return Scaffold(
        appBar: AppBar(
          shadowColor: Colors.blueGrey,
          backgroundColor: Colors.black54,
          title: Text("Login Alarmoto"),
        ),
        body: Container(
          decoration: BoxDecoration(
              image: DecorationImage(
                  image: AssetImage("assets/loginFondo.jpeg"),
                  fit: BoxFit.cover)),
          child: Center(
            child: Column(
              children: [
                Container(
                  //TEXT SING IN
                  padding: EdgeInsets.fromLTRB(25, 75, 25, 5),
                  child: Text(
                    "Sing in",
                    style: TextStyle(
                        color: Colors.white,
                        fontSize: 25,
                        fontWeight: FontWeight.bold),
                  ),
                ),
                Container(
                    //TEXTFILED USER
                    padding: EdgeInsets.symmetric(horizontal: 25, vertical: 5),
                    child: TextField(
                      onChanged: (value) {
                        setState(() {
                          _user = value;
                        });
                      },
                      decoration: InputDecoration(
                        hintText: "User",
                        fillColor: Colors.white,
                        filled: true,
                      ),
                    )),
                Container(
                    //TEXTFILED CONTRASEÑA
                    padding: EdgeInsets.symmetric(horizontal: 25, vertical: 5),
                    child: TextField(
                      onChanged: (value) {
                        setState(() {
                          _pwd = value;
                        });
                      },
                      obscureText: true,
                      decoration: InputDecoration(
                          hintText: "Pasword",
                          fillColor: Colors.white,
                          filled: true),
                    )),
                RaisedButton(
                  //BOTON ENTER
                  color: Colors.black87,
                  onPressed: () => {
                    FirebaseAuth.instance
                        .signInWithEmailAndPassword(
                            email: _user, password: _pwd)
                        .catchError((e) {
                      print("Usuario o contraseña -------");
                      _alerta(context);
                    }).then((user) {
                      Navigator.of(context).pushReplacementNamed('/homepage');
                    })
                  },
                  child: Text(
                    "Sing In",
                    style: TextStyle(
                        color: Colors.white, fontWeight: FontWeight.bold),
                  ),
                ),
                SizedBox(
                  height: 5.0,
                ),
                RaisedButton(
                  //BOTON ENTER
                  color: Colors.black87,
                  onPressed: () => {},
                  child: Text(
                    "Notify",
                    style: TextStyle(
                        color: Colors.white, fontWeight: FontWeight.bold),
                  ),
                ),
              ],
            ),
          ),
        ));
  }
}

void _alerta(BuildContext contexto) {
  showDialog(
      context: contexto,
      builder: (BuildContext contexto) {
        return AlertDialog(
          title: Text("Error"),
          content: Text("Usiario o contraseña incorrectos"),
        );
      });
}
