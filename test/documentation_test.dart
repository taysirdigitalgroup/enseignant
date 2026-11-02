import 'dart:convert';
import 'dart:io';
import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:enseignant/core.dart';
import 'package:enseignant/documentation.dart';
import 'package:enseignant/main.dart' show store;

ReferencePack fixture()=>ReferencePack({
 'displayDate':'31 octobre 2026','scope':'Fonds de test','method':'Méthode de test',
 'sources':{'s':{'title':'Référence de test','publisher':'Source de test','url':'https://example.org','date':'2026','note':'Note'}},'images':{},
 'subjects':[{'id':'geo','title':'Géographie du Sénégal','description':'Territoires','image':''},{'id':'history','title':'Histoire du Sénégal','description':'Repères','image':''}],
 'timeline':[],'glossary':[{'term':'chronologie','definition':'Ordre des événements','article':'h-test'}],
 'articles':[{
  'id':'h-test','subject':'history','group':'Repères','title':'Une fiche historique','summary':'Comprendre une période.','minutes':3,
  'objectives':['Situer un événement.'],'blocks':[{'type':'p','text':'Un texte documentaire et ses sources.'}],
  'takeaways':['Les sources ont un contexte.'],'sources':['s'],'related':[],
  'activity':{'task':'Comparer deux documents.','answer':'Identifier auteur et date.'},'questions':[],
 }],
});
class TestReferences extends ReferenceRepository {
 const TestReferences();
 @override Future<ReferencePack> load() async =>fixture();
}
Future<void> flushStore(WidgetTester tester) async {
 await tester.runAsync(() async { await Future<void>.delayed(const Duration(milliseconds:10)); });
 await tester.pumpAndSettle();
}
void main(){
 TestWidgetsFlutterBinding.ensureInitialized();
 late Map<String,dynamic> previous;
 setUp((){
  previous=store.data;store.data=emptyData();
  TestDefaultBinaryMessengerBinding.instance.defaultBinaryMessenger.setMockMethodCallHandler(bridge,(call) async {
   if(call.method=='read')return jsonEncode(store.data);
   return null;
  });
 });
 tearDown((){
  store.data=previous;
  TestDefaultBinaryMessengerBinding.instance.defaultBinaryMessenger.setMockMethodCallHandler(bridge,null);
 });
 test('recherche française et index du lexique',(){
  expect(referenceNormalize('SÉNÉGAL ŒUVRE Ke\u0301dougou'),'senegal oeuvre kedougou');
  expect(fixture().find(query:'chronologie').single['id'],'h-test');
  expect(fixture().find(subject:'geo'),isEmpty);
 });
 test('la carte distingue le Sénégal de la bande gambienne',(){
  final raw=jsonDecode(File('assets/documentation/regions.json').readAsStringSync()) as Map;
  final geometry=ReferenceMapGeometry(raw['features'] as List,const Size(640,480));
  expect(geometry.paths.length,14);
  expect(geometry.paths['r-tambacounda']!.contains(geometry.project(-13.67,13.77)),isTrue);
  expect(geometry.paths['r-diourbel']!.contains(geometry.project(-16.23,14.65)),isTrue);
  expect(geometry.paths.values.any((p)=>p.contains(geometry.project(-15.50,13.45))),isFalse);
 });
 testWidgets('ouvrir les détails et démarquer un favori actualise la liste', (tester) async {
  await tester.pumpWidget(const MaterialApp(home:DocumentationScreen(repository:TestReferences())));
  await tester.pumpAndSettle();
  await tester.tap(find.text('Histoire du Sénégal'));
  await tester.pumpAndSettle();
  await tester.tap(find.text('Une fiche historique'));
  await tester.pumpAndSettle();
  expect(find.text('Un texte documentaire et ses sources.'),findsOneWidget);
  await tester.tap(find.byTooltip('Ajouter aux favoris'));
  await flushStore(tester);
  expect(store.contains('favorites','reference:h-test'),isTrue);
  expect(find.byTooltip('Retirer des favoris'),findsOneWidget);
  await tester.pageBack();await tester.pumpAndSettle();
  await tester.tap(find.text('Favoris'));await tester.pumpAndSettle();
  await tester.tap(find.byTooltip('Retirer des favoris'));await flushStore(tester);
  expect(find.text('Aucune fiche pour ces filtres.'),findsOneWidget);
  expect(store.contains('favorites','reference:h-test'),isFalse);
  expect(tester.takeException(),isNull);
 });
 test('les marqueurs documentaires cohabitent avec ceux des leçons et du dictionnaire',(){
  (store.data['favorites'] as List).addAll(['l001','dictionary:25']);
  (store.data['completed'] as List).add('l001');
  (store.data['favorites'] as List).add(referenceKey('h-test'));
  (store.data['completed'] as List).add(referenceKey('h-test'));
  final restored=jsonDecode(jsonEncode(store.data)) as Map<String,dynamic>;
  validateData(restored);
  expect(restored['favorites'],containsAll(['l001','dictionary:25','reference:h-test']));
  expect(restored['completed'],containsAll(['l001','reference:h-test']));
 });
}
