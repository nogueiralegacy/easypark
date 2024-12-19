
import 'package:dio/dio.dart';
import 'package:ipark/models/park_session.dart';

class ParkSessionService {

  Future<ParkSession> getCurrentSession({int idUsuario = 2}) async {
    try {
      Response response = await Dio().get('http://realbetis.software:8000/registro/sessao/$idUsuario');
      return ParkSession.fromJson(response.data);
    } catch (e) {
      rethrow;
    }
  }
}