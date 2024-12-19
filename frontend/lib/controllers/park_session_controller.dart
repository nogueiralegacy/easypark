import 'package:ipark/models/park_session.dart';
import 'package:ipark/services/park_session_service.dart';
import 'package:mobx/mobx.dart';

part 'park_session_controller.g.dart';

class ParkSessionController = ParkSessionControllerBase with _$ParkSessionController;

abstract class ParkSessionControllerBase with Store {

  final ParkSessionService _service = ParkSessionService();

  @observable
  ParkSession? session;

  Future<void> getSession({Function? onSuccess, Function? onError}) async {
    try {
      _service.getCurrentSession().then((response) {
        session = response;
        onSuccess?.call();
      });
    } catch (e) {
      print(e);
      onError?.call();
    }
  }

}
