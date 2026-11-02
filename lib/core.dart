import 'dart:convert';
import 'package:flutter/foundation.dart';
import 'package:flutter/services.dart';

const bridge = MethodChannel('com.tdg.enseignant/storage');
const levels = ['CI', 'CP', 'CE1', 'CE2', 'CM1', 'CM2'];
String fold(String value) {
  var s = value.toLowerCase();
  const from = 'àâäáãåçéèêëíìîïñóòôöõúùûüýÿ';
  const to =   'aaaaaaceeeeiiiinooooouuuuyy';
  for (var i = 0; i < from.length; i++) { s = s.replaceAll(from[i], to[i]); }
  return s.replaceAll('œ', 'oe').replaceAll('æ', 'ae').replaceAll('’', "'");
}
String uid() => DateTime.now().microsecondsSinceEpoch.toString();
String dateKey(DateTime d) => '${d.year}-${d.month.toString().padLeft(2,'0')}-${d.day.toString().padLeft(2,'0')}';
String frenchDate(DateTime d) => '${d.day.toString().padLeft(2,'0')}/${d.month.toString().padLeft(2,'0')}/${d.year}';
int minutes(String time) { final p = time.split(':'); return int.parse(p[0])*60+int.parse(p[1]); }
double? number(String s) => double.tryParse(s.replaceAll(',', '.'));

Map<String,dynamic> emptyData() => {
 'version':1, 'notes':[], 'tasks':[], 'slots':[], 'classes':[], 'pupils':[],
 'evaluations':[], 'attendance':[], 'favorites':[], 'bookmarks':[], 'completed':[],
 'theme':'system', 'font':1.0, 'dictionaryHistory':[],
};
const recordKeys = ['notes','tasks','slots','classes','pupils','evaluations','attendance'];
void validateData(Map<String,dynamic> data) {
 if(data['version'] != 1) { throw const FormatException('Version de sauvegarde incompatible.'); }
 for(final key in recordKeys) {
  if(data[key] is! List || (data[key] as List).any((v)=>v is! Map || v['id'] is! String)) {
   throw FormatException('Données invalides : $key.');
  }
  final ids=(data[key] as List).map((v)=>v['id']).toSet();
  if(ids.length != (data[key] as List).length) { throw FormatException('Identifiants dupliqués : $key.'); }
 }
 for(final key in ['favorites','bookmarks','completed']) {
  if(data[key] is! List || (data[key] as List).any((v)=>v is! String)) { throw FormatException('Liste invalide : $key.'); }
 }
 if(data.containsKey('dictionaryHistory')) {
  final history=data['dictionaryHistory'];
  if(history is! List || history.length>50 || history.any((v)=>v is! String || (int.tryParse(v)??0)<1)) {
   throw const FormatException('Historique du dictionnaire invalide.');
  }
 }
 if(!['system','light','dark'].contains(data['theme']) || data['font'] is! num || data['font']<0.8 || data['font']>1.6) {
  throw const FormatException('Réglages invalides.');
 }
 bool has(String kind, dynamic id) => (data[kind] as List).any((v)=>v['id']==id);
 for(final p in data['classes']) {
  if(p['name'] is! String || !levels.contains(p['level'])) { throw const FormatException('Classe invalide.'); }
 }
 for(final p in data['pupils']) {
  if(p['name'] is! String || !has('classes',p['classId'])) { throw const FormatException('Élève invalide.'); }
 }
 for(final p in data['notes']) {
  if(p['title'] is! String || p['body'] is! String || p['kind'] is! String) { throw const FormatException('Note invalide.'); }
 }
 for(final p in data['tasks']) {
  if(p['title'] is! String || p['done'] is! bool || DateTime.tryParse(p['date']?.toString() ?? '')==null) { throw const FormatException('Tâche invalide.'); }
 }
 for(final p in data['slots']) {
  final pattern=RegExp(r'^([01]\d|2[0-3]):[0-5]\d$');
  if(p['title'] is! String || p['place'] is! String || p['day'] is! int || p['day']<1 || p['day']>7 ||
    !pattern.hasMatch(p['start']?.toString() ?? '') || !pattern.hasMatch(p['end']?.toString() ?? '') || minutes(p['start'])>=minutes(p['end'])) {
   throw const FormatException('Créneau invalide.');
  }
 }
 for(final p in data['evaluations']) {
  if(p['title'] is! String || !has('classes',p['classId']) || p['max'] is! num || p['max']<=0 || p['weight'] is! num || p['weight']<=0 || p['scores'] is! Map || p['date'] is! String) { throw const FormatException('Évaluation invalide.'); }
  for(final e in (p['scores'] as Map).entries) {
   if(!(data['pupils'] as List).any((v)=>v['id']==e.key && v['classId']==p['classId']) || e.value is! num || !(e.value as num).isFinite || e.value<0 || e.value>p['max']) { throw const FormatException('Note scolaire invalide.'); }
  }
 }
 for(final p in data['attendance']) {
  if(!has('pupils',p['pupilId']) || DateTime.tryParse(p['date']?.toString() ?? '')==null || !['Présent','Absent','Retard','Excusé'].contains(p['status'])) { throw const FormatException('Présence invalide.'); }
 }
}

double? average(List<Map<String,dynamic>> evaluations, String pupilId) {
 double total=0, weights=0;
 for(final e in evaluations) {
  final score=(e['scores'] as Map)[pupilId];
  if(score is num) { total+=score/(e['max'] as num)*20*(e['weight'] as num); weights+=(e['weight'] as num); }
 }
 return weights==0 ? null : total/weights;
}

class Store extends ChangeNotifier {
 Map<String,dynamic> data=emptyData();
 Future<void> _tail=Future.value();
 List<Map<String,dynamic>> rows(String key) => (data[key] as List).map((v)=>Map<String,dynamic>.from(v as Map)).toList();
 Future<void> load() async {
  final raw=await bridge.invokeMethod<String>('read');
  if(raw!=null) { final decoded=Map<String,dynamic>.from(jsonDecode(raw) as Map); validateData(decoded); data=decoded; }
 }
 Future<void> reload() async {
  await _tail;
  await load();
  notifyListeners();
 }
 Future<void> change(void Function(Map<String,dynamic>) action) {
  final future=_tail.then((_) async {
   final next=Map<String,dynamic>.from(jsonDecode(jsonEncode(data)) as Map);
   action(next); validateData(next);
   await bridge.invokeMethod('write',jsonEncode(next));
   data=next; notifyListeners();
  });
  _tail=future.catchError((Object _) {});
  return future;
 }
 Future<void> put(String kind, Map<String,dynamic> value) => change((d) {
  final list=d[kind] as List; final i=list.indexWhere((v)=>v['id']==value['id']);
  if(i<0) { list.add(value); } else { list[i]=value; }
 });
 Future<void> remove(String kind,String id) => change((d) { (d[kind] as List).removeWhere((v)=>v['id']==id); });
 Future<void> toggle(String kind,String id) => change((d) { final list=d[kind] as List; list.contains(id)?list.remove(id):list.add(id); });
 bool contains(String key,String id) => (data[key] as List).contains(id);
 Future<void> restore(String raw) async {
  final next=Map<String,dynamic>.from(jsonDecode(raw) as Map); validateData(next);
  await change((d) { d.clear(); d.addAll(next); });
 }
}
