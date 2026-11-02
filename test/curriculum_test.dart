import 'dart:convert';
import 'dart:io';
import 'package:flutter_test/flutter_test.dart';
void main(){
 test('parcours CI à CM2 et identifiants historiques conservés',(){
  final lessons=(jsonDecode(File('assets/data/lessons.json').readAsStringSync()) as List);
  final ids=lessons.map((l)=>l['id']).toSet();
  expect(lessons.length,225);
  expect(ids.length,lessons.length);
  for(var i=1;i<=51;i++){expect(ids.contains('l${i.toString().padLeft(3,'0')}'),isTrue);}
  for(final level in ['CI','CP','CE1','CE2','CM1','CM2']){
   for(final subject in ['Français','Mathématiques','Sciences et technologie','Histoire','Géographie','Éducation civique','Éducation artistique','EPS','Arabe','Éducation religieuse']){
    expect(lessons.where((l)=>l['level']==level&&l['subject']==subject).length,greaterThanOrEqualTo(2),reason:'$level — $subject');
   }
  }
  for(final lesson in lessons){for(final field in ['course','example','question','answer','activity','objective','trap']){expect(lesson[field],isNotEmpty);}}
 });
}
