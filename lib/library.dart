import 'dart:async';
import 'dart:convert';
import 'package:flutter/foundation.dart';
import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'core.dart';
import 'main.dart' show store, perform, message, tile, section, empty, refreshable, recordOptions, optionsButton;

Future<List<Map<String,dynamic>>> loadList(String path) async => (jsonDecode(await rootBundle.loadString(path)) as List).map((v)=>Map<String,dynamic>.from(v as Map)).toList();
class Knowledge extends StatefulWidget { const Knowledge({super.key}); @override State<Knowledge> createState()=>_KnowledgeState(); }
class _KnowledgeState extends State<Knowledge> {
 late final Future<List<Map<String,dynamic>>> loading=loadList('assets/data/lessons.json');
 String query='',subject='Toutes',level='Tous',domain='Tous les domaines',progress='Tout';bool favorites=false;
 @override Widget build(BuildContext context)=>FutureBuilder<List<Map<String,dynamic>>>(future:loading,builder:(context,s){
  if(s.hasError)return empty('Les leçons n’ont pas pu être chargées : ${s.error}');
  if(!s.hasData)return const Center(child:CircularProgressIndicator());
  final all=s.data!;
  final subjects=['Toutes',...(all.map((l)=>l['subject'] as String).toSet().toList()..sort((a,b)=>fold(a).compareTo(fold(b))))];
  final contextRows=all.where((l)=>(subject=='Toutes'||l['subject']==subject)&&(level=='Tous'||l['level']==level||l['level']=='Tous')).toList();
  final domains=['Tous les domaines',...contextRows.map((l)=>l['domain']?.toString()??'Repères et fondamentaux').toSet()];
  final tokens=fold(query.trim()).split(RegExp(r'\s+')).where((t)=>t.isNotEmpty).toList();
  final rows=contextRows.where((l){final studied=store.contains('completed',l['id']);return (domain=='Tous les domaines'||l['domain']==domain)&&(!favorites||store.contains('favorites',l['id']))&&(progress=='Tout'||(progress=='À étudier'&&!studied)||(progress=='Étudié'&&studied))&&tokens.every((t)=>fold('${l['title']} ${l['subject']} ${l['domain']} ${l['course']} ${l['example']}').contains(t));}).toList();
  final studied=contextRows.where((l)=>store.contains('completed',l['id'])).length;
  return refreshable(CustomScrollView(physics:const AlwaysScrollableScrollPhysics(),slivers:[
   SliverToBoxAdapter(child:Padding(padding:const EdgeInsets.all(16),child:Column(crossAxisAlignment:CrossAxisAlignment.start,children:[
    Text('Ma bibliothèque pédagogique',style:Theme.of(context).textTheme.headlineSmall),Text('${all.length} leçons · CI au CM2 · pédagogie'),const SizedBox(height:6),const Text('Comprendre la notion, essayer, vérifier et préparer sa séance. Contenus originaux à adapter au programme de l’établissement.'),
    const SizedBox(height:14),Wrap(spacing:8,runSpacing:8,children:[for(final levelName in levels)Builder(builder:(context){final group=all.where((l)=>l['level']==levelName).toList();final done=group.where((l)=>store.contains('completed',l['id'])).length;return SizedBox(width:100,child:Card(color:level==levelName?Theme.of(context).colorScheme.primaryContainer:null,child:InkWell(borderRadius:BorderRadius.circular(12),onTap:()=>setState((){level=levelName;subject='Toutes';domain='Tous les domaines';}),child:Padding(padding:const EdgeInsets.all(12),child:Column(children:[Text(levelName,style:const TextStyle(fontWeight:FontWeight.bold,fontSize:19)),Text('${group.length} leçons'),const SizedBox(height:7),LinearProgressIndicator(value:group.isEmpty?0:done/group.length),const SizedBox(height:4),Text('$done étudiées',style:Theme.of(context).textTheme.bodySmall)])))));})]),
    Wrap(spacing:6,children:[ActionChip(label:const Text('Tous les niveaux'),onPressed:()=>setState((){level='Tous';domain='Tous les domaines';})),ActionChip(label:const Text('Pédagogie'),avatar:const Icon(Icons.psychology_outlined),onPressed:()=>setState((){subject='Pédagogie';level='Tous';domain='Tous les domaines';}))]),
    const SizedBox(height:12),TextField(decoration:const InputDecoration(labelText:'Rechercher une notion ou une compétence',prefixIcon:Icon(Icons.search)),onChanged:(v)=>setState(()=>query=v)),const SizedBox(height:12),
    DropdownButtonFormField<String>(key:ValueKey('subject-$subject'),initialValue:subject,isExpanded:true,decoration:const InputDecoration(labelText:'Matière'),items:subjects.map((v)=>DropdownMenuItem(value:v,child:Text(v))).toList(),onChanged:(v)=>setState((){subject=v!;domain='Tous les domaines';})),
    const SizedBox(height:10),DropdownButtonFormField<String>(key:ValueKey('domain-$subject-$level-$domain'),initialValue:domains.contains(domain)?domain:'Tous les domaines',isExpanded:true,decoration:const InputDecoration(labelText:'Domaine / parcours'),items:domains.map((v)=>DropdownMenuItem(value:v,child:Text(v))).toList(),onChanged:(v)=>setState(()=>domain=v!)),
    const SizedBox(height:8),Wrap(spacing:6,children:['Tous',...levels].map((l)=>ChoiceChip(label:Text(l),selected:level==l,onSelected:(_)=>setState((){level=l;domain='Tous les domaines';}))).toList()),
    Wrap(spacing:6,children:[FilterChip(label:const Text('Favoris'),avatar:const Icon(Icons.bookmark_border),selected:favorites,onSelected:(v)=>setState(()=>favorites=v)),for(final p in ['Tout','À étudier','Étudié'])ChoiceChip(label:Text(p),selected:progress==p,onSelected:(_)=>setState(()=>progress=p))]),
    const SizedBox(height:8),Text('$studied / ${contextRows.length} étudiées dans cette sélection'),LinearProgressIndicator(value:contextRows.isEmpty?0:studied/contextRows.length),const SizedBox(height:12),Text('${rows.length} leçon(s) trouvée(s)',style:const TextStyle(fontWeight:FontWeight.bold)),
   ]))),
   if(rows.isEmpty)SliverToBoxAdapter(child:empty('Aucune leçon avec ces filtres. Changez la matière, le niveau ou les mots recherchés.')),
   SliverList.builder(itemCount:rows.length,itemBuilder:(context,i){final l=rows[i];final done=store.contains('completed',l['id']);final saved=store.contains('favorites',l['id']);
    final actions=<(String,IconData,VoidCallback)>[(saved?'Retirer des favoris':'Ajouter aux favoris',saved?Icons.bookmark:Icons.bookmark_border,()=>perform(context,()=>store.toggle('favorites',l['id']))),('Ouvrir la leçon',Icons.menu_book_outlined,()=>Navigator.push(context,MaterialPageRoute<void>(builder:(_)=>Lesson(lesson:l))))];
    return Padding(padding:const EdgeInsets.symmetric(horizontal:16),child:tile(l['title'],'${l['level']} · ${l['subject']}\n${l['domain']??'Repères et fondamentaux'}\n${l['objective']}',icon:done?Icons.check_circle:Icons.auto_stories_outlined,onTap:()=>Navigator.push(context,MaterialPageRoute<void>(builder:(_)=>Lesson(lesson:l))),onLongPress:()=>recordOptions(context,actions),trailing:Row(mainAxisSize:MainAxisSize.min,children:[IconButton(tooltip:saved?'Retirer des favoris':'Ajouter aux favoris',icon:Icon(saved?Icons.bookmark:Icons.bookmark_border),onPressed:()=>perform(context,()=>store.toggle('favorites',l['id']))),optionsButton(actions)])));
   }),
   SliverToBoxAdapter(child:Padding(padding:const EdgeInsets.all(16),child:Column(crossAxisAlignment:CrossAxisAlignment.start,children:[const Text('L’arabe et l’éducation religieuse sont à utiliser selon la filière et le cadre de l’établissement. Les domaines ont été repérés notamment sur PROMET ; ces leçons sont rédigées pour Enseignant.'),TextButton.icon(onPressed:()=>perform(context,()=>bridge.invokeMethod<void>('openUrl','https://apprendre.education.sn/')),icon:const Icon(Icons.open_in_new),label:const Text('Consulter PROMET'))]))),
  ]));
 });
}
class Lesson extends StatefulWidget {
 final Map<String,dynamic> lesson; const Lesson({super.key,required this.lesson});
 @override State<Lesson> createState()=>_LessonState();
}
class _LessonState extends State<Lesson> {
 bool answer=false;
 @override Widget build(BuildContext context)=>ListenableBuilder(listenable:store,builder:(context,_){final l=widget.lesson;return Scaffold(appBar:AppBar(title:Text(l['title']),actions:[IconButton(tooltip:'Favori',icon:Icon(store.contains('favorites',l['id'])?Icons.bookmark:Icons.bookmark_border),onPressed:()=>perform(context,()=>store.toggle('favorites',l['id'])))]),body:ListView(padding:const EdgeInsets.all(20),children:[
  Text('${l['subject']} · ${l['level']} · ${l['duration']}',style:Theme.of(context).textTheme.labelLarge),if(l['domain']!=null)Text(l['domain'],style:Theme.of(context).textTheme.labelMedium),section('Objectif'),SelectableText(l['objective']),section('Comprendre la notion'),SelectableText(l['course']),section('Exemple expliqué'),SelectableText(l['example']),section('En classe'),SelectableText(l['activity']),section('Point de vigilance'),SelectableText(l['trap']),section('Je vérifie ma compréhension'),SelectableText(l['question']),const SizedBox(height:10),OutlinedButton(onPressed:()=>setState(()=>answer=!answer),child:Text(answer?'Masquer la correction':'Voir la correction')),if(answer)Card(child:Padding(padding:const EdgeInsets.all(16),child:SelectableText(l['answer']))),
  CheckboxListTile(contentPadding:EdgeInsets.zero,title:const Text('Fiche étudiée'),subtitle:const Text('Suivi personnel, sans certification de maîtrise'),value:store.contains('completed',l['id']),onChanged:(_)=>perform(context,()=>store.toggle('completed',l['id']))),
  FilledButton.icon(icon:const Icon(Icons.edit_note),label:const Text('Copier dans mes préparations'),onPressed:()=>perform(context,() async {await store.put('notes',{'id':uid(),'title':l['title'],'kind':'Préparation','level':l['level']=='Tous'?'CI':l['level'],'subject':l['subject'],'objective':l['objective'],'body':'Notion :\n${l['course']}\n\nExemple :\n${l['example']}\n\nActivité :\n${l['activity']}\n\nVigilance :\n${l['trap']}','assessment':'${l['question']}\nCorrection : ${l['answer']}','updated':DateTime.now().toIso8601String(),'pinned':false});if(context.mounted)message(context,'Préparation créée dans le Carnet. Vous pouvez l’adapter.');})),
  const SizedBox(height:20),Text(l['origin'],style:Theme.of(context).textTheme.bodySmall),
 ]));});
}

