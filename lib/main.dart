import 'dart:convert';
import 'package:flutter/material.dart';
import 'core.dart';
import 'library.dart';
import 'teacher_tools.dart';
import 'dictionary.dart';
import 'documentation.dart';

final store=Store();
void main() { WidgetsFlutterBinding.ensureInitialized(); runApp(const EnseignantApp()); }
class EnseignantApp extends StatefulWidget {
 const EnseignantApp({super.key});
 @override State<EnseignantApp> createState()=>_AppState();
}
class _AppState extends State<EnseignantApp> {
 late Future<void> loading;
 @override void initState() { super.initState(); loading=store.load(); }
 @override Widget build(BuildContext context)=>ListenableBuilder(listenable:store,builder:(context,_)=>MaterialApp(
  title:'Enseignant',debugShowCheckedModeBanner:false,
  theme:theme(Brightness.light),darkTheme:theme(Brightness.dark),
  themeMode:switch(store.data['theme']) {'light'=>ThemeMode.light,'dark'=>ThemeMode.dark,_=>ThemeMode.system},
  builder:(context,child)=>MediaQuery(data:MediaQuery.of(context).copyWith(textScaler:TextScaler.linear((store.data['font'] as num).toDouble())),child:child!),
  home:FutureBuilder<void>(future:loading,builder:(context,snapshot) {
   if(snapshot.connectionState!=ConnectionState.done) { return const Scaffold(body:Center(child:CircularProgressIndicator())); }
   if(snapshot.hasError) { return Scaffold(body:SafeArea(child:Padding(padding:const EdgeInsets.all(24),child:Column(mainAxisAlignment:MainAxisAlignment.center,children:[
    const Icon(Icons.warning_amber,size:48),const Text('Les données n’ont pas pu être chargées.'),Text('${snapshot.error}'),
    const Text('Aucune donnée existante ne sera écrasée. Vérifiez l’espace disponible ou réessayez.'),
    FilledButton(onPressed:()=>setState(()=>loading=store.load()),child:const Text('Réessayer')),
    TextButton(onPressed:() async { final raw=await bridge.invokeMethod<String>('import'); if(raw!=null) { try { await store.restore(raw); setState(()=>loading=Future.value()); } catch(e) { if(context.mounted) { message(context,'$e'); } } } },child:const Text('Restaurer une sauvegarde')),
   ])))); }
   return const Home();
  }),
 ));
 ThemeData theme(Brightness b)=>ThemeData(useMaterial3:true,brightness:b,
  colorScheme:ColorScheme.fromSeed(seedColor:const Color(0xff2548b8),brightness:b),
  scaffoldBackgroundColor:b==Brightness.light?const Color(0xfff6f7fc):const Color(0xff101827),
  appBarTheme:const AppBarTheme(centerTitle:false),
  inputDecorationTheme:InputDecorationTheme(border:OutlineInputBorder(borderRadius:BorderRadius.circular(14))),
  cardTheme:const CardThemeData(elevation:0,margin:EdgeInsets.symmetric(vertical:5)),
 );
}
void message(BuildContext c,String s)=>ScaffoldMessenger.of(c).showSnackBar(SnackBar(content:Text(s)));
Future<void> perform(BuildContext c,Future<void> Function() action) async {
 try { await action(); } catch(e) { if(c.mounted) { message(c,'Enregistrement impossible : $e'); } }
}
Future<bool> confirm(BuildContext c,String title,String text) async => await showDialog<bool>(context:c,builder:(c)=>AlertDialog(title:Text(title),content:Text(text),actions:[TextButton(onPressed:()=>Navigator.pop(c,false),child:const Text('Annuler')),FilledButton(onPressed:()=>Navigator.pop(c,true),child:const Text('Confirmer'))]))??false;
Widget empty(String text)=>Padding(padding:const EdgeInsets.all(30),child:Column(mainAxisSize:MainAxisSize.min,children:[const Icon(Icons.auto_stories_outlined,size:42),const SizedBox(height:12),Text(text,textAlign:TextAlign.center)]));
Widget section(String text)=>Padding(padding:const EdgeInsets.only(top:18,bottom:8),child:Text(text,style:const TextStyle(fontSize:20,fontWeight:FontWeight.w700)));
Widget tile(String title,String subtitle,{IconData icon=Icons.description_outlined,VoidCallback? onTap,VoidCallback? onLongPress,Widget? trailing})=>Card(child:ListTile(leading:Icon(icon),title:Text(title),subtitle:subtitle.isEmpty?null:Text(subtitle),trailing:trailing,onTap:onTap,onLongPress:onLongPress));
Future<void> detail(BuildContext context,String title,List<Widget> content) async => showModalBottomSheet<void>(context:context,isScrollControlled:true,showDragHandle:true,builder:(c)=>SafeArea(child:DraggableScrollableSheet(expand:false,initialChildSize:0.65,minChildSize:0.25,maxChildSize:0.95,builder:(c,controller)=>ListView(controller:controller,padding:const EdgeInsets.all(20),children:[Text(title,style:Theme.of(c).textTheme.headlineSmall),...content]))));
Future<void> recordOptions(BuildContext context,List<(String,IconData,VoidCallback)> actions) async => showModalBottomSheet<void>(context:context,showDragHandle:true,builder:(sheet)=>SafeArea(child:Column(mainAxisSize:MainAxisSize.min,children:[for(final (label,icon,action) in actions)ListTile(leading:Icon(icon),title:Text(label),onTap:(){Navigator.pop(sheet);action();})])));
Widget optionsButton(List<(String,IconData,VoidCallback)> actions)=>PopupMenuButton<int>(tooltip:'Options',icon:const Icon(Icons.more_vert),onSelected:(index)=>actions[index].$3(),itemBuilder:(_)=>[for(var i=0;i<actions.length;i++)PopupMenuItem(value:i,child:Row(children:[Icon(actions[i].$2),const SizedBox(width:12),Text(actions[i].$1)]))]);
Widget refreshable(Widget child)=>RefreshIndicator(onRefresh:store.reload,child:child);

