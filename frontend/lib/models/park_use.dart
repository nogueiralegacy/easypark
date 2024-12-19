import 'package:json_annotation/json_annotation.dart';

part 'park_use.g.dart';

@JsonSerializable(explicitToJson: true)
class ParkUse {
  @JsonKey(name: 'placa')
  String placa;
  @JsonKey(name: 'valor_total')
  double valorTotal;
  @JsonKey(name: 'nome_estabelecimento')
  String nomeEstabelecimento;
  @JsonKey(name: 'horas_estacionado')
  double horasEstacionado;

  ParkUse({
    required this.placa,
    required this.valorTotal,
    required this.nomeEstabelecimento,
    required this.horasEstacionado,
  });

  factory ParkUse.fromJson(Map<String, dynamic> json) =>
      _$ParkUseFromJson(json);

  Map<String, dynamic> toJson() => _$ParkUseToJson(this);
}
