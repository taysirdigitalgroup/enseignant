import 'dart:async';
import 'dart:convert';
import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'core.dart' show bridge;
import 'main.dart' show store, perform, message, recordOptions, optionsButton, empty, confirm, detail, section;

Future<void> dictionaryLicence(BuildContext context,String name) async {
 final file=name=='Wiktionnaire'?'CC-BY-SA-4.0-fr.txt':'Licence-Ouverte.md';
 try {
  final text=await rootBundle.loadString('assets/dictionary/licenses/$file');
  if(context.mounted)detail(context,'Licence · $name',[SelectableText(text)]);
 }catch(e){if(context.mounted)message(context,'Licence indisponible : $e');}
}

String dictionaryFavorite(int id)=>'dictionary:$id';
List<int> dictionaryFavorites()=>(store.data['favorites'] as List).whereType<String>().where((v)=>v.startsWith('dictionary:')).map((v)=>int.tryParse(v.substring(11))).whereType<int>().toList();
List<int> dictionaryHistory()=>((store.data['dictionaryHistory'] as List?)??[]).whereType<String>().map(int.tryParse).whereType<int>().toList();
Future<void> rememberDictionary(int id)=>store.change((data){final rows=List<String>.from((data['dictionaryHistory'] as List?)??[]);rows.remove('$id');rows.insert(0,'$id');data['dictionaryHistory']=rows.take(50).toList();});

class DictionaryResult {
 final List<Map<String,dynamic>> rows;final int total;final bool hasMore;
 const DictionaryResult(this.rows,this.total,this.hasMore);
}
class DictionaryRepository {
 final MethodChannel channel;
 const DictionaryRepository({this.channel=bridge});
 Future<Map<String,dynamic>> info() async {
  final raw=await channel.invokeMethod<String>('dictionaryInfo');
  if(raw==null)throw StateError('Informations du dictionnaire indisponibles.');
  return Map<String,dynamic>.from(jsonDecode(raw) as Map);
 }
 Future<DictionaryResult> search({String query='',String mode='word',String letter='',String category='',String source='',List<int>? ids,int offset=0}) async {
  final raw=await channel.invokeMethod<Map>('dictionarySearch',{'query':query,'mode':mode,'letter':letter,'category':category,'source':source,if(ids!=null)'ids':ids,'offset':offset,'limit':60});
  if(raw==null)throw StateError('Résultats indisponibles.');
  return DictionaryResult((raw['rows'] as List).map((v)=>Map<String,dynamic>.from(v as Map)).toList(),(raw['total'] as num).toInt(),raw['hasMore']==true);
 }
 Future<Map<String,dynamic>> entry(int id) async {
  final raw=await channel.invokeMethod<Map>('dictionaryEntry',{'id':id});
  if(raw==null)throw StateError('Article introuvable.');
  final data=Map<String,dynamic>.from(raw);
  data['paragraphs']=jsonDecode(data['paragraphs'] as String);
  data['references']=jsonDecode(data['references'] as String);
  return data;
 }
}

class DictionaryScreen extends StatefulWidget {
 final DictionaryRepository repository;
 const DictionaryScreen({super.key,this.repository=const DictionaryRepository()});
 @override State<DictionaryScreen> createState()=>_DictionaryScreenState();
}
class _DictionaryScreenState extends State<DictionaryScreen> {
 final controller=TextEditingController();Timer? debounce;
 Map<String,dynamic>? metadata;List<Map<String,dynamic>> rows=[];
 String mode='word',letter='',category='',collection='all',sourceFilter='',error='';
 int generation=0,total=0;bool loading=true,hasMore=false;
 @override void initState(){super.initState();unawaited(initialize());}
 @override void dispose(){debounce?.cancel();controller.dispose();super.dispose();}
 Future<void> initialize() async {
  try {final info=await widget.repository.info();if(!mounted)return;setState(()=>metadata=info);await search();}
  catch(e){if(mounted)setState((){loading=false;error='$e';});}
 }
 Future<void> search({bool more=false}) async {
  if(more&&loading)return;
  final token=more?generation:++generation;
  final start=more?rows.length:0;
  setState((){loading=true;error='';if(!more)rows=[];});
  final ids=collection=='favorites'?dictionaryFavorites():collection=='history'?dictionaryHistory():null;
  try{
   final result=await widget.repository.search(query:controller.text.trim(),mode:mode,letter:letter,category:category,source:sourceFilter,ids:ids,offset:start);
   if(!mounted||token!=generation)return;
   setState((){rows=[if(more)...rows,...result.rows];total=result.total;hasMore=result.hasMore;loading=false;
    if(collection=='history'&&ids!=null)rows.sort((a,b)=>ids.indexOf(a['id']).compareTo(ids.indexOf(b['id'])));
   });
  }catch(e){if(mounted&&token==generation)setState((){error='$e';loading=false;});}
 }
 Future<void> refresh() async {await store.reload();if(mounted){if(metadata==null){await initialize();}else{await search();}}}
 Future<void> open(int id) async {
  if(metadata==null)return;
  await Navigator.push(context,MaterialPageRoute<void>(builder:(_)=>DictionaryArticleScreen(id:id,metadata:metadata!,repository:widget.repository)));
  if(mounted&&collection!='all')await search();
 }
 Future<void> toggle(int id) async {await perform(context,()=>store.toggle('favorites',dictionaryFavorite(id)));if(mounted&&collection=='favorites')await search();}