class Field {
 final String key,label; final List<String>? options; final int lines; final String? Function(String)? validator;
 const Field(this.key,this.label,{this.options,this.lines=1,this.validator});
}
Future<Map<String,dynamic>?> edit(BuildContext c,String title,List<Field> fields,{Map<String,dynamic>? initial})=>showDialog<Map<String,dynamic>>(context:c,builder:(c)=>RecordDialog(title:title,fields:fields,initial:initial));
class RecordDialog extends StatefulWidget {
 final String title; final List<Field> fields; final Map<String,dynamic>? initial;
 const RecordDialog({super.key,required this.title,required this.fields,this.initial});
 @override State<RecordDialog> createState()=>_RecordDialogState();
}
class _RecordDialogState extends State<RecordDialog> {
 final form=GlobalKey<FormState>(); final controllers=<String,TextEditingController>{};
 @override void initState(){super.initState(); for(final f in widget.fields) { controllers[f.key]=TextEditingController(text:widget.initial?[f.key]?.toString()??f.options?.first??''); }}
 @override void dispose(){for(final c in controllers.values){c.dispose();}super.dispose();}
 @override Widget build(BuildContext context)=>AlertDialog(title:Text(widget.title),content:SizedBox(width:520,child:Form(key:form,child:SingleChildScrollView(child:Column(mainAxisSize:MainAxisSize.min,children:widget.fields.map((f)=>Padding(padding:const EdgeInsets.symmetric(vertical:8),child:f.options==null?TextFormField(controller:controllers[f.key],minLines:f.lines,maxLines:f.lines==1?1:12,decoration:InputDecoration(labelText:f.label),validator:(v)=>f.validator?.call((v??'').trim())):DropdownButtonFormField<String>(initialValue:f.options!.contains(controllers[f.key]!.text)?controllers[f.key]!.text:f.options!.first,isExpanded:true,items:f.options!.map((s)=>DropdownMenuItem(value:s,child:Text(s))).toList(),decoration:InputDecoration(labelText:f.label),onChanged:(v)=>controllers[f.key]!.text=v!))).toList())))),actions:[TextButton(onPressed:()=>Navigator.pop(context),child:const Text('Annuler')),FilledButton(onPressed:(){if(form.currentState!.validate()){Navigator.pop(context,{...?widget.initial,for(final f in widget.fields) f.key:controllers[f.key]!.text.trim()});}},child:const Text('Enregistrer'))]);
}
String? requiredText(String v)=>v.isEmpty?'Ce champ est nécessaire.':null;
String? dateValidation(String v){ final d=DateTime.tryParse(v); return d!=null&&dateKey(d)==v?null:'Format attendu : AAAA-MM-JJ.'; }
String? timeValidation(String v)=>RegExp(r'^([01]\d|2[0-3]):[0-5]\d$').hasMatch(v)?null:'Format attendu : HH:MM.';
String? positive(String v)=>number(v)!=null&&number(v)!.isFinite&&number(v)!>0?null:'Saisissez un nombre positif.';

