// GENERATED CODE - DO NOT MODIFY BY HAND

part of 'park_session.dart';

// **************************************************************************
// JsonSerializableGenerator
// **************************************************************************

ParkSession _$ParkSessionFromJson(Map<String, dynamic> json) => ParkSession(
      isSessaoAtiva: json['is_sessao_ativa'] as bool,
      sessaoData: json['dados_sessao'] == null
          ? null
          : SessaoData.fromJson(json['dados_sessao'] as Map<String, dynamic>),
    );

Map<String, dynamic> _$ParkSessionToJson(ParkSession instance) =>
    <String, dynamic>{
      'is_sessao_ativa': instance.isSessaoAtiva,
      'dados_sessao': instance.sessaoData?.toJson(),
    };

SessaoData _$SessaoDataFromJson(Map<String, dynamic> json) => SessaoData(
      carro: Carro.fromJson(json['carro'] as Map<String, dynamic>),
      tempoSessao: (json['tempo_sessao_ativa_em_minutos'] as num).toDouble(),
    );

Map<String, dynamic> _$SessaoDataToJson(SessaoData instance) =>
    <String, dynamic>{
      'tempo_sessao_ativa_em_minutos': instance.tempoSessao,
      'carro': instance.carro.toJson(),
    };

Carro _$CarroFromJson(Map<String, dynamic> json) => Carro(
      placa: json['placa'] as String,
      modelo: json['modelo'] as String,
      marca: json['marca'] as String,
      cidade: json['cidade'] as String,
      estado: json['estado'] as String,
    );

Map<String, dynamic> _$CarroToJson(Carro instance) => <String, dynamic>{
      'placa': instance.placa,
      'modelo': instance.modelo,
      'marca': instance.marca,
      'cidade': instance.cidade,
      'estado': instance.estado,
    };
