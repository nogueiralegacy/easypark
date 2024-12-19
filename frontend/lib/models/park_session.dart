import 'package:json_annotation/json_annotation.dart';

part 'park_session.g.dart';

@JsonSerializable(explicitToJson: true)
class ParkSession {
  @JsonKey(name: 'is_sessao_ativa')
  bool isSessaoAtiva;
  @JsonKey(name: 'dados_sessao', )
  SessaoData? sessaoData;

  ParkSession({
    required this.isSessaoAtiva,
    this.sessaoData,
  });

  factory ParkSession.fromJson(Map<String, dynamic> json) =>
      _$ParkSessionFromJson(json);

  Map<String, dynamic> toJson() => _$ParkSessionToJson(this);
}


@JsonSerializable(explicitToJson: true)
class SessaoData {
  @JsonKey(name: 'tempo_sessao_ativa_em_minutos')
  double tempoSessao;
  @JsonKey(name: 'carro')
  Carro carro;

  SessaoData({
    required this.carro,
    required this.tempoSessao,
  });

  factory SessaoData.fromJson(Map<String, dynamic> json) =>
      _$SessaoDataFromJson(json);

  Map<String, dynamic> toJson() => _$SessaoDataToJson(this);
}

@JsonSerializable(explicitToJson: true)
class Carro {
  @JsonKey(name: 'placa')
  String placa;
  @JsonKey(name: 'modelo')
  String modelo;
  @JsonKey(name: 'marca')
  String marca;
  @JsonKey(name: 'cidade')
  String cidade;
  @JsonKey(name: 'estado')
  String estado;


  Carro({
    required this.placa,
    required this.modelo,
    required this.marca,
    required this.cidade,
    required this.estado,
  });

  factory Carro.fromJson(Map<String, dynamic> json) =>
      _$CarroFromJson(json);

  Map<String, dynamic> toJson() => _$CarroToJson(this);
}
