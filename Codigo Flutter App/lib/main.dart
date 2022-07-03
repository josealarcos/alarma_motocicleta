import 'package:flutter/material.dart';
import 'package:firebase_core/firebase_core.dart';
import 'package:provider/provider.dart';
import 'package:prueba1/stream/database.dart';

import 'homepage.dart';
import 'loginpage.dart';
import 'stream/user.dart';

void main() {
  WidgetsFlutterBinding
      .ensureInitialized(); //para asegurarse q todas las dependencias esten incializadas
  Firebase.initializeApp().then((value) async {
    runApp(const MyApp());
  });
}

class MyApp extends StatelessWidget {
  const MyApp({Key? key}) : super(key: key);

  // This widget is the root of your application.
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      home: LoginPage(),
      //home: HomePage(),
      routes: <String, WidgetBuilder>{
        '/landingpage': (BuildContext context) => MyApp(),
        '/homepage': (BuildContext context) =>
            StreamProvider<List<Usuario>>.value(
                value: Database().usuarios, initialData: [], child: HomePage()),
      },
    );
  }
}
