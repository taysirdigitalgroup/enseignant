import 'package:flutter/material.dart';
import 'core.dart';
import 'main.dart' show store, days, detail, empty, section, refreshable, PupilDetail;

String slotSubject(Map<String,dynamic> slot) {
 final named=slot['subject']?.toString().trim()??'';
 return named.isNotEmpty?named:slot['title'].toString().split(RegExp(r'[/·|]')).first.trim();
}
Color subjectColor(String subject) {
 final text=fold(subject);
 const palette=[Color(0xff1d4ed8),Color(0xff047857),Color(0xff7e22ce),Color(0xffb45309),Color(0xffbe123c),Color(0xff0369a1),Color(0xff6d28d9),Color(0xff0f766e)];
 for(final entry in <String,int>{'franc':0,'math':1,'arab':2,'scien':3,'histo':4,'geo':5,'civi':6,'eps':7,'sport':7,'art':2}.entries){if(text.contains(entry.key))return palette[entry.value];}
 var hash=0;for(final c in text.runes){hash=(hash*31+c)%palette.length;}return palette[hash];
}
void courseDetails(BuildContext context,Map<String,dynamic> slot)=>detail(context,slot['title'],[
 section(slotSubject(slot)),Text('${days[(slot['day'] as int)-1]} · ${slot['start']} – ${slot['end']}'),
 section('Salle / lieu'),Text(slot['place']?.toString().isNotEmpty==true?slot['place']:'Non renseigné'),
 const SizedBox(height:16),const Text('Créneau récurrent chaque semaine.'),
]);
Widget courseCard(BuildContext context,Map<String,dynamic> s)=>Card(clipBehavior:Clip.antiAlias,child:InkWell(onTap:()=>courseDetails(context,s),child:IntrinsicHeight(child:Row(children:[Container(width:6,color:subjectColor(slotSubject(s))),Expanded(child:Padding(padding:const EdgeInsets.all(14),child:Column(crossAxisAlignment:CrossAxisAlignment.start,children:[Text('${s['start']} – ${s['end']}',style:TextStyle(color:subjectColor(slotSubject(s)),fontWeight:FontWeight.bold)),const SizedBox(height:6),Text(s['title'],style:const TextStyle(fontSize:17,fontWeight:FontWeight.w700)),Text('${slotSubject(s)} · Salle : ${s['place']?.toString().isNotEmpty==true?s['place']:'à préciser'}')]))),const Padding(padding:EdgeInsets.all(8),child:Icon(Icons.chevron_right))]))));
class DayCoursesScreen extends StatelessWidget {
 final int weekday;
 const DayCoursesScreen({super.key,required this.weekday});
 @override Widget build(BuildContext context)=>ListenableBuilder(listenable:store,builder:(context,_){
  final rows=store.rows('slots').where((s)=>s['day']==weekday).toList()..sort((a,b)=>a['start'].compareTo(b['start']));
  final total=rows.fold<int>(0,(sum,s)=>sum+minutes(s['end'])-minutes(s['start']));
  return Scaffold(appBar:AppBar(title:Text('Cours du ${days[weekday-1].toLowerCase()}'),actions:[IconButton(tooltip:'Tableau du jour',icon:const Icon(Icons.view_timeline_outlined),onPressed:()=>Navigator.push(context,MaterialPageRoute<void>(builder:(_)=>TimetableScreen(initialDay:weekday))))]),body:refreshable(ListView(physics:const AlwaysScrollableScrollPhysics(),padding:const EdgeInsets.all(16),children:[Text('${rows.length} cours · ${total~/60} h ${total%60} min',style:Theme.of(context).textTheme.headlineSmall),const SizedBox(height:12),if(rows.isEmpty)empty('Aucun cours prévu ce jour.'),for(final s in rows)courseCard(context,s)])));
 });
}
class TimetableScreen extends StatefulWidget {
 final int initialDay;final bool initialWeek;
 const TimetableScreen({super.key,required this.initialDay,this.initialWeek=false});
 @override State<TimetableScreen> createState()=>_TimetableScreenState();
}
class _TimetableScreenState extends State<TimetableScreen> {
 late int selected=widget.initialDay;late bool week=widget.initialWeek;
 @override Widget build(BuildContext context)=>ListenableBuilder(listenable:store,builder:(context,_){
  final slots=store.rows('slots');final shown=slots.where((s)=>week||s['day']==selected).toList();
  final visibleDays=week?[1,2,3,4,5,6,7]:[selected];
  var start=8*60,end=18*60;
  if(shown.isNotEmpty){start=shown.map((s)=>minutes(s['start'])).reduce((a,b)=>a<b?a:b)~/60*60;end=((shown.map((s)=>minutes(s['end'])).reduce((a,b)=>a>b?a:b)+59)~/60)*60;}
  final height=(end-start)*1.2;final subjects=shown.map(slotSubject).toSet().toList()..sort();
  return Scaffold(appBar:AppBar(title:Text(week?'Emploi du temps · Semaine':'Emploi du temps · ${days[selected-1]}')),body:Column(children:[
   Padding(padding:const EdgeInsets.all(12),child:Column(children:[SegmentedButton<bool>(segments:const [ButtonSegment(value:false,label:Text('Jour'),icon:Icon(Icons.view_day_outlined)),ButtonSegment(value:true,label:Text('Semaine'),icon:Icon(Icons.calendar_view_week_outlined))],selected:{week},onSelectionChanged:(v)=>setState(()=>week=v.first)),
    if(!week)SingleChildScrollView(scrollDirection:Axis.horizontal,child:Row(children:[for(var i=1;i<=7;i++)Padding(padding:const EdgeInsets.only(right:5),child:ChoiceChip(label:Text(days[i-1]),selected:selected==i,onSelected:(_)=>setState(()=>selected=i)))])),
    const SizedBox(height:8),const Text('Glissez pour parcourir le tableau. Touchez un cours pour ses détails.'),
   ])),
   if(subjects.isNotEmpty)SizedBox(height:38,child:ListView(scrollDirection:Axis.horizontal,padding:const EdgeInsets.symmetric(horizontal:12),children:[for(final subject in subjects)Padding(padding:const EdgeInsets.only(right:8),child:Chip(avatar:CircleAvatar(backgroundColor:subjectColor(subject),radius:6),label:Text(subject)))])),
   Expanded(child:LayoutBuilder(builder:(context,box){
    final col=week?180.0:(box.maxWidth-64>240?box.maxWidth-64:240.0);final width=64+col*visibleDays.length;
    return SingleChildScrollView(child:SingleChildScrollView(scrollDirection:Axis.horizontal,child:SizedBox(width:width,height:height+54,child:Column(children:[
     SizedBox(height:54,child:Row(children:[const SizedBox(width:64,child:Center(child:Icon(Icons.schedule))),for(final d in visibleDays)Container(width:col,alignment:Alignment.center,decoration:BoxDecoration(color:Theme.of(context).colorScheme.primaryContainer,border:Border.all(color:Theme.of(context).dividerColor)),child:Text(days[d-1],style:const TextStyle(fontWeight:FontWeight.bold)))])),
     SizedBox(height:height,child:Stack(children:[
      for(var t=start;t<end;t+=30)Positioned(top:(t-start)*1.2,left:0,right:0,child:Row(crossAxisAlignment:CrossAxisAlignment.start,children:[SizedBox(width:64,child:Text('${(t~/60).toString().padLeft(2,'0')}:${(t%60).toString().padLeft(2,'0')}',textAlign:TextAlign.center,style:TextStyle(fontSize:12,color:Theme.of(context).colorScheme.onSurfaceVariant))),Expanded(child:Divider(height:1,color:Theme.of(context).dividerColor.withValues(alpha:t%60==0?0.7:0.25)))])),
      for(var d=0;d<visibleDays.length;d++)Positioned(left:64+d*col,top:0,bottom:0,child:VerticalDivider(width:1,color:Theme.of(context).dividerColor)),
      for(final s in shown)Positioned(left:64+visibleDays.indexOf(s['day'] as int)*col+4,top:(minutes(s['start'])-start)*1.2+2,width:col-8,height:(minutes(s['end'])-minutes(s['start']))*1.2,child:Material(color:subjectColor(slotSubject(s)),borderRadius:BorderRadius.circular(12),clipBehavior:Clip.antiAlias,child:InkWell(onTap:()=>courseDetails(context,s),child:LayoutBuilder(builder:(context,bounds)=>bounds.maxHeight<28?FittedBox(child:Text(s['title'],style:const TextStyle(color:Colors.white))):Padding(padding:const EdgeInsets.all(7),child:Column(crossAxisAlignment:CrossAxisAlignment.start,children:[Expanded(child:Text(s['title'],maxLines:bounds.maxHeight>65?2:1,overflow:TextOverflow.ellipsis,style:const TextStyle(color:Colors.white,fontWeight:FontWeight.bold))),if(bounds.maxHeight>43)Text('${s['start']} – ${s['end']}',style:const TextStyle(color:Colors.white,fontSize:12)),if(bounds.maxHeight>67)Text('Salle : ${s['place']?.toString().isNotEmpty==true?s['place']:'—'}',maxLines:1,overflow:TextOverflow.ellipsis,style:const TextStyle(color:Colors.white,fontSize:12))])))))),
     ])),
    ]))));
   })),
  ]));
 });
}

