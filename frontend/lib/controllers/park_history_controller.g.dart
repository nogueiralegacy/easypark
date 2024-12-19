// GENERATED CODE - DO NOT MODIFY BY HAND

part of 'park_history_controller.dart';

// **************************************************************************
// StoreGenerator
// **************************************************************************

// ignore_for_file: non_constant_identifier_names, unnecessary_brace_in_string_interps, unnecessary_lambdas, prefer_expression_function_bodies, lines_longer_than_80_chars, avoid_as, avoid_annotating_with_dynamic, no_leading_underscores_for_local_identifiers

mixin _$ParkHistoryController on ParkHistoryControllerBase, Store {
  late final _$parkUsesAtom =
      Atom(name: 'ParkHistoryControllerBase.parkUses', context: context);

  @override
  ObservableList<ParkUse> get parkUses {
    _$parkUsesAtom.reportRead();
    return super.parkUses;
  }

  @override
  set parkUses(ObservableList<ParkUse> value) {
    _$parkUsesAtom.reportWrite(value, super.parkUses, () {
      super.parkUses = value;
    });
  }

  @override
  String toString() {
    return '''
parkUses: ${parkUses}
    ''';
  }
}
