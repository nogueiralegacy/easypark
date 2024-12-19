import 'dart:async';

import 'package:flutter/material.dart';
import 'package:flutter_mobx/flutter_mobx.dart';
import 'package:get_it/get_it.dart';
import 'package:ipark/controllers/park_session_controller.dart';

class ParkPage extends StatefulWidget {
  const ParkPage({super.key});

  @override
  State<ParkPage> createState() => _ParkPageState();
}

class _ParkPageState extends State<ParkPage> {
  bool isParked = false;
  final parkSessionController = GetIt.instance<ParkSessionController>();
  late Timer timer;

  @override
  void initState() {
    parkSessionController.getSession();
    timer = Timer.periodic(Duration(seconds: 10), (timer) {
      parkSessionController.getSession();
    });
    super.initState();
  }

  @override
  void dispose() {
    timer.cancel();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: const EdgeInsets.all(16.0),
      child: Observer(builder: (context) {
        return Visibility(
          visible: parkSessionController.session?.isSessaoAtiva ?? false,
          replacement: NotParkedRightNowWidget(),
          child: ParkSessionWidget(),
        );
      }),
    );
  }
}

class ParkSessionWidget extends StatelessWidget {
  ParkSessionWidget({
    super.key,
  });
  final parkSessionController = GetIt.instance<ParkSessionController>();

  @override
  Widget build(BuildContext context) {
    return Observer(builder: (context) {
      return Column(
        mainAxisSize: MainAxisSize.max,
        children: [
          Image.asset(
            'assets/image.png',
            alignment: Alignment.center,
          ),
          Row(
            crossAxisAlignment: CrossAxisAlignment.center,
            children: [
              Text(
                "Modelo",
                style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold),
              ),
              Spacer(),
              Text(
                  (parkSessionController.session!.sessaoData?.carro.marca ??
                          'Ford ') +
                      (parkSessionController
                              .session!.sessaoData?.carro.modelo ??
                          'Fiesta'),
                  style: TextStyle(fontSize: 14)),
            ],
          ),
          Divider(
            color: Colors.white.withOpacity(0.6),
            height: 32,
          ),
          Row(
            crossAxisAlignment: CrossAxisAlignment.center,
            children: [
              Text(
                "Placa",
                style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold),
              ),
              Spacer(),
              Text(
                  parkSessionController.session!.sessaoData?.carro.placa ??
                      'BRA2020',
                  style: TextStyle(fontSize: 14)),
            ],
          ),
          Divider(
            color: Colors.white.withOpacity(0.6),
            height: 32,
          ),
          Row(
            crossAxisAlignment: CrossAxisAlignment.center,
            children: [
              Text(
                "Estacionamento",
                style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold),
              ),
              Spacer(),
              Text("UFG - Campus Samambaia", style: TextStyle(fontSize: 14)),
            ],
          ),
          Divider(
            color: Colors.white.withOpacity(0.6),
            height: 32,
          ),
          Row(
            crossAxisAlignment: CrossAxisAlignment.center,
            children: [
              Text(
                "Localização",
                style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold),
              ),
              Spacer(),
              Text(
                  '${parkSessionController.session!.sessaoData?.carro.cidade ?? 'Goiânia'} - ${parkSessionController.session!.sessaoData?.carro.estado ?? 'Goiás'}',
                  style: TextStyle(fontSize: 14)),
            ],
          ),
          Divider(
            color: Colors.white.withOpacity(0.6),
            height: 32,
          ),
          Row(
            crossAxisAlignment: CrossAxisAlignment.center,
            children: [
              Text(
                "Sesssão",
                style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold),
              ),
              Spacer(),
              Text("G", style: TextStyle(fontSize: 14)),
            ],
          ),
          Divider(
            color: Colors.white.withOpacity(0.6),
            height: 32,
          ),
          Row(
            crossAxisAlignment: CrossAxisAlignment.center,
            children: [
              Text(
                "Tempo de uso",
                style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold),
              ),
              Spacer(),
              Text((parkSessionController.session!.sessaoData?.tempoSessao.toStringAsFixed(0) ?? '0') + 'min', style: TextStyle(fontSize: 14)),
            ],
          ),
          Divider(
            color: Colors.white.withOpacity(0.6),
            height: 32,
          ),
        ],
      );
    });
  }
}

class NotParkedRightNowWidget extends StatelessWidget {
  const NotParkedRightNowWidget({super.key});

  @override
  Widget build(BuildContext context) {
    return Column(
      mainAxisAlignment: MainAxisAlignment.center,
      children: [
        Image.asset(
          'assets/park_image.png',
          width: 300,
        ),
        SizedBox(
          height: 16,
        ),
        Text(
          'Entre em algum de nossos estacionamentos para acompanhar os detalhes sobre seu uso atual.',
          style: TextStyle(
            fontSize: 18,
          ),
          textAlign: TextAlign.center,
        ),
      ],
    );
  }
}