 @override Widget build(BuildContext context)=>ListenableBuilder(listenable:store,builder:(context,_){
  final letters=metadata==null?<String>[]:(metadata!['letters'] as Map).keys.cast<String>().toList();
  final categories=metadata==null?<String>[]:(metadata!['categories'] as Map).keys.cast<String>().toList();
  return Scaffold(appBar:AppBar(title:const Text('Dictionnaire',overflow:TextOverflow.ellipsis),actions:[IconButton(tooltip:'Sources et licences',icon:const Icon(Icons.info_outline),onPressed:()=>detail(context,'À propos du dictionnaire',[
   section('Deux sources complémentaires'),
   const Text('Wiktionnaire : définitions en français, prononciations, étymologies et relations lexicales. FranceTerme : vocabulaire scientifique et technique publié au Journal officiel français.'),
   if(metadata!=null)...[
    Text('Pack intégré le ${metadata!['builtAt']} · dump Wiktionnaire du 01/10/2026.'),
    for(final dynamic src in metadata!['sources'] as List)...[
     section(src['name']),SelectableText('${src['credit']}\n${src['licence']}\n${src['changes']}'),
     TextButton(onPressed:()=>dictionaryLicence(context,src['name']),child:const Text('Lire la licence hors connexion')),
    ],
   ],
   const Text('Les marques de registre, les régionalismes et les emplois anciens appartiennent aux articles de la source. Les données modernes ne constituent pas un programme scolaire sénégalais. Les citations littéraires et les médias ne sont pas inclus. La consultation et la recherche fonctionnent hors connexion ; les liens de provenance nécessitent Internet.'),
  ]))]),body:RefreshIndicator(onRefresh:refresh,child:CustomScrollView(physics:const AlwaysScrollableScrollPhysics(),slivers:[
   SliverToBoxAdapter(child:Padding(padding:const EdgeInsets.all(16),child:Column(crossAxisAlignment:CrossAxisAlignment.start,children:[
    Text('Les mots à portée de main',style:Theme.of(context).textTheme.headlineSmall),const SizedBox(height:6),const Chip(avatar:Icon(Icons.offline_pin_outlined,size:18),label:Text('Français · sciences · techniques · histoire')),
    if(metadata!=null)Text('${metadata!['counts']['entries']} articles indexés · consultation hors connexion'),
    const Text('Comparez les sources depuis un article et retrouvez les formes fléchies par la recherche.'),const SizedBox(height:14),
    TextField(controller:controller,decoration:InputDecoration(labelText:'Mot, expression ou définition',prefixIcon:const Icon(Icons.search),suffixIcon:IconButton(tooltip:'Effacer la recherche',icon:const Icon(Icons.clear),onPressed:(){debounce?.cancel();controller.clear();unawaited(search());})),onChanged:(_){debounce?.cancel();debounce=Timer(const Duration(milliseconds:280),(){if(mounted)unawaited(search());});}),
    Wrap(spacing:6,children:[for(final item in [('word','Début du mot'),('exact','Mot exact'),('definitions','Définitions')])ChoiceChip(label:Text(item.$2),selected:mode==item.$1,onSelected:(_){setState(()=>mode=item.$1);unawaited(search());})]),
    const Text('Recherche sans distinction de casse ni d’accents. En mode Définitions, tous les mots recherchés doivent apparaître dans un même article.'),
    Wrap(spacing:6,children:[for(final name in ['', 'Wiktionnaire', 'FranceTerme'])ChoiceChip(label:Text(name.isEmpty?'Toutes les sources':name),selected:sourceFilter==name,onSelected:(_){setState(()=>sourceFilter=name);unawaited(search());})]),
    Wrap(spacing:6,children:[for(final item in [('all','Tout',Icons.menu_book_outlined),('favorites','Favoris',Icons.bookmark_border),('history','Récents',Icons.history)])FilterChip(label:Text(item.$2),avatar:Icon(item.$3,size:18),selected:collection==item.$1,onSelected:(_){setState(()=>collection=item.$1);unawaited(search());})]),
    if(collection=='history')TextButton(onPressed:() async {if(await confirm(context,'Effacer l’historique ?','Seules les consultations récentes du dictionnaire seront retirées.')&&context.mounted){await perform(context,()=>store.change((d)=>d['dictionaryHistory']=<String>[]));if(mounted)await search();}},child:const Text('Effacer les consultations récentes')),
    const SizedBox(height:8),DropdownButtonFormField<String>(key:ValueKey('dict-category-$category'),initialValue:category,isExpanded:true,decoration:const InputDecoration(labelText:'Emploi grammatical ou domaine'),items:[const DropdownMenuItem(value:'',child:Text('Tous les emplois')),for(final c in categories)DropdownMenuItem(value:c,child:Text(c))],onChanged:(v){setState(()=>category=v!);unawaited(search());}),
    const SizedBox(height:8),SizedBox(height:49,child:ListView(scrollDirection:Axis.horizontal,children:[Padding(padding:const EdgeInsets.only(right:5),child:ChoiceChip(label:const Text('A–Z'),selected:letter.isEmpty,onSelected:(_){setState(()=>letter='');unawaited(search());})),for(final l in letters)Padding(padding:const EdgeInsets.only(right:5),child:ChoiceChip(label:Text(l),selected:letter==l,onSelected:(_){setState(()=>letter=l);unawaited(search());}))])),
    if(!loading)Text('$total résultat(s)',style:const TextStyle(fontWeight:FontWeight.bold)),
    if(error.isNotEmpty)...[Text('Chargement impossible : $error'),TextButton(onPressed:()=>metadata==null?initialize():search(),child:const Text('Réessayer'))],
   ]))),
   if(loading&&rows.isEmpty)const SliverToBoxAdapter(child:Padding(padding:EdgeInsets.all(28),child:Center(child:CircularProgressIndicator()))),
   if(!loading&&error.isEmpty&&rows.isEmpty)SliverToBoxAdapter(child:empty(collection=='favorites'?'Aucun favori pour ces filtres. Marquez un article avec le signet.':collection=='history'?'Aucune consultation pour ces filtres.':'Aucun article trouvé. Essayez un début de mot ou le mode Définitions.')),
   SliverList.builder(itemCount:rows.length,itemBuilder:(context,i){final word=rows[i];final id=word['id'] as int;final saved=store.contains('favorites',dictionaryFavorite(id));final actions=<(String,IconData,VoidCallback)>[
    ('Ouvrir l’article',Icons.menu_book_outlined,()=>open(id)),(saved?'Retirer des favoris':'Ajouter aux favoris',saved?Icons.bookmark:Icons.bookmark_border,()=>toggle(id)),
   ];return Padding(padding:const EdgeInsets.symmetric(horizontal:16),child:Card(child:ListTile(title:Text(word['headword'],style:const TextStyle(fontWeight:FontWeight.w700)),subtitle:Column(crossAxisAlignment:CrossAxisAlignment.start,children:[Text("${word['source']} · ${word['category']}",style:Theme.of(context).textTheme.labelMedium),const SizedBox(height:5),Text(word['preview'],maxLines:3,overflow:TextOverflow.ellipsis)]),onTap:()=>open(id),onLongPress:()=>recordOptions(context,actions),trailing:Row(mainAxisSize:MainAxisSize.min,children:[IconButton(tooltip:saved?'Retirer des favoris':'Ajouter aux favoris',icon:Icon(saved?Icons.bookmark:Icons.bookmark_border),onPressed:()=>toggle(id)),optionsButton(actions)]))));}),
   if(hasMore)SliverToBoxAdapter(child:Padding(padding:const EdgeInsets.all(16),child:FilledButton(onPressed:loading?null:()=>search(more:true),child:Text(loading?'Chargement…':'Afficher la suite (${rows.length}/$total)')))),
   const SliverToBoxAdapter(child:SizedBox(height:24)),
  ])));
 });
}

