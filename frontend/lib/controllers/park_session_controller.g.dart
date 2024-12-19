// GENERATED CODE - DO NOT MODIFY BY HAND

part of 'park_session_controller.dart';

// **************************************************************************
// StoreGenerator
// **************************************************************************

// ignore_for_file: non_constant_identifier_names, unnecessary_brace_in_string_interps, unnecessary_lambdas, prefer_expression_function_bodies, lines_longer_than_80_chars, avoid_as, avoid_annotating_with_dynamic, no_leading_underscores_for_local_identifiers

mixin _$ParkSessionController on ParkSessionControllerBase, Store {
  late final _$sessionAtom =
      Atom(name: 'ParkSessionControllerBase.session', context: context);

  @override
  ParkSession? get session {
    _$sessionAtom.reportRead();
    return super.session;
  }

  @override
  set session(ParkSession? value) {
    _$sessionAtom.reportWrite(value, super.session, () {
      super.session = value;
    });
  }

  @override
  String toString() {
    return '''
session: ${session}
    ''';
  }
}
