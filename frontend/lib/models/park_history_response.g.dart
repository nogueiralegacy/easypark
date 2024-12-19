// GENERATED CODE - DO NOT MODIFY BY HAND

part of 'park_history_response.dart';

// **************************************************************************
// JsonSerializableGenerator
// **************************************************************************

ParkHistoryResponse _$ParkHistoryResponseFromJson(Map<String, dynamic> json) =>
    ParkHistoryResponse(
      estacionamentosFinalizados:
          (json['estacionamentos_finalizados'] as List<dynamic>?)
              ?.map((e) => ParkUse.fromJson(e as Map<String, dynamic>))
              .toList(),
    );

Map<String, dynamic> _$ParkHistoryResponseToJson(
        ParkHistoryResponse instance) =>
    <String, dynamic>{
      'estacionamentos_finalizados':
          instance.estacionamentosFinalizados?.map((e) => e.toJson()).toList(),
    };
