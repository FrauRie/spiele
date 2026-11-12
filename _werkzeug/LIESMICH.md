# Werkzeug für dieses Repo (Stand 12.11.2026)

Bauskripte und Vorlagen, mit denen Startseite, Spielstunde, Handy-Seite und Bingo-Rufer erzeugt wurden.
Die Skripte erwarten ihre Dateien unter `/tmp/work/` und das Repo unter `/home/claude/spiele/` – vor dem Start dorthin kopieren.

| Datei | Zweck |
|---|---|
| `musik.html` | Musik-Baustein (3 eigene Stücke, Knopf unten links, `localStorage rie_musik`). Steht in jedem Spiel direkt vor `</body>`. In neue Spiele genauso einsetzen. |
| `ton.html` | Ton-Baustein (Knopf 🔔 unten links zwischen Musik und Automatik, `localStorage rie_ton`, Standard aus): kurzer eigener Zweiklang, sobald die Lösung erscheint; bei „Was sagen die meisten?“ pro aufgedeckter Antwort. Steht vor dem Automatik- bzw. Musik-Baustein. In allen Spielen außer Sortiertafel, Suchsel und Buchstaben-Pizza. Neues Spiel: im Baustein prüfen, ob die Lösung erkannt wird (Funktion `K`). |
| `auto.html` | Automatik-Baustein (Knopf „⏱ Auto“ unten links neben der Musik, `localStorage rie_auto`, Standard an, gilt für alle Spiele gemeinsam). Steht direkt vor dem Musik-Baustein. An: Bingo löst jedes Wort nach 5/8/12 s auf · Boss-Runde, Exit-Quiz, Fehler-Detektiv, Satz-Chaos: die Zeit startet 3 s nach jeder neuen Aufgabe von selbst, am Ende kommt die Lösung · Zoom-Bild: Zeit pro Schritt läuft von selbst, dann nächster Schritt, nach dem letzten die Auflösung · Wer bin ich?: nach der Zeit kommt der nächste Satz von selbst · Was sagen die meisten?: nach der Schreibzeit (oder nach „Antworten aufdecken“) kommt alle 4 s die nächste Antwort. Aus: alles wie bisher mit Knopf. Neues Spiel mit Zeit: im Baustein einen Eintrag ergänzen (ready/sig/lead/go). |
| `fonts.css` | Andika, eingebettet (für neue Spiele) |
| `bingo_tpl.html` + `build_bingo.py` | Bingo-Rufer; Wörter und Bilder kommen aus `spiele/vokabelcheck/vokabelcheck.html` (`dW`, `dIMG`); Handy-Karte kontrolliert sich selbst: 6-stelliger Spielcode (Startwert + Einstellungen, auch im QR-Link `#s=…&karte=1`) und 3-stellige Prüfzahl neben 📱 pro gezogenem Wort – daraus weiß das Handy, welche Wörter schon dran waren; falsche Kreuze werden gelöscht, erneut prüfen erst beim nächsten Wort |
| `stunde_tpl.html`, `index_new_tpl.html`, `index_old.html` + `build_pages.py` | bauen `spielstunde.html`, `handy.html`, `index.html`; neue Spiele in `build_pages.py` eintragen (Liste `einzel`, `DESC`, `KIND`, `TXT`) |
| `meisten_tpl.html`, `sortiertafel_tpl.html` + `build_neu.py` | bauen „Was sagen die meisten?“ und die Sortiertafel. Sortiertafel: Wörter und Bilder aus dem Vokabelcheck (`dW`, `dIMG`); die Ausdrücke für wo?/wohin? stehen von Hand in `build_neu.py` (Liste `WW`). Nach einem neuen Vokabelcheck `build_neu.py` neu laufen lassen. |
| `spiele/suchsel/suchsel.html` | Suchsel (36 Themen, nur ●-Wörter, „Bild“ oder „Bild + Wort“, Druckknopf). Fertig gebaute Einzeldatei; Wörter und Bilder kommen aus dem Suchsel-Generator im Material-Ordner (`08_Vorlagen_BS29/Suchsel_Generator/topics.json`, `topics2.json`), nicht aus dem Vokabelcheck. Eingetragen in `build_pages.py` (Startseite, Spielstunde, Handy-Seite). |
| `build_blitz.py` + `blitz_listen.py` + `blitz_namen.json` | Blitz! (Dobble) → `spiele/blitz/`: 16 Bild-Blitz-Sets aus `Blitz_Dobble/Smartboard/Blitz_Smartboard_*_Rie_v*.html` (Material-Ordner, nach `/tmp/work/blitz_src/` kopieren) plus 13 Wort-Blitz-Sets Blitzlesen (Wortlisten aus `Blitz_Generator_Blitzlesen_Rie_v1.py`; Verwechslungs-Sets ganz schwarz). Setzt Ton + Musik ein, Spielart „Für sich / Erklären“ oder „Duell“. Kein Automatik-Baustein (keine Zeit). Neues Blitz-Set: erst im Material-Ordner bauen, dann `build_blitz.py` und `build_pages.py` laufen lassen (Zahl im Chip in `index_new_tpl.html` und `assert n==` anpassen). |
| `patch.py` | einmaliger Umbau: „Zeigen!“-Schritt entfernt |
| `zoom_sheets.py` | Zoompunkte prüfen (Startausschnitt, Weißanteil) |