class Home extends StatefulWidget { const Home({super.key}); @override State<Home> createState()=>_HomeState(); }
class _HomeState extends State<Home> {
 int index=0;
 @override Widget build(BuildContext context)=>Scaffold(
  appBar:AppBar(title:Row(children:[ClipRRect(borderRadius:BorderRadius.circular(10),child:Image.asset('assets/images/icon.png',width:34,height:34)),const SizedBox(width:10),const Flexible(child:Text('Enseignant',overflow:TextOverflow.ellipsis))]),actions:[IconButton(tooltip:'Dictionnaire de poche',icon:const Icon(Icons.local_library_outlined),onPressed:()=>Navigator.push(context,MaterialPageRoute<void>(builder:(_)=>const DictionaryScreen()))),IconButton(tooltip:'Documentation & Référence',icon:const Icon(Icons.auto_stories_outlined),onPressed:()=>Navigator.push(context,MaterialPageRoute<void>(builder:(_)=>const DocumentationScreen()))),IconButton(tooltip:'Réglages et informations',icon:const Icon(Icons.settings_outlined),onPressed:()=>Navigator.push(context,MaterialPageRoute<void>(builder:(_)=>const Settings())))]),
  body:SafeArea(child:ListenableBuilder(listenable:store,builder:(context,_)=>IndexedStack(index:index,children:[Agenda(),Classes(),Notes(),Knowledge(),Grevisse()]))),
  bottomNavigationBar:NavigationBar(selectedIndex:index,onDestinationSelected:(i)=>setState(()=>index=i),destinations:const [
   NavigationDestination(icon:Icon(Icons.calendar_month_outlined),label:'Agenda'),NavigationDestination(icon:Icon(Icons.groups_outlined),label:'Classes'),NavigationDestination(icon:Icon(Icons.edit_note),label:'Carnet'),NavigationDestination(icon:Icon(Icons.school_outlined),label:'Savoirs'),NavigationDestination(icon:Icon(Icons.menu_book_outlined),label:'Grevisse')]),
 );
}
const days=['Lundi','Mardi','Mercredi','Jeudi','Vendredi','Samedi','Dimanche'];
class Agenda extends StatefulWidget { const Agenda({super.key}); @override State<Agenda> createState()=>_AgendaState(); }
class _AgendaState extends State<Agenda> {
 DateTime day=DateTime.now();
 Future<void> task() async {
  final result=await edit(context,'Nouvelle tâche',[
   Field('title','Tâche',validator:requiredText),Field('date','Date AAAA-MM-JJ',validator:dateValidation),const Field('priority','Priorité',options:['Normale','Haute']),
  ],initial:{'date':dateKey(day)});
  if(result!=null&&mounted){await perform(context,()=>store.put('tasks',{'id':uid(),...result,'done':false}));}
 }
 Future<void> slot([Map<String,dynamic>? current]) async {
  final result=await edit(context,'Créneau hebdomadaire',[
   Field('title','Cours / classe',validator:requiredText),Field('subject','Matière (couleur du tableau)',validator:requiredText),const Field('weekday','Jour',options:days),Field('start','Début HH:MM',validator:timeValidation),Field('end','Fin HH:MM',validator:timeValidation),const Field('place','Salle / lieu'),
  ],initial:{'weekday':days[day.weekday-1],'start':'08:00','end':'09:00',...?current,'subject':current==null?'':slotSubject(current),if(current!=null)'weekday':days[(current['day'] as int)-1]});
  if(result==null||!mounted)return;
  if(minutes(result['start'])>=minutes(result['end'])){message(context,'La fin doit suivre le début.');return;}
  final weekday=days.indexOf(result.remove('weekday'))+1;
  final overlap=store.rows('slots').any((s)=>s['id']!=current?['id']&&s['day']==weekday&&minutes(s['start'])<minutes(result['end'])&&minutes(s['end'])>minutes(result['start']));
  if(overlap){message(context,'Ce créneau chevauche un cours existant.');return;}
  await perform(context,()=>store.put('slots',{'id':current?['id']??uid(),...result,'day':weekday}));
 }
 @override Widget build(BuildContext context){
  final slots=store.rows('slots').where((s)=>s['day']==day.weekday).toList()..sort((a,b)=>a['start'].compareTo(b['start']));
  final tasks=store.rows('tasks').where((t)=>t['date']==dateKey(day)||(!t['done']&&t['date'].compareTo(dateKey(day))<0)).toList()..sort((a,b)=>a['date'].compareTo(b['date']));
  return refreshable(ListView(padding:const EdgeInsets.all(16),physics:const AlwaysScrollableScrollPhysics(),children:[
   Text('Ma journée de classe',style:Theme.of(context).textTheme.headlineSmall),
   Row(children:[IconButton(tooltip:'Jour précédent',onPressed:()=>setState(()=>day=day.subtract(const Duration(days:1))),icon:const Icon(Icons.chevron_left)),Expanded(child:TextButton(onPressed:() async {final d=await showDatePicker(context:context,initialDate:day,firstDate:DateTime(2020),lastDate:DateTime(2100));if(d!=null){setState(()=>day=d);}},child:Text('${days[day.weekday-1]} · ${frenchDate(day)}'))),IconButton(tooltip:'Jour suivant',onPressed:()=>setState(()=>day=day.add(const Duration(days:1))),icon:const Icon(Icons.chevron_right))]),
   Wrap(spacing:8,children:[FilledButton.icon(onPressed:slot,icon:const Icon(Icons.add),label:const Text('Cours récurrent')),OutlinedButton.icon(onPressed:task,icon:const Icon(Icons.checklist),label:const Text('Tâche'))]),
   Row(children:[Expanded(child:section('Emploi du temps')),IconButton(tooltip:'Tableau de la journée',icon:const Icon(Icons.view_timeline_outlined),onPressed:()=>Navigator.push(context,MaterialPageRoute<void>(builder:(_)=>TimetableScreen(initialDay:day.weekday))))]),if(slots.isEmpty)empty('Aucun cours prévu ce jour. Ajoutez un créneau hebdomadaire.'),
   for(final s in slots)Builder(builder:(c){
    Future<void> delete() async {if(await confirm(c,'Supprimer ce créneau ?','Il sera retiré de toutes les semaines.')&&c.mounted){await perform(c,()=>store.remove('slots',s['id']));}}
    final actions=< (String,IconData,VoidCallback)>[('Modifier',Icons.edit_outlined,()=>slot(s)),('Supprimer',Icons.delete_outline,delete)];
    return tile(s['title'],'${s['start']} – ${s['end']} · ${s['place']}',icon:Icons.schedule,onTap:()=>detail(c,s['title'],[Text('${days[(s['day'] as int)-1]} · ${s['start']} – ${s['end']}'),section('Lieu'),Text(s['place']?.toString().isEmpty==true?'Non renseigné':s['place'].toString())]),onLongPress:()=>recordOptions(c,actions),trailing:optionsButton(actions));
   }),
   section('Tâches et échéances'),const Text('Les échéances sont visibles ici. Cette version ne déclenche pas de notification système.'),
   if(tasks.isEmpty)empty('Aucune tâche pour cette journée, ni tâche en retard.'),
   for(final t in tasks)Builder(builder:(c){
    Future<void> changeTask() async {final r=await edit(c,'Modifier la tâche',[Field('title','Tâche',validator:requiredText),Field('date','Date AAAA-MM-JJ',validator:dateValidation),const Field('priority','Priorité',options:['Normale','Haute'])],initial:t);if(r!=null&&c.mounted)await perform(c,()=>store.put('tasks',r));}
    Future<void> deleteTask() async {if(await confirm(c,'Supprimer la tâche ?',t['title'])&&c.mounted)await perform(c,()=>store.remove('tasks',t['id']));}
    final actions=< (String,IconData,VoidCallback)>[('Modifier',Icons.edit_outlined,changeTask),('Supprimer',Icons.delete_outline,deleteTask)];
    return Card(child:ListTile(leading:Checkbox(value:t['done'],onChanged:(v)=>perform(c,()=>store.put('tasks',{...t,'done':v}))),title:Text(t['title']),subtitle:Text('${t['date']} · ${t['priority']}'),onTap:()=>detail(c,t['title'],[Text('Échéance : ${t['date']}'),Text('Priorité : ${t['priority']}'),Text(t['done']==true?'Terminée':'À faire')]),onLongPress:()=>recordOptions(c,actions),trailing:optionsButton(actions)));
   }),
   Row(children:[Expanded(child:section('Cette semaine')),IconButton(tooltip:'Tableau de la semaine',icon:const Icon(Icons.calendar_view_week_outlined),onPressed:()=>Navigator.push(context,MaterialPageRoute<void>(builder:(_)=>TimetableScreen(initialDay:day.weekday,initialWeek:true))))]),for(var i=1;i<=7;i++)tile(days[i-1],'${store.rows('slots').where((s)=>s['day']==i).length} cours',icon:Icons.event_note_outlined,onTap:()=>Navigator.push(context,MaterialPageRoute<void>(builder:(_)=>DayCoursesScreen(weekday:i)))),
  ]));
 }
}