class DictionaryArticleScreen extends StatefulWidget {
 final int id;final Map<String,dynamic> metadata;final DictionaryRepository repository;
 const DictionaryArticleScreen({super.key,required this.id,required this.metadata,required this.repository});
 @override State<DictionaryArticleScreen> createState()=>_DictionaryArticleScreenState();
}
class _DictionaryArticleScreenState extends State<DictionaryArticleScreen> {
 late Future<Map<String,dynamic>> loading;
 @override void initState(){super.initState();loading=load();}
 Future<Map<String,dynamic>> load() async {final article=await widget.repository.entry(widget.id);if(mounted)unawaited(perform(context,()=>rememberDictionary(widget.id)));return article;}
 void related(int id,{bool replace=false}){final route=MaterialPageRoute<void>(builder:(_)=>DictionaryArticleScreen(id:id,metadata:widget.metadata,repository:widget.repository));if(replace){Navigator.pushReplacement(context,route);}else{Navigator.push(context,route);}}
 @override Widget build(BuildContext context)=>ListenableBuilder(listenable:store,builder:(context,_)=>Scaffold(appBar:AppBar(title:const Text('Article du dictionnaire',overflow:TextOverflow.ellipsis),actions:[IconButton(tooltip:'Favori',icon:Icon(store.contains('favorites',dictionaryFavorite(widget.id))?Icons.bookmark:Icons.bookmark_border),onPressed:()=>perform(context,()=>store.toggle('favorites',dictionaryFavorite(widget.id))))]),body:FutureBuilder<Map<String,dynamic>>(future:loading,builder:(context,s){
  if(s.hasError)return Center(child:Column(mainAxisSize:MainAxisSize.min,children:[Text('Article indisponible : ${s.error}'),TextButton(onPressed:()=>setState(()=>loading=load()),child:const Text('Réessayer'))]));
  if(!s.hasData)return const Center(child:CircularProgressIndicator());
  final a=s.data!;final refs=a['references'] as List;final paragraphs=a['paragraphs'] as List;
  final citation='${a['source']}, « ${a['headword']} », ${a['publication']}. ${a['sourceUrl']} · ${a['licence']}. Extraction et mise en forme pour Enseignant. Contributions : ${a['source']=='Wiktionnaire'?'contributeurs du Wiktionnaire, via Wiktextract / Kaikki.org':'ministère de la Culture, Commission d’enrichissement de la langue française'}.';
  return ListView(padding:const EdgeInsets.all(20),children:[
   Text(a['headword'],style:Theme.of(context).textTheme.headlineMedium),Wrap(spacing:8,children:[Chip(label:Text(a['category'])),Chip(label:Text(a['source']))]),
   OutlinedButton.icon(onPressed:()=>perform(context,()=>bridge.invokeMethod<void>('openUrl',a['sourceUrl'])),icon:const Icon(Icons.open_in_new),label:const Text('Consulter la provenance en ligne')),
   if((a['alternatives'] as List? ?? []).isNotEmpty)...[section('Comparer les autres sources'),for(final dynamic other in a['alternatives'] as List)Card(child:ListTile(title:Text(other['source']),subtitle:Text(other['headword']),trailing:const Icon(Icons.chevron_right),onTap:()=>related(other['id'])))],
   const SizedBox(height:12),
   for(final p in paragraphs)Padding(padding:const EdgeInsets.only(bottom:18),child:SelectableText.rich(TextSpan(style:Theme.of(context).textTheme.bodyLarge?.copyWith(fontSize:18,height:1.55),children:[for(final dynamic run in p as List)TextSpan(text:run['text'] as String,style:TextStyle(fontWeight:run['bold']==true?FontWeight.w700:FontWeight.normal,fontStyle:run['italic']==true?FontStyle.italic:FontStyle.normal))]))),
   if(refs.isNotEmpty)...[section('Renvois reconnus dans l’article'),for(final dynamic ref in refs)Card(child:ListTile(leading:const Icon(Icons.link),title:Text(ref['headword']),subtitle:Text("${ref['category']}${ref['page']>0?' · p. ${ref['page']}':''}\n${ref['preview']}",maxLines:3,overflow:TextOverflow.ellipsis),onTap:()=>related(ref['id'])))],
   TextButton(onPressed:()=>dictionaryLicence(context,a['source']),child:Text('Licence : ${a['licence']}')),
   section('Référence de l’article'),SelectableText(citation,style:Theme.of(context).textTheme.bodySmall),
   Wrap(spacing:8,children:[TextButton.icon(icon:const Icon(Icons.copy),label:const Text('Copier la référence'),onPressed:() async {await Clipboard.setData(ClipboardData(text:citation));if(context.mounted)message(context,'Référence copiée.');}),TextButton.icon(icon:const Icon(Icons.content_copy),label:const Text('Copier le texte'),onPressed:() async {await Clipboard.setData(ClipboardData(text:'${a['headword']}\n\n${a['body']}\n\n$citation'));if(context.mounted)message(context,'Texte copié.');})]),
   const SizedBox(height:16),
  ]);
 })));
}

