// GENERATED CODE - DO NOT MODIFY BY HAND

part of 'park_use.dart';

// **************************************************************************
// JsonSerializableGenerator
// **************************************************************************

ParkUse _$ParkUseFromJson(Map<String, dynamic> json) => ParkUse(
      placa: json['placa'] as String,
      valorTotal: (json['valor_total'] as num).toDouble(),
      nomeEstabelecimento: json['nome_estabelecimento'] as String,
      horasEstacionado: (json['horas_estacionado'] as num).toDouble(),
    );

Map<String, dynamic> _$ParkUseToJson(ParkUse instance) => <String, dynamic>{
      'placa': instance.placa,
      'valor_total': instance.valorTotal,
      'nome_estabelecimento': instance.nomeEstabelecimento,
      'horas_estacionado': instance.horasEstacionado,
    };