class Classes extends StatelessWidget {
 const Classes({super.key});
 Future<void> add(BuildContext c) async {
  final result=await edit(c,'Nouvelle classe',[Field('name','Nom de la classe',validator:requiredText),const Field('level','Niveau',options:levels),const Field('year','Année scolaire')],initial:{'year':'2026–2027'});
  if(result!=null&&c.mounted){await perform(c,()=>store.put('classes',{'id':uid(),...result}));}
 }
 Future<void> rename(BuildContext c,Map<String,dynamic> value) async {final r=await edit(c,'Modifier la classe',[Field('name','Nom',validator:requiredText),const Field('level','Niveau',options:levels),const Field('year','Année scolaire')],initial:value);if(r!=null&&c.mounted)await perform(c,()=>store.put('classes',r));}
 Future<void> delete(BuildContext c,Map<String,dynamic> value) async {if(!await confirm(c,'Supprimer toute la classe ?','Les élèves, présences et évaluations associés seront supprimés.'))return;if(!c.mounted)return;await perform(c,()=>store.change((d){final ids=(d['pupils'] as List).where((p)=>p['classId']==value['id']).map((p)=>p['id']).toSet();for(final k in ['pupils','evaluations']){(d[k] as List).removeWhere((p)=>p['classId']==value['id']);}(d['attendance'] as List).removeWhere((p)=>ids.contains(p['pupilId']));(d['classes'] as List).removeWhere((p)=>p['id']==value['id']);}));}
 @override Widget build(BuildContext context)=>refreshable(ListView(padding:const EdgeInsets.all(16),physics:const AlwaysScrollableScrollPhysics(),children:[
  Text('Mes classes' ,style:Theme.of(context).textTheme.headlineSmall),const SizedBox(height:12),FilledButton.icon(onPressed:()=>add(context),icon:const Icon(Icons.add),label:const Text('Créer une classe')),
  if(store.rows('classes').isEmpty)empty('Créez une classe, puis ajoutez ses élèves pour faire l’appel et saisir les évaluations.'),
  for(final c in store.rows('classes'))Builder(builder:(itemContext){final actions=< (String,IconData,VoidCallback)>[('Modifier',Icons.edit_outlined,()=>rename(itemContext,c)),('Supprimer',Icons.delete_outline,()=>delete(itemContext,c))];return tile(c['name'],'${c['level']} · ${c['year']} · ${store.rows('pupils').where((p)=>p['classId']==c['id']).length} élèves',icon:Icons.groups,onTap:()=>Navigator.push(context,MaterialPageRoute<void>(builder:(_)=>ClassDetail(classId:c['id']))),onLongPress:()=>recordOptions(itemContext,actions),trailing:optionsButton(actions));}),
 ]));
}
class ClassDetail extends StatefulWidget { final String classId; const ClassDetail({super.key,required this.classId}); @override State<ClassDetail> createState()=>_ClassDetailState(); }
class _ClassDetailState extends State<ClassDetail> {
 DateTime date=DateTime.now();
 List<Map<String,dynamic>> get pupils=>store.rows('pupils').where((p)=>p['classId']==widget.classId).toList()..sort((a,b)=>fold(a['name']).compareTo(fold(b['name'])));
 List<Map<String,dynamic>> get evals=>store.rows('evaluations').where((p)=>p['classId']==widget.classId).toList();
 Future<void> pupil([Map<String,dynamic>? existing]) async {
  final result=await edit(context,'Élève',[Field('name','Prénom et nom',validator:requiredText),const Field('reference','Matricule (facultatif)'),const Field('guardianName','Nom parent / tuteur'),Field('guardianPhone','Téléphone parent / tuteur',validator:(v)=>v.isEmpty||RegExp(r'^\+?[0-9 ()-]{7,20}$').hasMatch(v)?null:'Numéro de téléphone invalide.')],initial:existing);
  if(result!=null&&mounted){await perform(context,()=>store.put('pupils',{'id':existing?['id']??uid(),...result,'classId':widget.classId}));}
 }
 Future<void> evaluation([Map<String,dynamic>? existing]) async {
  if(pupils.isEmpty){message(context,'Ajoutez d’abord les élèves.');return;}
  final result=await edit(context,'Évaluation',[
   Field('title','Matière et intitulé',validator:requiredText),Field('date','Date AAAA-MM-JJ',validator:dateValidation),Field('max','Barème',validator:positive),Field('weight','Coefficient',validator:positive),
   for(final p in pupils)Field('score_${p['id']}',p['name'],validator:(v)=>v.isEmpty?null:(number(v)!=null&&number(v)!.isFinite&&number(v)!>=0?null:'Note positive ou champ vide.')),
  ],initial:{'date':dateKey(date),'max':'20','weight':'1',...?existing,for(final p in pupils)'score_${p['id']}':existing==null?'':(existing['scores'] as Map)[p['id']]?.toString()??''});
  if(result==null||!mounted)return;
  final max=number(result['max'])!,weight=number(result['weight'])!;final scores=<String,double>{};
  for(final p in pupils){final v=number(result.remove('score_${p['id']}'));if(v!=null){if(v>max){message(context,'La note de ${p['name']} dépasse le barème.');return;}scores[p['id']]=v;}}
  await perform(context,()=>store.put('evaluations',{'id':existing?['id']??uid(),...result,'classId':widget.classId,'max':max,'weight':weight,'scores':scores}));
 }
 @override Widget build(BuildContext context)=>ListenableBuilder(listenable:store,builder:(context,_) {
  final current=store.rows('classes').where((c)=>c['id']==widget.classId).firstOrNull;
  if(current==null)return const Scaffold(body:Center(child:Text('Classe supprimée')));
  return DefaultTabController(length:4,child:Scaffold(appBar:AppBar(title:Text(current['name']),actions:[PopupMenuButton<String>(onSelected:(v) async {
   if(v=='rename') {
    final next=await edit(context,'Modifier la classe',[Field('name','Nom',validator:requiredText),const Field('level','Niveau',options:levels),const Field('year','Année scolaire')],initial:current);
    if(next!=null&&context.mounted){await perform(context,()=>store.put('classes',next));}
   } else if(await confirm(context,'Supprimer toute la classe ?','Les élèves, présences et évaluations associés seront supprimés. Exportez une sauvegarde si nécessaire.')&&context.mounted){
    await perform(context,()=>store.change((d){final ids=(d['pupils'] as List).where((p)=>p['classId']==widget.classId).map((p)=>p['id']).toSet();for(final k in ['pupils','evaluations']){(d[k] as List).removeWhere((p)=>p['classId']==widget.classId);}(d['attendance'] as List).removeWhere((p)=>ids.contains(p['pupilId']));(d['classes'] as List).removeWhere((p)=>p['id']==widget.classId);}));
    if(context.mounted){Navigator.pop(context);}
   }
  },itemBuilder:(_)=>const [PopupMenuItem(value:'rename',child:Text('Modifier')),PopupMenuItem(value:'delete',child:Text('Supprimer la classe'))])],bottom:const TabBar(isScrollable:true,tabAlignment:TabAlignment.start,tabs:[Tab(text:'Élèves'),Tab(text:'Appel'),Tab(text:'Notes'),Tab(text:'Appréciation') ])),body:TabBarView(children:[
   refreshable(ListView(padding:const EdgeInsets.all(16),physics:const AlwaysScrollableScrollPhysics(),children:[FilledButton.icon(onPressed:pupil,icon:const Icon(Icons.person_add_alt),label:const Text('Ajouter un élève')),if(pupils.isEmpty)empty('Aucun élève.'),for(final p in pupils)Builder(builder:(itemContext){
    Future<void> deletePupil() async {if(await confirm(itemContext,'Supprimer cet élève ?','Ses présences et notes seront retirées.')&&itemContext.mounted){await perform(itemContext,()=>store.change((d){(d['pupils'] as List).removeWhere((v)=>v['id']==p['id']);(d['attendance'] as List).removeWhere((v)=>v['pupilId']==p['id']);for(final e in d['evaluations']){(e['scores'] as Map).remove(p['id']);}}));}}
    final actions=< (String,IconData,VoidCallback)>[('Modifier',Icons.edit_outlined,()=>pupil(p)),('Supprimer',Icons.delete_outline,deletePupil)];
    return tile(p['name'],p['reference']??'',icon:Icons.person_outline,onTap:()=>Navigator.push(itemContext,MaterialPageRoute<void>(builder:(_)=>PupilDetail(pupilId:p['id']))),onLongPress:()=>recordOptions(itemContext,actions),trailing:optionsButton(actions));
   })])),
   refreshable(ListView(padding:const EdgeInsets.all(16),physics:const AlwaysScrollableScrollPhysics(),children:[OutlinedButton.icon(onPressed:() async {final d=await showDatePicker(context:context,initialDate:date,firstDate:DateTime(2020),lastDate:DateTime(2100));if(d!=null)setState(()=>date=d);},icon:const Icon(Icons.today),label:Text(frenchDate(date))),const Text('Un statut non renseigné reste « Non pointé ». Chaque choix est enregistré immédiatement.'),for(final p in pupils)Card(child:Padding(padding:const EdgeInsets.all(12),child:Column(crossAxisAlignment:CrossAxisAlignment.start,children:[Text(p['name']),const SizedBox(height:8),DropdownButtonFormField<String>(key:ValueKey('${p['id']}_${dateKey(date)}'),initialValue:store.rows('attendance').where((a)=>a['pupilId']==p['id']&&a['date']==dateKey(date)).firstOrNull?['status'],hint:const Text('Non pointé'),items:['Présent','Absent','Retard','Excusé'].map((s)=>DropdownMenuItem(value:s,child:Text(s))).toList(),onChanged:(v)=>perform(context,()=>store.put('attendance',{'id':'${p['id']}_${dateKey(date)}','pupilId':p['id'],'date':dateKey(date),'status':v})))]))),section('Bilan des absences'),for(final p in pupils)tile(p['name'],'${store.rows('attendance').where((a)=>a['pupilId']==p['id']&&a['status']=='Absent').length} absence(s) sur les appels renseignés',onTap:()=>Navigator.push(context,MaterialPageRoute<void>(builder:(_)=>PupilDetail(pupilId:p['id']))))])),
   refreshable(ListView(padding:const EdgeInsets.all(16),physics:const AlwaysScrollableScrollPhysics(),children:[FilledButton.icon(onPressed:evaluation,icon:const Icon(Icons.add_chart),label:const Text('Ajouter une évaluation')),const SizedBox(height:12),const Text('Moyenne générale sur 20 = somme des notes ramenées sur 20 × coefficient, divisée par la somme des coefficients renseignés. Une case vide n’est pas un zéro.'),for(final e in evals)Builder(builder:(itemContext){
    Future<void> deleteEvaluation() async {if(await confirm(itemContext,'Supprimer cette évaluation ?',e['title'])&&itemContext.mounted)await perform(itemContext,()=>store.remove('evaluations',e['id']));}
    final actions=< (String,IconData,VoidCallback)>[('Modifier',Icons.edit_outlined,()=>evaluation(e)),('Supprimer',Icons.delete_outline,deleteEvaluation)];
    return tile(e['title'],'${e['date']} · /${e['max']} · coef. ${e['weight']}',onTap:()=>detail(itemContext,e['title'],[Text('Date : ${e['date']} · Barème : ${e['max']} · Coefficient : ${e['weight']}'),section('Notes des élèves'),for(final p in pupils)Text('${p['name']} : ${(e['scores'] as Map)[p['id']]?.toString()??'Non noté'} / ${e['max']}')]),onLongPress:()=>recordOptions(itemContext,actions),trailing:optionsButton(actions));
   }),section('Moyennes générales'),for(final p in pupils)tile(p['name'],average(evals,p['id'])==null?'Aucune note':'${average(evals,p['id'])!.toStringAsFixed(2)} / 20',icon:Icons.analytics_outlined,onTap:()=>Navigator.push(context,MaterialPageRoute<void>(builder:(_)=>PupilDetail(pupilId:p['id']))))])),
   AppreciationPanel(classId:widget.classId),
  ])));
 });
}

