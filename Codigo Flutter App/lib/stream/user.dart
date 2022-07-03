// ignore_for_file: empty_constructor_bodies

class Usuario {
  bool subir;
  bool levantar;
  bool caer;
  bool ejecucion;
  bool detenerEj;
  var latitud;
  var longitud;
  Usuario(
      {required this.subir,
      required this.caer,
      required this.levantar,
      required this.latitud,
      required this.ejecucion,
      required this.detenerEj,
      required this.longitud});
}
