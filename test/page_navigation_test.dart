import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:enseignant/library.dart';

void main() {
  testWidgets('Recherche de page : fermeture du dialogue sans contrôleur réutilisé', (tester) async {
    int? selected;
    await tester.pumpWidget(MaterialApp(home: Builder(builder: (context) => Scaffold(
      body: FilledButton(
        onPressed: () async {
          selected = await showDialog<int>(
            context: context,
            builder: (_) => const PageJumpDialog(initialPage: 1, totalPages: 468),
          );
        },
        child: const Text('Chercher'),
      ),
    ))));

    await tester.tap(find.text('Chercher'));
    await tester.pumpAndSettle();
    await tester.enterText(find.byType(TextField), '468');
    await tester.tap(find.text('Ouvrir'));
    await tester.pumpAndSettle();
    expect(selected, 468);
    expect(tester.takeException(), isNull);

    await tester.tap(find.text('Chercher'));
    await tester.pumpAndSettle();
    await tester.tap(find.text('Annuler'));
    await tester.pumpAndSettle();
    expect(tester.takeException(), isNull);
  });
}
