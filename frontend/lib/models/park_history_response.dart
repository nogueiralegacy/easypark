import 'package:ipark/models/park_use.dart';
import 'package:json_annotation/json_annotation.dart';

part 'park_history_response.g.dart';

@JsonSerializable(explicitToJson: true)
class ParkHistoryResponse {
  @JsonKey(name: 'estacionamentos_finalizados')
  final List<ParkUse>? estacionamentosFinalizados;

  const ParkHistoryResponse({this.estacionamentosFinalizados,});

  factory ParkHistoryResponse.fromJson(Map<String, dynamic> json) => _$ParkHistoryResponseFromJson(json);

  Map<String, dynamic> toJson() => _$ParkHistoryResponseToJson(this);
}