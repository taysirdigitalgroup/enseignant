import 'dart:convert';
import 'dart:math' as math;
import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'core.dart' show bridge;
import 'main.dart' show store, perform, message, detail, section, empty, recordOptions, optionsButton;

void referenceImageCredits(BuildContext context,ReferencePack pack)=>detail(context,'Crédits des illustrations',[
 for(final dynamic image in pack.images.values)ListTile(contentPadding:EdgeInsets.zero,title:Text(image['title']),subtitle:Text('${image['author']} · ${image['licence']}\n${image['changes']}'),trailing:const Icon(Icons.open_in_new),onTap:()=>referenceUrl(context,image['source'])),
]);
String referenceKey(String id)=>'reference:$id';
String referenceNormalize(String value) {
 const accents='àáâãäåçèéêëìíîïñòóôõöùúûüýÿ';
 const plain='aaaaaaceeeeiiiinooooouuuuyy';
 var text=value.toLowerCase().replaceAll('œ','oe').replaceAll('æ','ae').replaceAll('’',"'");
 for(var i=0;i<accents.length;i++){text=text.replaceAll(accents[i],plain[i]);}
 return text.replaceAll(RegExp(r'[\u0300-\u036f]'),'').replaceAll(RegExp(r'\s+'),' ').trim();
}
class ReferencePack {
 final Map<String,dynamic> data;
 late final List<Map<String,dynamic>> articles=(data['articles'] as List).map((e)=>Map<String,dynamic>.from(e as Map)).toList();
 late final Map<String,Map<String,dynamic>> byId={for(final a in articles)a['id'] as String:a};
 late final Map<String,String> searchIndex={for(final a in articles)a['id'] as String:referenceNormalize([
  jsonEncode(a),
  for(final dynamic term in (data['glossary'] as List? ?? []))if(term['article']==a['id'])'${term['term']} ${term['definition']}',
  for(final dynamic event in (data['timeline'] as List? ?? []))if(event['article']==a['id'])'${event['date']} ${event['text']}',
 ].join(' '))};
 late final Map<String,dynamic> sources=Map<String,dynamic>.from(data['sources'] as Map);
 late final Map<String,dynamic> images=Map<String,dynamic>.from(data['images'] as Map);
 ReferencePack(this.data);
 List<Map<String,dynamic>> find({String query='',String subject='',String group='',bool favorites=false}) {
  final terms=referenceNormalize(query).split(' ').where((e)=>e.isNotEmpty).toList();
  return articles.where((a)=>(subject.isEmpty||a['subject']==subject)&&(group.isEmpty||a['group']==group)&&(!favorites||store.contains('favorites',referenceKey(a['id'])))&&terms.every((t)=>searchIndex[a['id']]!.contains(t))).toList();
 }
}
class ReferenceRepository {
 const ReferenceRepository();
 Future<ReferencePack> load() async =>ReferencePack(Map<String,dynamic>.from(jsonDecode(await rootBundle.loadString('assets/documentation/senegal.json')) as Map));
}
Future<void> referenceUrl(BuildContext context,String url) async {
 try {await bridge.invokeMethod<void>('openUrl',url);}
 catch(error){if(context.mounted)message(context,'Impossible d’ouvrir la référence : $error');}
}
void referenceSources(BuildContext context,ReferencePack pack,List<dynamic> ids)=>detail(context,'Sources et repères de vérification',[
 const Text('Les textes sont des synthèses pédagogiques. Les liens donnent accès aux références consultées. Leur ouverture nécessite Internet.'),
 for(final id in ids)if(pack.sources[id]!=null)Padding(padding:const EdgeInsets.only(top:16),child:Column(crossAxisAlignment:CrossAxisAlignment.start,children:[Text(pack.sources[id]['title'],style:const TextStyle(fontWeight:FontWeight.bold)),Text('${pack.sources[id]['publisher']} · ${pack.sources[id]['date']}'),Text(pack.sources[id]['note']),TextButton.icon(onPressed:()=>referenceUrl(context,pack.sources[id]['url']),icon:const Icon(Icons.open_in_new),label:const Text('Consulter la référence'))])),
]);