class PupilDetail extends StatelessWidget {
 final String pupilId;
 const PupilDetail({super.key,required this.pupilId});
 @override Widget build(BuildContext context)=>ListenableBuilder(listenable:store,builder:(context,_){
  final p=store.rows('pupils').where((v)=>v['id']==pupilId).firstOrNull;
  if(p==null)return const Scaffold(body:Center(child:Text('Élève supprimé')));
  final exams=store.rows('evaluations').where((e)=>e['classId']==p['classId']).toList()..sort((a,b)=>b['date'].compareTo(a['date']));
  final attend=store.rows('attendance').where((a)=>a['pupilId']==pupilId).toList()..sort((a,b)=>b['date'].compareTo(a['date']));
  final scored=exams.where((e)=>(e['scores'] as Map).containsKey(pupilId)).toList();
  final absent=attend.where((a)=>a['status']=='Absent').length;
  final late=attend.where((a)=>a['status']=='Retard').length;
  final excused=attend.where((a)=>a['status']=='Excusé').length;
  return Scaffold(appBar:AppBar(title:Text(p['name'])),body:refreshable(ListView(physics:const AlwaysScrollableScrollPhysics(),padding:const EdgeInsets.all(16),children:[
   section('Informations'),tile('Matricule',p['reference']?.toString().isNotEmpty==true?p['reference']:'Non renseigné'),tile('Parent / tuteur',p['guardianName']?.toString().isNotEmpty==true?p['guardianName']:'Non renseigné'),tile('Téléphone parent / tuteur',p['guardianPhone']?.toString().isNotEmpty==true?p['guardianPhone']:'Non renseigné'),
   section('Bilan'),tile('Moyenne générale',average(exams,pupilId)==null?'Aucune note':'${average(exams,pupilId)!.toStringAsFixed(2)} / 20'),tile('Appels','${attend.length} renseigné(s) · $absent absence(s) · $late retard(s) · $excused excusé(s)'),
   section('Évaluations et notes'),if(exams.isEmpty)empty('Aucune évaluation.'),for(final e in exams)tile(e['title'],'${e['date']} · ${(e['scores'] as Map)[pupilId]?.toString()??'Non noté'} / ${e['max']} · coef. ${e['weight']}'),if(exams.isNotEmpty)Text('${scored.length} évaluation(s) notée(s) sur ${exams.length}.'),
   section('Présences et retards'),if(attend.isEmpty)empty('Aucun appel renseigné.'),for(final a in attend)tile(a['date'],a['status'],icon:a['status']=='Présent'?Icons.check_circle_outline:Icons.event_busy_outlined),
  ])));
 });
}

