import 'package:ipark/models/park_use.dart';
import 'package:ipark/services/park_history_service.dart';
import 'package:mobx/mobx.dart';

part 'park_history_controller.g.dart';

class ParkHistoryController = ParkHistoryControllerBase with _$ParkHistoryController;

abstract class ParkHistoryControllerBase with Store {

  final ParkHistoryService _service = ParkHistoryService();

  @observable
  ObservableList<ParkUse> parkUses = ObservableList<ParkUse>();

  Future<void> getHistory({Function? onSuccess, Function? onError}) async {
    try {
      _service.getParkHistory().then((response) {
        parkUses = (response.estacionamentosFinalizados ?? []).asObservable();
        onSuccess?.call();
      });
    } catch (e) {
      onError?.call();
    }
  }

}