QR-Code: `npm pack qrcode-generator@1.4.4`, entpackt nach `/tmp/work/package/`.

## Regeln für alle Spiele
- Kein „Zeigen!“-Schritt: nach der Schreibzeit kommt direkt die Lösung.
- Funktioniert ohne Ton; Musik und Lösungston nur über die Knöpfe (Standard aus).
- Spiele mit Zeit lösen bei „⏱ Auto an“ von selbst auf; mit „Auto aus“ bleibt der Knopf wie bisher.
- „Jeder für sich“ muss möglich sein; Teams heißen nach Plätzen (Tür, Fenster, Mitte …), 1 Punkt pro Team und Runde.
- Schrift Andika, Hintergrund #F1EFEB, Orange #D9690A, Grün #059E42, Rosa #F2A7C3; Vollbild-Knopf, Taste F.
- Artikelfarben: der #5B8DB8 · die #FA3A2F · das #269A31 · Plural #AF7F23 · Verben #D9690A · Adjektive #3A8C8C.
- Immer „Plural“/„Singular“ und „Infinitiv“; auf Spielen nur Punkte ●/●●/●●●, keine Niveauangaben.
- Öffentliches Repo: keine Namen, Fotos oder Daten von Schüler:innen.

## Daten, die nur auf dem Gerät liegen
- „Was sagen die meisten?“: Fragen und Antworten stehen im `localStorage` (`rie_meisten_v1`) des Geräts, nicht im Repo. Weitergabe über Export/Import im Spiel (JSON-Datei). Im Repo stehen nur 3 erfundene Beispielfragen.
- Fertiger Satz „Deutschland“ (Liste `FERTIG` in `meisten_tpl.html`): 9 Fragen mit echten Zahlen (Quelle steht an jeder Frage, Stand 12.11.2026) und 7 geschätzte Fragen (`art:"g"`, im Spiel als „geschätzt“ markiert). Neue Umfragen dort ergänzen, Quelle immer mit Jahr.

## Fehler-Detektiv: Sätze und Themengruppen (Stand 12.11.2026)
- Sätze stehen in zwei Blöcken in `spiele/fehler-detektiv/fehler-detektiv-grammatik-dienstag.html`: `saetze-original` (14 Themen) und `saetze-neu` (neue Sätze für diese Themen, 14 Themen „später“, 10 Themen „Experten“).
- Themenkopf: `# Name | Hinweis für ● | später` bzw. `| Experten`. Solche Themen sind beim Start nicht ausgewählt und stehen auf dem Startbildschirm zum Aufklappen („Kommt später“, „Experten“). „Alle“ meint nur die Themen ohne Gruppe.
- Quelle der neuen Sätze: Reihen „Grammatik interaktiv“ im Material-Ordner (Basis, A2-Reihe mit Satzpool `19_Moodle_Wortschatz/Grammatik_Interaktiv_A2/Grammatik_Interaktiv_Satzpool_Rie_v1.json`, Experten). Wortschatz nicht gegen das ABC-Lexikon geprüft.
- Geräte mit eigenen gespeicherten Sätzen (`localStorage fehlerdetektiv_saetze_v2`) bekommen die neuen Themen und Sätze einmalig dazugemischt (Merker `fehlerdetektiv_saetze_v2_neu1`); eigene Änderungen bleiben.
- Weitere neue Sätze später: neuen Block und neuen Merker anlegen (z. B. `saetze-neu2`, `_neu2`), nicht den alten Block ändern – sonst kommen sie auf Geräten mit gespeicherten Sätzen nicht an.

## Noch offen
- Wort-Comeback für die Leseheft-Wörter (Wortlisten kommen von Frau Rie).
