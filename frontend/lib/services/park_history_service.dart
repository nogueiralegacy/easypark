
import 'package:dio/dio.dart';
import 'package:ipark/models/park_history_response.dart';

class ParkHistoryService {

  Future<ParkHistoryResponse> getParkHistory({int idUsuario = 2}) async {
    try {
      Response response = await Dio().get('http://realbetis.software:8000/view/historico/$idUsuario');
      return ParkHistoryResponse.fromJson(response.data);
    } catch (e) {
      rethrow;
    }
  }
}