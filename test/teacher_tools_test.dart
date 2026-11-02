import 'package:flutter_test/flutter_test.dart';
import 'package:enseignant/teacher_tools.dart';

void main() {
 const pupil=<String,dynamic>{'id':'a','name':'Awa'};
 test('une seule note ne produit pas une appréciation définitive',(){
  final report=assessPupil(pupil,[{'max':20,'weight':1,'scores':{'a':3}}],[]);
  expect(report.group,'Données limitées');
  expect(report.mean,3);
  expect(report.absent,0);
  expect(report.calls,0);
 });
 test('les notes vides ne sont pas des zéros et les barèmes sont ramenés sur 20',(){
  final report=assessPupil(pupil,[
   {'max':10,'weight':2,'scores':{'a':8}},
   {'max':20,'weight':1,'scores':{'a':10}},
   {'max':20,'weight':1,'scores':{}},
  ],[]);
  expect(report.mean,14);
  expect(report.marks,2);
  expect(report.examCount,3);
  expect(report.group,'À encourager');
 });
 test('absences, retards et appels non renseignés restent distincts',(){
  final report=assessPupil(pupil,[],[
   {'pupilId':'a','status':'Absent'},
   {'pupilId':'a','status':'Retard'},
   {'pupilId':'a','status':'Excusé'},
   {'pupilId':'b','status':'Absent'},
  ]);
  expect(report.absent,1);
  expect(report.late,1);
  expect(report.excused,1);
  expect(report.present,0);
  expect(report.calls,3);
 });
 test('la couleur d’une matière est stable malgré la casse et les accents',(){
  expect(subjectColor('FRANÇAIS'),subjectColor('francais'));
  expect(slotSubject({'title':'Mathématiques / CM2','subject':''}),'Mathématiques');
  expect(slotSubject({'title':'CM2 A','subject':'Sciences'}),'Sciences');
 });
}