class PupilAssessment {
 final Map<String,dynamic> pupil;final double? mean;final int marks,examCount,present,absent,late,excused;final String group;final Color color;final List<String> advice;
 const PupilAssessment({required this.pupil,required this.mean,required this.marks,required this.examCount,required this.present,required this.absent,required this.late,required this.excused,required this.group,required this.color,required this.advice});
 int get calls=>present+absent+late+excused;
}
PupilAssessment assessPupil(Map<String,dynamic> p,List<Map<String,dynamic>> exams,List<Map<String,dynamic>> calls) {
 final markCount=exams.where((e)=>(e['scores'] as Map).containsKey(p['id'])).length;
 final mean=average(exams,p['id']);final rows=calls.where((a)=>a['pupilId']==p['id']).toList();
 int count(String status)=>rows.where((a)=>a['status']==status).length;
 final absent=count('Absent'),late=count('Retard'),excused=count('Excusé');
 String group;Color color;final advice=<String>[];
 if(mean==null){group='Données limitées';color=const Color(0xff64748b);advice.add('Saisir une première évaluation pour identifier les acquis et les besoins.');}
 else if(markCount<2){group='Données limitées';color=const Color(0xff64748b);advice.add('Une seule note : confirmer les observations par une autre activité avant une appréciation durable.');}
 else if(mean<10){group='À accompagner';color=const Color(0xffb45309);advice.add(mean<8?'Prévoir une remédiation ciblée en petit groupe et vérifier les prérequis.':'Reprendre les notions fragiles avec un exemple guidé, puis vérifier la réussite en autonomie.');}
 else if(mean<14){group='À consolider';color=const Color(0xff1d4ed8);advice.add('Encourager les acquis et renforcer la régularité par de courts entraînements.');}
 else{group='À encourager';color=const Color(0xff047857);advice.add(mean>=16?'Féliciter les réussites et proposer un approfondissement adapté.':'Valoriser le travail et proposer un défi accessible pour poursuivre la progression.');}
 if(absent>0)advice.add('$absent absence(s) enregistrée(s) : vérifier le contexte et prévoir le rattrapage des apprentissages manqués.');
 if(late>=2)advice.add('$late retards : rechercher les causes avec la famille et convenir d’un objectif réaliste de ponctualité.');
 else if(late==1)advice.add('Un retard renseigné : suivre l’évolution avant de conclure à une difficulté régulière.');
 if(excused>0)advice.add('$excused absence(s) excusée(s) : prévoir une reprise des contenus concernés.');
 if(rows.isEmpty)advice.add('Aucun appel renseigné sur la période : assiduité non interprétable.');
 else if(absent==0&&late==0)advice.add('Valoriser la ponctualité et la présence dans les appels renseignés.');
 if(markCount<exams.length)advice.add('${exams.length-markCount} évaluation(s) non notée(s) : compléter si pertinent, sans transformer les cases vides en zéro.');
 return PupilAssessment(pupil:p,mean:mean,marks:markCount,examCount:exams.length,present:count('Présent'),absent:absent,late:late,excused:excused,group:group,color:color,advice:advice);
}
class AppreciationPanel extends StatefulWidget {
 final String classId;
 const AppreciationPanel({super.key,required this.classId});
 @override State<AppreciationPanel> createState()=>_AppreciationPanelState();
}
class _AppreciationPanelState extends State<AppreciationPanel> {
 String filter='Tous',query='';DateTime? from,to;
 bool inPeriod(String value){final d=DateTime.tryParse(value);return d!=null&&(from==null||!d.isBefore(from!))&&(to==null||!d.isAfter(to!));}
 Future<void> pick(bool start) async {final d=await showDatePicker(context:context,initialDate:(start?from:to)??DateTime.now(),firstDate:DateTime(2020),lastDate:DateTime(2100));if(d!=null&&mounted){if(start&&to!=null&&d.isAfter(to!))return;if(!start&&from!=null&&d.isBefore(from!))return;setState((){if(start){from=d;}else{to=d;}});}}
 @override Widget build(BuildContext context)=>ListenableBuilder(listenable:store,builder:(context,_){
  final pupils=store.rows('pupils').where((p)=>p['classId']==widget.classId).toList();final ids=pupils.map((p)=>p['id']).toSet();
  final exams=store.rows('evaluations').where((e)=>e['classId']==widget.classId&&inPeriod(e['date'])).toList();
  final calls=store.rows('attendance').where((a)=>ids.contains(a['pupilId'])&&inPeriod(a['date'])).toList();
  final reports=pupils.map((p)=>assessPupil(p,exams,calls)).toList()..sort((a,b)=>fold(a.pupil['name']).compareTo(fold(b.pupil['name'])));
  final means=reports.where((r)=>r.mean!=null).map((r)=>r.mean!).toList();
  final visible=reports.where((r)=>fold(r.pupil['name']).contains(fold(query))&&(filter=='Tous'||filter==r.group||(filter=='Assiduité'&&(r.absent>0||r.late>0)))).toList();
  return refreshable(ListView(physics:const AlwaysScrollableScrollPhysics(),padding:const EdgeInsets.all(16),children:[
   Text('Repères pour accompagner',style:Theme.of(context).textTheme.headlineSmall),const Text('Suggestions automatiques à relire par l’enseignant. Les chiffres concernent uniquement les notes et appels renseignés, jamais les jours non pointés.'),
   const SizedBox(height:12),Wrap(spacing:8,runSpacing:8,children:[_metric('Élèves','${pupils.length}',Icons.groups_outlined),_metric('Moyenne des élèves notés',means.isEmpty?'—':'${(means.reduce((a,b)=>a+b)/means.length).toStringAsFixed(1)} /20',Icons.analytics_outlined),_metric('À accompagner','${reports.where((r)=>r.group=='À accompagner').length}',Icons.support_agent),_metric('Assiduité à vérifier','${reports.where((r)=>r.absent>0||r.late>0).length}',Icons.event_note)]),
   const SizedBox(height:12),Wrap(spacing:6,children:[OutlinedButton(onPressed:()=>pick(true),child:Text(from==null?'Depuis : tout':frenchDate(from!))),OutlinedButton(onPressed:()=>pick(false),child:Text(to==null?'Jusqu’au : tout':frenchDate(to!))),TextButton(onPressed:()=>setState((){from=null;to=null;}),child:const Text('Toutes les dates'))]),
   TextField(decoration:const InputDecoration(labelText:'Rechercher un élève',prefixIcon:Icon(Icons.search)),onChanged:(v)=>setState(()=>query=v)),
   Wrap(spacing:6,children:['Tous','À accompagner','À consolider','À encourager','Assiduité','Données limitées'].map((f)=>ChoiceChip(label:Text(f),selected:filter==f,onSelected:(_)=>setState(()=>filter=f))).toList()),
   ExpansionTile(title:const Text('Comprendre les repères'),children:const [Padding(padding:EdgeInsets.all(12),child:Text('À partir de deux notes : moyenne <10 → accompagnement ; de 10 à moins de 14 → consolidation ; ≥14 → encouragement. Avec zéro ou une note, les données sont limitées. Ce sont des repères internes, pas des seuils officiels de décision. Une absence ne diminue jamais automatiquement une note.'))]),
   if(visible.isEmpty)empty('Aucun élève correspondant à ces critères.'),
   for(final group in ['À accompagner','À consolider','À encourager','Données limitées'])if(visible.any((r)=>r.group==group))...[
    section(group),for(final r in visible.where((r)=>r.group==group))Card(clipBehavior:Clip.antiAlias,child:InkWell(onTap:()=>Navigator.push(context,MaterialPageRoute<void>(builder:(_)=>PupilDetail(pupilId:r.pupil['id']))),child:Padding(padding:const EdgeInsets.all(14),child:Column(crossAxisAlignment:CrossAxisAlignment.start,children:[
     Row(children:[CircleAvatar(backgroundColor:r.color,foregroundColor:Colors.white,child:Icon(r.group=='À accompagner'?Icons.school_outlined:r.group=='Données limitées'?Icons.info_outline:Icons.trending_up)),const SizedBox(width:10),Expanded(child:Text(r.pupil['name'],style:const TextStyle(fontSize:18,fontWeight:FontWeight.bold))),Text(r.mean==null?'—':'${r.mean!.toStringAsFixed(1)}/20',style:TextStyle(color:r.color,fontSize:19,fontWeight:FontWeight.w800))]),
     const SizedBox(height:10),Wrap(spacing:6,runSpacing:6,children:[Chip(label:Text('${r.marks}/${r.examCount} notes')),Chip(label:Text('${r.present} présences')),Chip(backgroundColor:r.absent>0?Theme.of(context).colorScheme.errorContainer:null,label:Text('${r.absent} absences')),Chip(backgroundColor:r.late>0?Theme.of(context).colorScheme.tertiaryContainer:null,label:Text('${r.late} retards')),Chip(label:Text('${r.excused} excusées'))]),
     for(final a in r.advice)Padding(padding:const EdgeInsets.only(top:7),child:Text('• $a')),
    ]))))],
  ]));
 });
 Widget _metric(String label,String value,IconData icon)=>SizedBox(width:160,child:Card(child:Padding(padding:const EdgeInsets.all(12),child:Column(crossAxisAlignment:CrossAxisAlignment.start,children:[Icon(icon),const SizedBox(height:8),Text(value,style:const TextStyle(fontSize:23,fontWeight:FontWeight.w800)),Text(label)]))));
}