class Notes extends StatefulWidget { const Notes({super.key}); @override State<Notes> createState()=>_NotesState(); }
class _NotesState extends State<Notes> {
 String query='',kind='Tous';
 Future<void> write([Map<String,dynamic>? initial]) async {
  final r=await edit(context,'Carnet enseignant',[
   Field('title','Titre',validator:requiredText),const Field('kind','Type',options:['Note','Préparation','Cahier de textes','Réunion']),const Field('level','Niveau',options:levels),const Field('subject','Matière / thème'),const Field('objective','Objectif'),Field('body','Contenu / déroulement',lines:5,validator:requiredText),const Field('assessment','Évaluation / devoirs',lines:2),
  ],initial:initial);
  if(r!=null&&mounted){await perform(context,()=>store.put('notes',{'id':initial?['id']??uid(),...r,'updated':DateTime.now().toIso8601String(),'pinned':r['pinned']??false}));}
 }
 void view(Map<String,dynamic> n)=>showModalBottomSheet<void>(context:context,isScrollControlled:true,showDragHandle:true,builder:(c)=>SafeArea(child:DraggableScrollableSheet(expand:false,initialChildSize:0.8,minChildSize:0.3,maxChildSize:0.95,builder:(c,scroll)=>ListView(controller:scroll,padding:const EdgeInsets.all(20),children:[Text(n['title'],style:Theme.of(c).textTheme.headlineSmall),Text('${n['kind']} · ${n['level']} · ${n['subject']}'),if((n['objective']??'').isNotEmpty)...[section('Objectif'),SelectableText(n['objective'])],section('Contenu'),SelectableText(n['body']),if((n['assessment']??'').isNotEmpty)...[section('Évaluation / devoirs'),SelectableText(n['assessment'])],const SizedBox(height:20),FilledButton(onPressed:(){Navigator.pop(c);write(n);},child:const Text('Modifier'))]))));
 @override Widget build(BuildContext context){
  final rows=store.rows('notes').where((n)=>(kind=='Tous'||n['kind']==kind)&&fold('${n['title']} ${n['body']} ${n['subject']} ${n['level']}').contains(fold(query))).toList()..sort((a,b){final p=(b['pinned']==true?1:0)-(a['pinned']==true?1:0);return p!=0?p:(b['updated']??'').compareTo(a['updated']??'');});
  return refreshable(CustomScrollView(physics:const AlwaysScrollableScrollPhysics(),slivers:[SliverToBoxAdapter(child:Padding(padding:const EdgeInsets.all(16),child:Column(crossAxisAlignment:CrossAxisAlignment.start,children:[Text('Mon carnet',style:Theme.of(context).textTheme.headlineSmall),const SizedBox(height:12),TextField(decoration:const InputDecoration(labelText:'Rechercher dans le carnet',prefixIcon:Icon(Icons.search)),onChanged:(v)=>setState(()=>query=v)),const SizedBox(height:10),Wrap(spacing:6,children:['Tous','Note','Préparation','Cahier de textes','Réunion'].map((s)=>ChoiceChip(label:Text(s),selected:kind==s,onSelected:(_)=>setState(()=>kind=s))).toList()),FilledButton.icon(onPressed:write,icon:const Icon(Icons.add),label:const Text('Nouvelle note'))]))),if(rows.isEmpty)SliverToBoxAdapter(child:empty('Aucune note correspondante.')),SliverList.builder(itemCount:rows.length,itemBuilder:(c,i){final n=rows[i];return Padding(padding:const EdgeInsets.symmetric(horizontal:16),child:tile(n['title'],'${n['kind']} · ${n['level']}\n${n['body'].toString().replaceAll('\n',' ').substring(0,n['body'].toString().length>140?140:n['body'].toString().length)}${n['body'].toString().length>140?'…':''}',icon:n['pinned']==true?Icons.push_pin:Icons.notes,onTap:()=>view(n),onLongPress:()=>recordOptions(c,[('Épingler / détacher',Icons.push_pin_outlined,()=>perform(c,()=>store.put('notes',{...n,'pinned':n['pinned']!=true}))),('Modifier',Icons.edit_outlined,()=>write(n)),('Supprimer',Icons.delete_outline,() async {if(await confirm(c,'Supprimer cette note ?',n['title'])&&c.mounted)await perform(c,()=>store.remove('notes',n['id']));})]),trailing:PopupMenuButton<String>(onSelected:(v) async {if(v=='pin'){await perform(c,()=>store.put('notes',{...n,'pinned':n['pinned']!=true}));}else if(v=='edit'){write(n);}else if(await confirm(c,'Supprimer cette note ?',n['title'])&&c.mounted){await perform(c,()=>store.remove('notes',n['id']));}},itemBuilder:(_)=>[PopupMenuItem(value:'pin',child:Text(n['pinned']==true?'Détacher':'Épingler')),const PopupMenuItem(value:'edit',child:Text('Modifier')),const PopupMenuItem(value:'delete',child:Text('Supprimer'))])));})]));
 }
}

