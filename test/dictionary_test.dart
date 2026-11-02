import 'dart:async';
import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:enseignant/core.dart';
import 'package:enseignant/dictionary.dart';
import 'package:enseignant/main.dart' show store;

class FakeDictionary extends DictionaryRepository {
 final a=Completer<DictionaryResult>(),ab=Completer<DictionaryResult>();
 @override Future<Map<String,dynamic>> info() async => {'counts':{'entries':2},'builtAt':'2026-10-31','sources':[],'letters':{'A':2},'categories':{'Nom féminin':2}};
 @override Future<DictionaryResult> search({String query='',String mode='word',String letter='',String category='',String source='',List<int>? ids,int offset=0}) async {
  if(query=='a')return a.future;
  if(query=='ab')return ab.future;
  return const DictionaryResult([],0,false);
 }
}
Map<String,dynamic> word(int id,String title)=>{'id':id,'headword':title,'letter':'A','category':'Nom féminin','startPage':0,'endPage':0,'source':'Wiktionnaire','preview':'Définition de test.'};
void main(){
 TestWidgetsFlutterBinding.ensureInitialized();
 testWidgets('une ancienne réponse ne remplace pas la dernière recherche', (tester) async {
  final repo=FakeDictionary();
  await tester.pumpWidget(MaterialApp(home:DictionaryScreen(repository:repo)));
  await tester.pumpAndSettle();
  await tester.enterText(find.byType(TextField),'a');
  await tester.pump(const Duration(milliseconds:300));
  await tester.enterText(find.byType(TextField),'ab');
  await tester.pump(const Duration(milliseconds:300));
  repo.ab.complete(DictionaryResult([word(2,'ABAISSE')],1,false));
  await tester.pumpAndSettle();
  repo.a.complete(DictionaryResult([word(1,'ANCIEN RÉSULTAT')],1,false));
  await tester.pumpAndSettle();
  tester.testTextInput.hide();
  await tester.pump();
  await tester.drag(find.byType(CustomScrollView),const Offset(0,-700));
  await tester.pumpAndSettle();
  expect(find.text('ABAISSE'),findsOneWidget);
  expect(find.text('ANCIEN RÉSULTAT'),findsNothing);
  expect(tester.takeException(),isNull);
 });
 test('sauvegarde ancienne compatible et historique séparé',(){
  final data=emptyData()..remove('dictionaryHistory');
  validateData(data);
  data['dictionaryHistory']=['40000000000000001','60000000000000001'];validateData(data);
  data['dictionaryHistory']=['mot invalide'];expect(()=>validateData(data),throwsFormatException);
 });
 test('les favoris du dictionnaire ne se confondent pas avec les leçons',(){
  final previous=store.data;
  try {
   store.data=emptyData();(store.data['favorites'] as List).addAll(['l001','dictionary:25']);
   expect(dictionaryFavorites(),[25]);
   expect(store.contains('favorites','l001'),isTrue);
  } finally {store.data=previous;}
 });
}