class DocumentationScreen extends StatefulWidget {
 final ReferenceRepository repository;
 const DocumentationScreen({super.key,this.repository=const ReferenceRepository()});
 @override State<DocumentationScreen> createState()=>_DocumentationScreenState();
}
class _DocumentationScreenState extends State<DocumentationScreen> {
 late Future<ReferencePack> loading;
 @override void initState(){super.initState();loading=widget.repository.load();}
 @override Widget build(BuildContext context)=>Scaffold(appBar:AppBar(title:const Text('Documentation & Référence',overflow:TextOverflow.ellipsis)),body:FutureBuilder<ReferencePack>(future:loading,builder:(context,s){
  if(s.hasError)return Center(child:Column(mainAxisSize:MainAxisSize.min,children:[const Text('La documentation ne peut pas être chargée.'),TextButton(onPressed:()=>setState(()=>loading=widget.repository.load()),child:const Text('Réessayer'))]));
  if(!s.hasData)return const Center(child:CircularProgressIndicator());
  return ReferenceLibrary(pack:s.data!,onRefresh:() async {await store.reload();if(mounted)setState(()=>loading=widget.repository.load());});
 }));
}
class ReferenceLibrary extends StatefulWidget {
 final ReferencePack pack;final Future<void> Function() onRefresh;
 const ReferenceLibrary({super.key,required this.pack,required this.onRefresh});
 @override State<ReferenceLibrary> createState()=>_ReferenceLibraryState();
}
class _ReferenceLibraryState extends State<ReferenceLibrary> {
 final search=TextEditingController();bool favorites=false;
 @override void dispose(){search.dispose();super.dispose();}
 @override Widget build(BuildContext context)=>ListenableBuilder(listenable:store,builder:(context,_){
  final pack=widget.pack;final results=pack.find(query:search.text,favorites:favorites);final searching=search.text.trim().isNotEmpty||favorites;
  return RefreshIndicator(onRefresh:widget.onRefresh,child:ListView(padding:const EdgeInsets.all(16),physics:const AlwaysScrollableScrollPhysics(),children:[
   Text('Comprendre le Sénégal',style:Theme.of(context).textTheme.headlineMedium),const SizedBox(height:8),Text('${pack.articles.length} fiches · 14 régions · textes, repères et images hors connexion'),
   Text('Édition du ${pack.data['displayDate']} · pour apprendre et préparer ses cours'),const SizedBox(height:16),
   TextField(controller:search,onChanged:(_)=>setState((){}),decoration:InputDecoration(labelText:'Rechercher dans toute la documentation',hintText:'Ex. mangrove, indépendance, Kédougou…',prefixIcon:const Icon(Icons.search),suffixIcon:IconButton(tooltip:'Effacer',icon:const Icon(Icons.clear),onPressed:(){search.clear();setState((){});}))),
   Wrap(spacing:8,children:[FilterChip(label:const Text('Mes favoris'),avatar:Icon(favorites?Icons.bookmark:Icons.bookmark_border,size:18),selected:favorites,onSelected:(v)=>setState(()=>favorites=v)),ActionChip(label:const Text('Sources et méthode'),avatar:const Icon(Icons.info_outline,size:18),onPressed:()=>detail(context,'Le fonds documentaire',[
    Text(pack.data['scope']),section('Méthode et limites'),Text(pack.data['method']),section('Photographies et carte'),const Text('Les crédits et licences sont accessibles sous chaque illustration. Les limites cartographiques simplifiées représentent les régions de 2019 et servent au repérage pédagogique.'),TextButton(onPressed:()=>referenceImageCredits(context,pack),child:const Text('Crédits de toutes les illustrations')),section('Adapter à la classe'),const Text('CI–CP : nommer et repérer à partir d’images. CE1–CE2 : décrire et ordonner des repères. CM1–CM2 : comparer des documents et justifier. Ce sont des pistes à adapter au programme et au niveau réel des élèves.'),TextButton(onPressed:()=>referenceSources(context,pack,pack.sources.keys.toList()),child:const Text('Toutes les références')),
   ]))]),
   if(searching)...[section('${results.length} fiche(s) trouvée(s)'),if(results.isEmpty)empty('Aucune fiche pour cette recherche.'),for(final a in results)ReferenceArticleTile(pack:pack,article:a)]else...[
    for(final dynamic subject in pack.data['subjects'] as List)Padding(padding:const EdgeInsets.only(top:12),child:Card(clipBehavior:Clip.antiAlias,child:InkWell(onTap:()=>Navigator.push(context,MaterialPageRoute<void>(builder:(_)=>ReferenceSubjectScreen(pack:pack,subject:subject))),child:Column(crossAxisAlignment:CrossAxisAlignment.start,children:[
     if(pack.images[subject['image']]!=null)Image.asset(pack.images[subject['image']]['asset'],height:145,width:double.infinity,fit:BoxFit.cover,excludeFromSemantics:true),
     Padding(padding:const EdgeInsets.all(18),child:Column(crossAxisAlignment:CrossAxisAlignment.start,children:[Row(children:[Icon(subject['id']=='geo'?Icons.public:Icons.history_edu,size:30),const SizedBox(width:10),Expanded(child:Text(subject['title'],style:Theme.of(context).textTheme.titleLarge)),const Icon(Icons.arrow_forward)]),const SizedBox(height:8),Text(subject['description']),Text('${pack.find(subject:subject['id']).length} fiches',style:Theme.of(context).textTheme.labelLarge)])),
    ])))),
    section('Accès directs'),Wrap(spacing:8,runSpacing:8,children:[FilledButton.tonalIcon(onPressed:()=>openReferenceMap(context,pack),icon:const Icon(Icons.map_outlined),label:const Text('Carte des régions')),FilledButton.tonalIcon(onPressed:()=>openReferenceTimeline(context,pack),icon:const Icon(Icons.timeline),label:const Text('Chronologie')),FilledButton.tonalIcon(onPressed:()=>openReferenceGlossary(context,pack),icon:const Icon(Icons.abc),label:const Text('Vocabulaire'))]),
    section('Reprendre une lecture'),for(final a in pack.articles.where((a)=>store.contains('completed',referenceKey(a['id']))).take(3))ReferenceArticleTile(pack:pack,article:a),
    const Text('Une synthèse nationale étendue, à compléter par les réalités locales, les manuels et le programme de la classe.'),
   ],const SizedBox(height:24),
  ]));
 });
}
class ReferenceSubjectScreen extends StatefulWidget {
 final ReferencePack pack;final Map<String,dynamic> subject;
 const ReferenceSubjectScreen({super.key,required this.pack,required this.subject});
 @override State<ReferenceSubjectScreen> createState()=>_ReferenceSubjectScreenState();
}
class _ReferenceSubjectScreenState extends State<ReferenceSubjectScreen> {
 final search=TextEditingController();String group='';bool favorites=false;
 @override void dispose(){search.dispose();super.dispose();}
 @override Widget build(BuildContext context)=>ListenableBuilder(listenable:store,builder:(context,_){
  final pack=widget.pack;final id=widget.subject['id'] as String;final articles=pack.find(subject:id,query:search.text,group:group,favorites:favorites);final all=pack.find(subject:id);
  final groups=all.map((a)=>a['group'] as String).toSet().toList();final read=all.where((a)=>store.contains('completed',referenceKey(a['id']))).length;
  return Scaffold(appBar:AppBar(title:Text(widget.subject['title'],overflow:TextOverflow.ellipsis),actions:[IconButton(tooltip:id=='geo'?'Carte des régions':'Chronologie',icon:Icon(id=='geo'?Icons.map_outlined:Icons.timeline),onPressed:()=>id=='geo'?openReferenceMap(context,pack):openReferenceTimeline(context,pack))]),body:RefreshIndicator(onRefresh:() async {await store.reload();if(mounted)setState((){});},child:ListView(padding:const EdgeInsets.all(16),physics:const AlwaysScrollableScrollPhysics(),children:[
   Text(widget.subject['description']),const SizedBox(height:12),Text('$read / ${all.length} fiches marquées comme lues'),LinearProgressIndicator(value:all.isEmpty?0:read/all.length),const SizedBox(height:16),
   TextField(controller:search,onChanged:(_)=>setState((){}),decoration:InputDecoration(labelText:'Rechercher dans cette section',prefixIcon:const Icon(Icons.search),suffixIcon:IconButton(tooltip:'Effacer',icon:const Icon(Icons.clear),onPressed:(){search.clear();setState((){});}))),
   const SizedBox(height:12),DropdownButtonFormField<String>(key:ValueKey(group),initialValue:group,isExpanded:true,decoration:const InputDecoration(labelText:'Dossier'),items:[const DropdownMenuItem(value:'',child:Text('Tous les dossiers')),for(final g in groups)DropdownMenuItem(value:g,child:Text(g,overflow:TextOverflow.ellipsis))],onChanged:(v)=>setState(()=>group=v??'')),
   Align(alignment:Alignment.centerLeft,child:FilterChip(label:const Text('Favoris'),selected:favorites,avatar:Icon(favorites?Icons.bookmark:Icons.bookmark_border,size:18),onSelected:(v)=>setState(()=>favorites=v))),
   Text('${articles.length} résultat(s)'),if(articles.isEmpty)empty('Aucune fiche pour ces filtres.'),for(final a in articles)ReferenceArticleTile(pack:pack,article:a),const SizedBox(height:24),
  ])));
 });
}
void openReferenceArticle(BuildContext context,ReferencePack pack,String id,{bool replace=false}) {
 final article=pack.byId[id];if(article==null)return;
 final route=MaterialPageRoute<void>(builder:(_)=>ReferenceArticleScreen(pack:pack,article:article));
 if(replace){Navigator.pushReplacement(context,route);}else{Navigator.push(context,route);}
}
class ReferenceArticleTile extends StatelessWidget {
 final ReferencePack pack;final Map<String,dynamic> article;
 const ReferenceArticleTile({super.key,required this.pack,required this.article});
 @override Widget build(BuildContext context) {
  final key=referenceKey(article['id']);final saved=store.contains('favorites',key);final read=store.contains('completed',key);
  final actions=<(String,IconData,VoidCallback)>[
   ('Lire la fiche',Icons.menu_book_outlined,()=>openReferenceArticle(context,pack,article['id'])),
   (saved?'Retirer des favoris':'Ajouter aux favoris',saved?Icons.bookmark:Icons.bookmark_border,()=>perform(context,()=>store.toggle('favorites',key))),
   (read?'Marquer comme non lue':'Marquer comme lue',read?Icons.check_circle:Icons.check_circle_outline,()=>perform(context,()=>store.toggle('completed',key))),
  ];
  return Card(child:ListTile(contentPadding:const EdgeInsets.symmetric(horizontal:14,vertical:8),leading:Icon(read?Icons.check_circle_outline:article['subject']=='geo'?Icons.public:Icons.history_edu,color:read?Colors.green:null),title:Text(article['title'],style:const TextStyle(fontWeight:FontWeight.w700)),subtitle:Text('${article['group']} · ${article['minutes']} min\n${article['summary']}',maxLines:4,overflow:TextOverflow.ellipsis),onTap:actions.first.$3,onLongPress:()=>recordOptions(context,actions),trailing:Row(mainAxisSize:MainAxisSize.min,children:[IconButton(tooltip:saved?'Retirer des favoris':'Ajouter aux favoris',icon:Icon(saved?Icons.bookmark:Icons.bookmark_border),onPressed:actions[1].$3),optionsButton(actions)])));
 }
}
class ReferenceArticleScreen extends StatelessWidget {
 final ReferencePack pack;final Map<String,dynamic> article;
 const ReferenceArticleScreen({super.key,required this.pack,required this.article});
 @override Widget build(BuildContext context)=>ListenableBuilder(listenable:store,builder:(context,_){
  final key=referenceKey(article['id']);final saved=store.contains('favorites',key);final read=store.contains('completed',key);final siblings=pack.find(subject:article['subject']);final index=siblings.indexWhere((a)=>a['id']==article['id']);
  final citation='Enseignant · TDG, Documentation & Référence, « ${article['title']} », édition du ${pack.data['displayDate']}. Sources : ${(article['sources'] as List).map((id)=>pack.sources[id]['url']).join(' ; ')}';
  return Scaffold(appBar:AppBar(title:Text(article['title'],overflow:TextOverflow.ellipsis),actions:[IconButton(tooltip:saved?'Retirer des favoris':'Ajouter aux favoris',icon:Icon(saved?Icons.bookmark:Icons.bookmark_border),onPressed:()=>perform(context,()=>store.toggle('favorites',key))),IconButton(tooltip:'Sources de cette fiche',icon:const Icon(Icons.info_outline),onPressed:()=>referenceSources(context,pack,article['sources']))]),body:RefreshIndicator(onRefresh:store.reload,child:ListView(padding:const EdgeInsets.all(20),physics:const AlwaysScrollableScrollPhysics(),children:[
   Text(article['group'],style:Theme.of(context).textTheme.labelLarge),Text(article['title'],style:Theme.of(context).textTheme.headlineMedium),const SizedBox(height:8),Text(article['summary'],style:Theme.of(context).textTheme.titleMedium),Wrap(spacing:8,children:[Chip(label:Text('${article['minutes']} min')),const Chip(label:Text('Référence enseignant'))]),
   section('Objectifs'),for(final dynamic objective in article['objectives'] as List)Padding(padding:const EdgeInsets.only(bottom:6),child:Text('• $objective')),
   for(final dynamic block in article['blocks'] as List)ReferenceBlock(pack:pack,block:Map<String,dynamic>.from(block as Map)),
   section('À retenir'),Container(padding:const EdgeInsets.all(16),decoration:BoxDecoration(color:Theme.of(context).colorScheme.primaryContainer,borderRadius:BorderRadius.circular(16)),child:Column(crossAxisAlignment:CrossAxisAlignment.start,children:[for(final dynamic fact in article['takeaways'] as List)Padding(padding:const EdgeInsets.only(bottom:8),child:Text('• $fact'))])),
   section('Préparer une activité'),SelectableText(article['activity']['task'],style:Theme.of(context).textTheme.bodyLarge),ExpansionTile(tilePadding:EdgeInsets.zero,title:const Text('Piste de correction / conduite de classe'),children:[Padding(padding:const EdgeInsets.all(12),child:SelectableText(article['activity']['answer']))]),
   if((article['questions'] as List).isNotEmpty)...[section('Vérifier sa compréhension'),for(final dynamic question in article['questions'] as List)ExpansionTile(tilePadding:EdgeInsets.zero,title:Text(question['q']),children:[Padding(padding:const EdgeInsets.all(12),child:SelectableText(question['a']))])],
   if((article['related'] as List).isNotEmpty)...[section('Poursuivre la lecture'),for(final dynamic id in article['related'] as List)if(pack.byId[id]!=null)ListTile(contentPadding:EdgeInsets.zero,leading:const Icon(Icons.link),title:Text(pack.byId[id]!['title']),trailing:const Icon(Icons.chevron_right),onTap:()=>openReferenceArticle(context,pack,id))],
   section('Références'),for(final dynamic id in article['sources'] as List)ListTile(contentPadding:EdgeInsets.zero,title:Text(pack.sources[id]['title']),subtitle:Text(pack.sources[id]['publisher']),trailing:const Icon(Icons.open_in_new),onTap:()=>referenceUrl(context,pack.sources[id]['url'])),
   TextButton.icon(onPressed:() async {await Clipboard.setData(ClipboardData(text:citation));if(context.mounted)message(context,'Référence copiée.');},icon:const Icon(Icons.copy),label:const Text('Copier la référence')),
   FilledButton.tonalIcon(onPressed:()=>perform(context,()=>store.toggle('completed',key)),icon:Icon(read?Icons.check_circle:Icons.check_circle_outline),label:Text(read?'Fiche lue · marquer comme non lue':'Marquer cette fiche comme lue')),
   const SizedBox(height:16),Row(children:[Expanded(child:OutlinedButton.icon(onPressed:index>0?()=>openReferenceArticle(context,pack,siblings[index-1]['id'],replace:true):null,icon:const Icon(Icons.chevron_left),label:const Text('Précédente'))),const SizedBox(width:8),Expanded(child:OutlinedButton.icon(onPressed:index<siblings.length-1?()=>openReferenceArticle(context,pack,siblings[index+1]['id'],replace:true):null,icon:const Icon(Icons.chevron_right),label:const Text('Suivante')))]),const SizedBox(height:24),
  ])));
 });
}
class ReferenceBlock extends StatelessWidget {
 final ReferencePack pack;final Map<String,dynamic> block;
 const ReferenceBlock({super.key,required this.pack,required this.block});
 @override Widget build(BuildContext context) {
  switch(block['type']) {
   case 'h2':return section(block['text']);
   case 'image':return ReferenceFigure(pack:pack,id:block['image'],caption:block['caption']);
   case 'bullets':return Padding(padding:const EdgeInsets.only(bottom:12),child:Column(crossAxisAlignment:CrossAxisAlignment.start,children:[for(final dynamic text in block['items'] as List)Padding(padding:const EdgeInsets.only(bottom:8),child:SelectableText('• $text'))]));
   case 'table':return Padding(padding:const EdgeInsets.only(bottom:16),child:SingleChildScrollView(scrollDirection:Axis.horizontal,child:DataTable(columns:[for(final dynamic title in block['headers'] as List)DataColumn(label:Text(title))],rows:[for(final dynamic row in block['rows'] as List)DataRow(cells:[for(final dynamic value in row as List)DataCell(SizedBox(width:180,child:Text('$value',softWrap:true)))] )],dataRowMinHeight:56,dataRowMaxHeight:300)));
   case 'note':return Card(color:Theme.of(context).colorScheme.tertiaryContainer,child:Padding(padding:const EdgeInsets.all(16),child:SelectableText(block['text'])));
   default:return Padding(padding:const EdgeInsets.only(bottom:16),child:SelectableText(block['text'],style:Theme.of(context).textTheme.bodyLarge?.copyWith(height:1.6)));
  }
 }
}
class ReferenceFigure extends StatelessWidget {
 final ReferencePack pack;final String id;final String caption;
 const ReferenceFigure({super.key,required this.pack,required this.id,required this.caption});
 @override Widget build(BuildContext context) {
  final dynamic image=pack.images[id];if(image==null)return const SizedBox.shrink();
  return Padding(padding:const EdgeInsets.symmetric(vertical:12),child:Column(crossAxisAlignment:CrossAxisAlignment.start,children:[
   Semantics(label:caption,button:true,child:InkWell(onTap:()=>Navigator.push(context,MaterialPageRoute<void>(builder:(_)=>Scaffold(appBar:AppBar(title:Text(caption,overflow:TextOverflow.ellipsis)),body:SafeArea(child:Column(children:[Expanded(child:InteractiveViewer(minScale:0.5,maxScale:5,child:Center(child:Image.asset(image['asset'],fit:BoxFit.contain)))),Padding(padding:const EdgeInsets.all(16),child:Text('$caption\n${image['author']} · ${image['licence']}'))]))))),child:ClipRRect(borderRadius:BorderRadius.circular(16),child:Image.asset(image['asset'],width:double.infinity,height:250,fit:BoxFit.contain,excludeFromSemantics:true)))),
   Text(caption,style:Theme.of(context).textTheme.bodySmall),TextButton(onPressed:()=>detail(context,'Crédits de l’illustration',[SelectableText('${image['title']}\n${image['author']}\n${image['licence']}\n${image['changes']}'),TextButton(onPressed:()=>referenceUrl(context,image['source']),child:const Text('Voir la source')),TextButton(onPressed:()=>referenceUrl(context,image['licenceUrl']),child:const Text('Lire la licence'))]),child:Text('${image['author']} · ${image['licence']}',maxLines:2,overflow:TextOverflow.ellipsis)),
  ]));
 }
}
void openReferenceTimeline(BuildContext context,ReferencePack pack)=>Navigator.push(context,MaterialPageRoute<void>(builder:(_)=>Scaffold(appBar:AppBar(title:const Text('Chronologie du Sénégal')),body:ListView(padding:const EdgeInsets.all(16),children:[const Text('Les dates anciennes sont des repères de période ; une date de tradition n’a pas la même précision qu’une archive datée.'),for(final dynamic event in pack.data['timeline'] as List)Card(child:ListTile(leading:const Icon(Icons.timeline),title:Text(event['date'],style:const TextStyle(fontWeight:FontWeight.bold)),subtitle:Text(event['text']),trailing:const Icon(Icons.chevron_right),onTap:()=>openReferenceArticle(context,pack,event['article'])))]))));
void openReferenceGlossary(BuildContext context,ReferencePack pack)=>Navigator.push(context,MaterialPageRoute<void>(builder:(_)=>ReferenceGlossary(pack:pack)));
class ReferenceGlossary extends StatefulWidget {
 final ReferencePack pack;
 const ReferenceGlossary({super.key,required this.pack});
 @override State<ReferenceGlossary> createState()=>_ReferenceGlossaryState();
}
class _ReferenceGlossaryState extends State<ReferenceGlossary> {
 String query='';
 @override Widget build(BuildContext context) {
  final terms=(widget.pack.data['glossary'] as List).where((dynamic g)=>referenceNormalize('${g['term']} ${g['definition']}').contains(referenceNormalize(query))).toList();
  return Scaffold(appBar:AppBar(title:const Text('Vocabulaire & notions')),body:Column(children:[Padding(padding:const EdgeInsets.all(16),child:TextField(onChanged:(v)=>setState(()=>query=v),decoration:const InputDecoration(prefixIcon:Icon(Icons.search),labelText:'Chercher une notion'))),Expanded(child:ListView.builder(itemCount:terms.length,itemBuilder:(context,i){final dynamic t=terms[i];return ListTile(title:Text(t['term'],style:const TextStyle(fontWeight:FontWeight.bold)),subtitle:Text(t['definition']),onTap:()=>openReferenceArticle(context,widget.pack,t['article']));}))]));
 }
}
void openReferenceMap(BuildContext context,ReferencePack pack)=>Navigator.push(context,MaterialPageRoute<void>(builder:(_)=>ReferenceMapScreen(pack:pack)));
class ReferenceMapScreen extends StatefulWidget {
 final ReferencePack pack;
 const ReferenceMapScreen({super.key,required this.pack});
 @override State<ReferenceMapScreen> createState()=>_ReferenceMapScreenState();
}
class _ReferenceMapScreenState extends State<ReferenceMapScreen> {
 String selected='';
 @override Widget build(BuildContext context) {
  final features=widget.pack.data['map']['features'] as List;final region=widget.pack.byId[selected];
  return Scaffold(appBar:AppBar(title:const Text('Les 14 régions du Sénégal')),body:ListView(padding:const EdgeInsets.all(16),children:[
   const Text('Touchez une région ou choisissez son nom. La carte peut être agrandie avec deux doigts.'),
   LayoutBuilder(builder:(context,bounds)=>SizedBox(height:math.max(280.0,bounds.maxWidth*0.82),child:InteractiveViewer(minScale:1,maxScale:4,child:LayoutBuilder(builder:(context,box){final size=Size(box.maxWidth,box.maxHeight);final geometry=ReferenceMapGeometry(features,size);return GestureDetector(onTapUp:(tap){for(final entry in geometry.paths.entries){if(entry.value.contains(tap.localPosition)){setState(()=>selected=entry.key);break;}}},child:CustomPaint(size:size,painter:ReferenceMapPainter(geometry:geometry,selected:selected,colors:Theme.of(context).colorScheme)));})))),
   Wrap(spacing:6,children:[for(final dynamic feature in features)ChoiceChip(label:Text(feature['name']),selected:selected==feature['article'],onSelected:(_)=>setState(()=>selected=feature['article']))]),
   if(region!=null)...[section(region['title']),Text(region['summary']),FilledButton.icon(onPressed:()=>openReferenceArticle(context,widget.pack,selected),icon:const Icon(Icons.menu_book_outlined),label:const Text('Lire la fiche régionale'))],
   section('Lire cette carte'),const Text('Le nord est en haut. La Gambie forme une bande à l’intérieur du contour sénégalais et dispose de sa propre façade maritime. Les couleurs distinguent les régions ; elles ne représentent ni la population ni le relief.'),
   Text(widget.pack.data['map']['credit'],style:Theme.of(context).textTheme.bodySmall),TextButton(onPressed:()=>referenceSources(context,widget.pack,['map']),child:const Text('Source cartographique')),TextButton(onPressed:()=>referenceUrl(context,widget.pack.data['map']['licenceUrl']),child:const Text('Licence CC BY 3.0 IGO')),
  ]));
 }
}
class ReferenceMapGeometry {
 final Map<String,Path> paths={};final Size size;
 late final double factor,left,top;
 Offset project(double longitude,double latitude)=>Offset(left+(longitude+17.65)*factor,top+(16.75-latitude)*factor);
 ReferenceMapGeometry(List<dynamic> features,this.size) {
  const minX=-17.65,maxX=-11.30,minY=12.25,maxY=16.75;
  factor=math.min((size.width-34)/(maxX-minX),(size.height-48)/(maxY-minY));
  left=(size.width-(maxX-minX)*factor)/2;top=(size.height-(maxY-minY)*factor)/2;
  for(final dynamic f in features){final path=Path()..fillType=PathFillType.evenOdd;for(final dynamic polygon in f['polygons'] as List){for(final dynamic ring in polygon as List){var first=true;for(final dynamic p in ring as List){final x=left+((p[0] as num)-minX)*factor;final y=top+(maxY-(p[1] as num))*factor;if(first){path.moveTo(x,y);first=false;}else{path.lineTo(x,y);}}path.close();}}paths[f['article']]=path;}
 }
}
class ReferenceMapPainter extends CustomPainter {
 final ReferenceMapGeometry geometry;final String selected;final ColorScheme colors;
 ReferenceMapPainter({required this.geometry,required this.selected,required this.colors});
 @override void paint(Canvas canvas,Size size) {
  canvas.drawRRect(RRect.fromRectAndRadius(Offset.zero&size,const Radius.circular(18)),Paint()..color=colors.surfaceContainerHighest);
  var i=0;for(final entry in geometry.paths.entries){
   final hue=(150.0+i++*37.0)%360;
   final fill=HSVColor.fromAHSV(1,hue,colors.brightness==Brightness.dark?0.35:0.24,colors.brightness==Brightness.dark?0.42:0.93).toColor();
   canvas.drawPath(entry.value,Paint()..color=entry.key==selected?colors.tertiary:fill);
   canvas.drawPath(entry.value,Paint()..color=colors.onSurface..style=PaintingStyle.stroke..strokeWidth=entry.key==selected?2.5:0.7);
  }
  void label(String text,Offset position){final painter=TextPainter(text:TextSpan(text:text,style:TextStyle(color:colors.onSurface,fontSize:11,fontWeight:FontWeight.w600)),textDirection:TextDirection.ltr)..layout();painter.paint(canvas,position);}
  label('N ↑',const Offset(12,10));label('OCÉAN\nATLANTIQUE',Offset(8,size.height*0.48));label('GAMBIE',geometry.project(-16.0,13.60));label('Carte de repérage · limites simplifiées',Offset(12,size.height-20));
 }
 @override bool shouldRepaint(covariant ReferenceMapPainter old)=>old.selected!=selected||old.geometry!=geometry||old.colors!=colors;
}