List<Map<String,dynamic>> decodeIndex(String raw) => (jsonDecode(raw) as List).map((v)=>{'page':v['page'],'text':v['text'],'normalized':fold(v['text'] as String)}).toList();
class Grevisse extends StatefulWidget { const Grevisse({super.key}); @override State<Grevisse> createState()=>_GrevisseState(); }
class _GrevisseState extends State<Grevisse> {
 List<Map<String,dynamic>> pages=[],chapters=[]; String query='',draft='',group='Toutes les parties',error='';
 bool exact=false,bookmarks=false;Timer? debounce;
 @override void initState(){super.initState();unawaited(load());}
 Future<void> load() async {
  try{final data=await Future.wait([rootBundle.loadString('assets/grevisse/index.json'),rootBundle.loadString('assets/grevisse/chapters.json')]);
   final index=await compute(decodeIndex,data[0]);final toc=(jsonDecode(data[1]) as List).map((v)=>Map<String,dynamic>.from(v as Map)).toList();
   if(mounted)setState((){pages=index;chapters=toc;error='';});
  }catch(e){if(mounted)setState(()=>error='$e');}
 }
 @override void dispose(){debounce?.cancel();super.dispose();}
 Map<String,dynamic>? chapterFor(int page)=>chapters.where((c)=>page>=c['page']&&page<=c['end']).lastOrNull;
 void open(int page)=>Navigator.push(context,MaterialPageRoute<void>(builder:(_)=>BookReader(initialPage:page,pages:pages,chapters:chapters)));
 String snippet(Map<String,dynamic> p) {
  final text=(p['text'] as String).replaceAll(RegExp(r'\s+'),' ');final normalized=fold(text);
  final token=fold(query).split(RegExp(r'\s+')).firstWhere((v)=>v.isNotEmpty,orElse:()=>'');
  final pos=normalized.indexOf(token);final start=pos>65?pos-65:0;final end=(start+230)<text.length?start+230:text.length;
  return '${start>0?'… ':''}${text.substring(start<text.length?start:text.length,end)}${end<text.length?' …':''}';
 }
 @override Widget build(BuildContext context){
  if(error.isNotEmpty)return Center(child:Column(mainAxisSize:MainAxisSize.min,children:[Text('Livre indisponible : $error'),TextButton(onPressed:load,child:const Text('Réessayer'))]));
  if(pages.isEmpty)return const Center(child:CircularProgressIndicator());
  final tokens=fold(query.trim()).split(RegExp(r'\s+')).where((v)=>v.isNotEmpty).toList();
  final matchingChapters=chapters.where((c)=>(group=='Toutes les parties'||c['group']==group)&&tokens.every((t)=>fold(c['title']).contains(t))).toList();
  final filtered=pages.where((p){final c=chapterFor(p['page']);if(group!='Toutes les parties'&&c?['group']!=group)return false;if(bookmarks&&!store.contains('bookmarks','${p['page']}'))return false;if(tokens.isEmpty)return true;return exact?(p['normalized'] as String).contains(fold(query.trim())):tokens.every((t)=>(p['normalized'] as String).contains(t));}).toList();
  final searching=tokens.isNotEmpty||bookmarks;
  return refreshable(CustomScrollView(physics:const AlwaysScrollableScrollPhysics(),slivers:[SliverToBoxAdapter(child:Padding(padding:const EdgeInsets.all(16),child:Column(crossAxisAlignment:CrossAxisAlignment.start,children:[
   Text('Le Grevisse de l’enseignant',style:Theme.of(context).textTheme.headlineSmall),Text('${pages.length} pages · ${chapters.length} repères classés · hors connexion'),const Text('Pellat & Fonvielle · Magnard · copie fournie. Recherche OCR indicative : vérifier la page scannée, notamment les tableaux.'),const SizedBox(height:12),
   TextField(decoration:const InputDecoration(labelText:'Rechercher dans le livre',hintText:'Ex. participe passé',prefixIcon:Icon(Icons.search)),onChanged:(v){draft=v;debounce?.cancel();debounce=Timer(const Duration(milliseconds:300),(){if(mounted)setState(()=>query=draft);});}),const SizedBox(height:10),
   DropdownButtonFormField<String>(initialValue:group,isExpanded:true,decoration:const InputDecoration(labelText:'Partie du livre'),items:['Toutes les parties',...chapters.map((c)=>c['group'] as String).toSet()].map((v)=>DropdownMenuItem(value:v,child:Text(v))).toList(),onChanged:(v)=>setState(()=>group=v!)),
   Wrap(spacing:8,children:[FilterChip(label:const Text('Expression exacte'),selected:exact,onSelected:(v)=>setState(()=>exact=v)),FilterChip(label:const Text('Signets'),selected:bookmarks,onSelected:(v)=>setState(()=>bookmarks=v))]),
   const Text('Recherche sans distinction de casse ni d’accents. Par défaut, tous les mots saisis doivent figurer sur une même page.'),
   Wrap(spacing:8,children:[OutlinedButton.icon(icon:const Icon(Icons.chrome_reader_mode),label:const Text('Ouvrir le livre'),onPressed:()=>open(1)),TextButton(onPressed:()=>open(4),child:const Text('Sommaire original'))]),
   if(searching)Text('${filtered.length} page(s) correspondante(s)'),
   if(query.trim().isNotEmpty&&matchingChapters.isNotEmpty&&!bookmarks)...[section('Notions du sommaire'),for(final c in matchingChapters)tile(c['title'],'${c['group']} · p. ${c['printed']}',onTap:()=>open(c['page']))],
  ]))),
  if(!searching)SliverList(delegate:SliverChildListDelegate([
   for(final g in chapters.map((c)=>c['group'] as String).toSet())if(group=='Toutes les parties'||g==group)Padding(padding:const EdgeInsets.symmetric(horizontal:16),child:Card(child:ExpansionTile(title:Text(g),children:[for(final c in chapters.where((v)=>v['group']==g))Builder(builder:(itemContext){
    final actions=< (String,IconData,VoidCallback)>[('Marquer / démarquer',Icons.bookmark_border,()=>perform(itemContext,()=>store.toggle('bookmarks','${c['page']}'))),('Ouvrir la page',Icons.menu_book_outlined,()=>open(c['page']))];
    return ListTile(title:Text(c['title']),subtitle:Text('p. ${c['printed']}'),trailing:optionsButton(actions),onTap:()=>open(c['page']),onLongPress:()=>recordOptions(itemContext,actions));
   })]))),
  ])),
  if(searching&&filtered.isEmpty)SliverToBoxAdapter(child:empty('Aucune page trouvée. Essayez un mot plus court ou consultez le sommaire : l’OCR peut manquer certains mots.')),
  if(searching)SliverList.builder(itemCount:filtered.length,itemBuilder:(context,i){final p=filtered[i],c=chapterFor(p['page']);return Padding(padding:const EdgeInsets.symmetric(horizontal:16),child:Builder(builder:(itemContext){
    final actions=< (String,IconData,VoidCallback)>[('Marquer / démarquer',Icons.bookmark_border,()=>perform(itemContext,()=>store.toggle('bookmarks','${p['page']}'))),('Ouvrir la page',Icons.menu_book_outlined,()=>open(p['page']))];
    return tile('${c?['title']??'Couverture et sommaire'} · page PDF ${p['page']}',snippet(p),icon:Icons.find_in_page_outlined,onTap:()=>open(p['page']),onLongPress:()=>recordOptions(itemContext,actions),trailing:Row(mainAxisSize:MainAxisSize.min,children:[IconButton(tooltip:'Signet',icon:Icon(store.contains('bookmarks','${p['page']}')?Icons.bookmark:Icons.bookmark_border),onPressed:()=>perform(itemContext,()=>store.toggle('bookmarks','${p['page']}'))),optionsButton(actions)]));
   }));}),
  const SliverToBoxAdapter(child:SizedBox(height:24)),
 ]));
 }
}
class PageJumpDialog extends StatefulWidget {
 final int initialPage, totalPages;
 final String explanation;
 const PageJumpDialog({super.key,required this.initialPage,required this.totalPages,this.explanation='Page imprimée = page PDF − 2'});
 @override State<PageJumpDialog> createState()=>_PageJumpDialogState();
}
class _PageJumpDialogState extends State<PageJumpDialog> {
 late final TextEditingController controller=TextEditingController(text:'${widget.initialPage}');
 @override void dispose(){controller.dispose();super.dispose();}
 @override Widget build(BuildContext context)=>AlertDialog(title:const Text('Atteindre une page PDF'),content:TextField(controller:controller,autofocus:true,keyboardType:TextInputType.number,decoration:InputDecoration(labelText:'1 à ${widget.totalPages}',helperText:widget.explanation)),actions:[TextButton(onPressed:()=>Navigator.pop(context),child:const Text('Annuler')),FilledButton(onPressed:(){final n=int.tryParse(controller.text.trim());if(n!=null&&n>=1&&n<=widget.totalPages)Navigator.pop(context,n);},child:const Text('Ouvrir'))]);
}
class BookReader extends StatefulWidget {
 final int initialPage;final List<Map<String,dynamic>> pages,chapters;
 const BookReader({super.key,required this.initialPage,required this.pages,required this.chapters});
 @override State<BookReader> createState()=>_BookReaderState();
}
class _BookReaderState extends State<BookReader> {
 late int page=widget.initialPage;bool text=false;int turns=0;
 late final PageController controller=PageController(initialPage:widget.initialPage-1);
 @override void dispose(){controller.dispose();super.dispose();}
 void go(int n){if(n>=1&&n<=widget.pages.length){controller.jumpToPage(n-1);setState((){page=n;turns=0;});}}
 Future<void> jump() async {
  final n=await showDialog<int>(context:context,builder:(_)=>PageJumpDialog(initialPage:page,totalPages:widget.pages.length));
  if(mounted&&n!=null)go(n);
 }
 @override Widget build(BuildContext context)=>ListenableBuilder(listenable:store,builder:(context,_){
  final chapter=widget.chapters.where((c)=>page>=c['page']&&page<=c['end']).lastOrNull;
  return Scaffold(appBar:AppBar(title:Text('Page $page / ${widget.pages.length}'),actions:[IconButton(tooltip:'Page précise',onPressed:jump,icon:const Icon(Icons.numbers)),IconButton(tooltip:'Signet',onPressed:()=>perform(context,()=>store.toggle('bookmarks','$page')),icon:Icon(store.contains('bookmarks','$page')?Icons.bookmark:Icons.bookmark_border)),PopupMenuButton<String>(onSelected:(v){if(v=='text'){setState(()=>text=!text);}else{setState(()=>turns=(turns+1)%4);}},itemBuilder:(_)=>[PopupMenuItem(value:'text',child:Text(text?'Voir la page scannée':'Lire le texte OCR')),const PopupMenuItem(value:'rotate',child:Text('Tourner de 90°'))])]),
   body:SafeArea(child:Column(children:[Padding(padding:const EdgeInsets.symmetric(horizontal:12,vertical:6),child:Text(chapter==null?'Couverture et sommaire':'${chapter['group']} · ${chapter['title']} · p. imprimée ${page-2}',maxLines:2,overflow:TextOverflow.ellipsis)),
    Expanded(child:PageView.builder(controller:controller,itemCount:widget.pages.length,onPageChanged:(i)=>setState((){page=i+1;turns=0;}),itemBuilder:(context,i){final n=i+1;
     if(text)return SingleChildScrollView(key:ValueKey('ocr-$n'),padding:const EdgeInsets.all(20),child:Column(crossAxisAlignment:CrossAxisAlignment.start,children:[const Text('OCR automatique, non corrigé. Se référer à la page scannée en cas de doute.',style:TextStyle(fontStyle:FontStyle.italic)),const SizedBox(height:16),SelectableText(widget.pages[i]['text'],style:const TextStyle(fontSize:18,height:1.6))]));
     return ZoomablePage(key:ValueKey('image-$n-$turns'),page:n,turns:i==page-1?turns:0);
    })),
    Row(mainAxisAlignment:MainAxisAlignment.spaceEvenly,children:[IconButton(tooltip:'Page précédente',onPressed:page>1?()=>go(page-1):null,icon:const Icon(Icons.chevron_left)),TextButton(onPressed:jump,child:Text('$page / ${widget.pages.length}')),IconButton(tooltip:'Page suivante',onPressed:page<widget.pages.length?()=>go(page+1):null,icon:const Icon(Icons.chevron_right))]),
   ])),
  );
 });
}
class ZoomablePage extends StatefulWidget {
 final int page,turns;
 const ZoomablePage({super.key,required this.page,required this.turns});
 @override State<ZoomablePage> createState()=>_ZoomablePageState();
}
class _ZoomablePageState extends State<ZoomablePage> {
 final transform=TransformationController();
 bool zoomed=false;
 @override void initState(){super.initState();transform.addListener(_updateZoom);}
 void _updateZoom(){final next=transform.value.getMaxScaleOnAxis()>1.01;if(next!=zoomed&&mounted)setState(()=>zoomed=next);}
 @override void dispose(){transform.removeListener(_updateZoom);transform.dispose();super.dispose();}
 @override Widget build(BuildContext context)=>InteractiveViewer(
  transformationController:transform,panEnabled:zoomed,minScale:1,maxScale:6,
  child:Center(child:RotatedBox(quarterTurns:widget.turns,child:Image.asset('assets/grevisse/pages/${widget.page.toString().padLeft(3,'0')}.jpg',fit:BoxFit.contain,errorBuilder:(_,e,stack)=>Text('Page indisponible : $e')))),
 );
}
