// ignore_for_file: curly_braces_in_flow_control_structures

import 'package:flutter/material.dart';
import 'package:get_it/get_it.dart';
import 'package:flutter_mobx/flutter_mobx.dart';
import 'package:ipark/controllers/park_history_controller.dart';
import 'package:ipark/models/park_use.dart';
import 'package:pull_to_refresh_flutter3/pull_to_refresh_flutter3.dart';

class HistoryPage extends StatefulWidget {
  const HistoryPage({super.key});

  @override
  State<HistoryPage> createState() => _HistoryPageState();
}

class _HistoryPageState extends State<HistoryPage> {
  final RefreshController _refreshController =
      RefreshController(initialRefresh: false);

  final parkHistoryController = GetIt.instance<ParkHistoryController>();

  void _onRefresh() async {
    await Future.delayed(Duration(milliseconds: 1000));
    parkHistoryController.getHistory(onSuccess: () {
      _refreshController.refreshCompleted();
    }, onError: () {
      _refreshController.refreshFailed();
    });
  }

  @override
  void initState() {
    parkHistoryController.getHistory();
    super.initState();
  }


  @override
  Widget build(BuildContext context) {
    return SmartRefresher(
      controller: _refreshController,
      onRefresh: _onRefresh,
      child: Observer(builder: (context) {
        return Visibility(
          visible: parkHistoryController.parkUses.isNotEmpty,
          replacement: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            mainAxisSize: MainAxisSize.max,
            children: [
              Text(
                'Não há pagamentos\nainda',
                style: TextStyle(fontSize: 28, color: Colors.white),
                textAlign: TextAlign.center,
              ),
            ],
          ),
          child: ListView.separated(
            itemBuilder: (_, i) {
              var payment = parkHistoryController.parkUses[i];
              return ParkUseWidget(data: payment);
            },
            separatorBuilder: (_, i) {
              return Divider(
                color: Colors.white.withOpacity(0.5),
              );
            },
            primary: false,
            itemCount: parkHistoryController.parkUses.length,
            shrinkWrap: true,
          ),
        );
      }),
    );
  }
}

class ParkUseWidget extends StatelessWidget {
  final ParkUse data;
  const ParkUseWidget({super.key, required this.data});

  @override
  Widget build(BuildContext context) {
    return Container(
      padding: EdgeInsets.all(16),
      child: Row(
        children: [
          Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Stack(
                alignment: Alignment.center,
                children: [
                  Image.asset('assets/placa.png', width: 120,),
                  Padding(
                    padding: const EdgeInsets.fromLTRB(0.0, 8, 0, 0),
                    child: Text(data.placa, style: TextStyle(color: Colors.black, fontSize: 18),),
                  ),
                ],
              ),
              SizedBox(height: 8,),
              Text(data.nomeEstabelecimento),
              Text('R\$ ${data.valorTotal.toStringAsFixed(2)}'),
            ],
          ),
          Spacer(),
          Text(
              '${Duration(minutes: (data.horasEstacionado * 60).toInt()).inMinutes}min'),
        ],
      ),
    );
  }
}