class Settings extends StatelessWidget {
 const Settings({super.key});
 @override Widget build(BuildContext context)=>ListenableBuilder(listenable:store,builder:(context,_)=>Scaffold(appBar:AppBar(title:const Text('Infos & À propos')),body:ListView(padding:const EdgeInsets.all(20),children:[
  Center(child:Image.asset('assets/images/icon.png',width:86,height:86)),section('Enseignant · 2.2.0'),const Text('Apprendre, préparer et enseigner. Compagnon local pour les enseignants du primaire. Les fiches originales sont une base pédagogique à adapter au programme et au contexte de la classe.'),
  section('Apparence'),DropdownButtonFormField<String>(initialValue:store.data['theme'],items:const [DropdownMenuItem(value:'system',child:Text('Automatique')),DropdownMenuItem(value:'light',child:Text('Clair')),DropdownMenuItem(value:'dark',child:Text('Sombre'))],onChanged:(v)=>perform(context,()=>store.change((d)=>d['theme']=v))),
  section('Taille de lecture'),Slider(value:(store.data['font'] as num).toDouble(),min:0.8,max:1.6,divisions:8,label:'${((store.data['font'] as num)*100).round()} %',onChanged:(v)=>perform(context,()=>store.change((d)=>d['font']=v))),
  section('Sauvegarde'),const Text('Les données sont stockées sur ce téléphone. Une désinstallation peut les effacer. Exportez régulièrement une sauvegarde et conservez-la dans un endroit privé.'),
  tile('Exporter une sauvegarde','Classes, élèves, présences, notes, carnet, favoris et réglages',icon:Icons.save_alt,onTap:()=>perform(context,() async {final ok=await bridge.invokeMethod<bool>('export',jsonEncode(store.data));if(ok==true&&context.mounted){message(context,'Sauvegarde exportée.');}})),
  tile('Restaurer une sauvegarde','Remplace les données actuelles après validation',icon:Icons.restore,onTap:()=>perform(context,() async {final raw=await bridge.invokeMethod<String>('import');if(raw==null)return;final decoded=Map<String,dynamic>.from(jsonDecode(raw) as Map);validateData(decoded);if(context.mounted&&await confirm(context,'Restaurer cette sauvegarde ?','Les données actuelles seront remplacées. Exportez-les d’abord si vous souhaitez les conserver.')){await store.restore(raw);if(context.mounted)message(context,'Sauvegarde restaurée.');}})),
  section('Développeur'),Center(child:Image.asset('assets/images/logo_tdg.png',width:150,height:150)),const SizedBox(height:12),const Text('Taysir Digital Group (TDG)\nVos rêves, nos défis\nAliou Mbengue — PDG / Développeur'),
  tile('+221 76 455 03 58','Appeler',icon:Icons.phone_outlined,onTap:()=>perform(context,()=>bridge.invokeMethod<void>('openUrl','tel:+221764550358'))),
  tile('taysirdigitalgroup@gmail.com','E-mail',icon:Icons.mail_outline,onTap:()=>perform(context,()=>bridge.invokeMethod<void>('openUrl','mailto:taysirdigitalgroup@gmail.com'))),
  tile('Site web TDG','taysirdigitalgroup.github.io',icon:Icons.language,onTap:()=>perform(context,()=>bridge.invokeMethod<void>('openUrl','https://taysirdigitalgroup.github.io/'))),
  section('Sources et crédits'),const Text('Grevisse : Jean-Christophe Pellat et Stéphanie Fonvielle, Le Grevisse de l’enseignant, Grammaire de référence, Magnard. Copie fournie par l’utilisateur, transformée en pages et index OCR. Application indépendante, sans affiliation à l’éditeur. L’OCR peut être inexact : consulter la page scannée. Les droits du livre restent ceux de leurs titulaires. Vérifier les autorisations avant toute diffusion publique du projet avec le livre.\n\nFiches Savoirs : contenus originaux TDG, édition initiale, non homologués comme programme officiel sénégalais. Pas de collecte réseau ni de publicité dans cette version.'),
  section('Dictionnaire de poche'),const Text('Wiktionnaire et FranceTerme : consultation hors connexion de définitions générales, scientifiques et techniques. Les licences et provenances sont disponibles dans le dictionnaire.'),
  const SizedBox(height:24),const Text('© 2026 Taysir Digital Group — Vos rêves, nos défis',textAlign:TextAlign.center),
 ])));
}
