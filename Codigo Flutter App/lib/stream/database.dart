import 'package:cloud_firestore/cloud_firestore.dart';
import 'package:firebase_auth/firebase_auth.dart';
import 'package:provider/provider.dart';

import 'user.dart';

class Database {
  final FirebaseFirestore _firestore = FirebaseFirestore.instance;
  var usuActual = FirebaseAuth.instance.currentUser!.email;

  Stream<List<Usuario>> get usuarios {
    return _firestore
        .collection('location')
        .where('user', isEqualTo: usuActual)
        .snapshots()
        .map((QuerySnapshot qs) => qs.docs
            .map((DocumentSnapshot ds) => Usuario(
                subir: ds['subir'],
                caer: ds['caer'],
                levantar: ds['levantar'],
                latitud: ds["location"].latitude,
                ejecucion: ds["ejecucion"],
                detenerEj: ds["detenerEj"],
                longitud: ds["location"].longitude))
            .toList());
  }
}
