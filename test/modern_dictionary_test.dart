import 'dart:convert';
import 'package:flutter/services.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:enseignant/core.dart';
import 'package:enseignant/dictionary.dart';

void main() {
 TestWidgetsFlutterBinding.ensureInitialized();
 const channel=MethodChannel('enseignant/dictionary-test');
 tearDown(()=>TestDefaultBinaryMessengerBinding.instance.defaultBinaryMessenger.setMockMethodCallHandler(channel,null));
 test('filtre de provenance et identifiants 64 bits transmis sans perte',() async {
  const modernId=60000000000000001;
  MethodCall? received;
  TestDefaultBinaryMessengerBinding.instance.defaultBinaryMessenger.setMockMethodCallHandler(channel,(call) async {
   received=call;
   return {'rows':[{'id':modernId,'headword':'informatique','source':'FranceTerme'}],'total':1,'hasMore':false};
  });
  const repository=DictionaryRepository(channel:channel);
  final result=await repository.search(query:'informatique',source:'FranceTerme',ids:[modernId]);
  expect(received!.method,'dictionarySearch');
  expect(received!.arguments['source'],'FranceTerme');
  expect(received!.arguments['ids'],[modernId]);
  expect(result.rows.single['id'],modernId);
 });
 test('article moderne : typographie, provenance et autres sources conservées',() async {
  TestDefaultBinaryMessengerBinding.instance.defaultBinaryMessenger.setMockMethodCallHandler(channel,(call) async => {
   'id':40000000000000001,'headword':'réseau','source':'Wiktionnaire','sourceUrl':'https://fr.wiktionary.org/wiki/réseau#fr','licence':'CC BY-SA 4.0','publication':'01/10/2026',
   'paragraphs':jsonEncode([[{'text':'Définition','bold':true,'italic':false}]]),'references':'[]','alternatives':[{'id':123,'source':'FranceTerme'}],
  });
  final article=await const DictionaryRepository(channel:channel).entry(40000000000000001);
  expect(article['paragraphs'][0][0]['bold'],isTrue);
  expect(article['licence'],'CC BY-SA 4.0');
  expect(article['alternatives'][0]['id'],123);
 });
 test('sauvegarde JSON : identifiants du dictionnaire sans perte',(){
  final data=emptyData();
  data['dictionaryHistory']=['40000000000000001','60000000000000001'];
  data['favorites']=['l001','dictionary:40000000000000001','dictionary:60000000000000001'];
  final restored=jsonDecode(jsonEncode(data)) as Map<String,dynamic>;
  validateData(restored);
  expect(restored['dictionaryHistory'],data['dictionaryHistory']);
 });
}
