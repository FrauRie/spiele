# Werkzeug für dieses Repo (Stand 12.11.2026)

Bauskripte und Vorlagen, mit denen Startseite, Spielstunde, Handy-Seite und Bingo-Rufer erzeugt wurden.
Die Skripte erwarten ihre Dateien unter `/tmp/work/` und das Repo unter `/home/claude/spiele/` – vor dem Start dorthin kopieren.

| Datei | Zweck |
|---|---|
| `musik.html` | Musik-Baustein (3 eigene Stücke, Knopf unten links, `localStorage rie_musik`). Steht in jedem Spiel direkt vor `</body>`. In neue Spiele genauso einsetzen. |
| `fonts.css` | Andika, eingebettet (für neue Spiele) |
| `bingo_tpl.html` + `build_bingo.py` | Bingo-Rufer; Wörter und Bilder kommen aus `spiele/vokabelcheck/vokabelcheck.html` (`dW`, `dIMG`); Handy-Karte kontrolliert sich selbst: 6-stelliger Spielcode (Startwert + Einstellungen, auch im QR-Link `#s=…&karte=1`) und 3-stellige Prüfzahl neben 📱 pro gezogenem Wort – daraus weiß das Handy, welche Wörter schon dran waren; falsche Kreuze werden gelöscht, erneut prüfen erst beim nächsten Wort |
| `stunde_tpl.html`, `index_new_tpl.html`, `index_old.html` + `build_pages.py` | bauen `spielstunde.html`, `handy.html`, `index.html`; neue Spiele in `build_pages.py` eintragen (Liste `einzel`, `DESC`, `KIND`, `TXT`) |
| `meisten_tpl.html`, `sortiertafel_tpl.html` + `build_neu.py` | bauen „Was sagen die meisten?“ und die Sortiertafel. Sortiertafel: Wörter und Bilder aus dem Vokabelcheck (`dW`, `dIMG`); die Ausdrücke für wo?/wohin? stehen von Hand in `build_neu.py` (Liste `WW`). Nach einem neuen Vokabelcheck `build_neu.py` neu laufen lassen. |
| `spiele/suchsel/suchsel.html` | Suchsel (36 Themen, nur ●-Wörter, „Bild“ oder „Bild + Wort“, Druckknopf). Fertig gebaute Einzeldatei; Wörter und Bilder kommen aus dem Suchsel-Generator im Material-Ordner (`08_Vorlagen_BS29/Suchsel_Generator/topics.json`, `topics2.json`), nicht aus dem Vokabelcheck. Eingetragen in `build_pages.py` (Startseite, Spielstunde, Handy-Seite). |
| `spiele/suchsel/suchsel.html` | Suchsel (36 Themen, nur ●-Wörter, „Bild“ oder „Bild + Wort“, Druckknopf). Fertig gebaute Einzeldatei; Wörter und Bilder kommen aus dem Suchsel-Generator im Material-Ordner (`08_Vorlagen_BS29/Suchsel_Generator/topics.json`, `topics2.json`), nicht aus dem Vokabelcheck. Eingetragen in `build_pages.py` (Startseite, Spielstunde, Handy-Seite). |
| `patch.py` | einmaliger Umbau: „Zeigen!“-Schritt entfernt |
| `zoom_sheets.py` | Zoompunkte prüfen (Startausschnitt, Weißanteil) |

QR-Code: `npm pack qrcode-generator@1.4.4`, entpackt nach `/tmp/work/package/`.

## Regeln für alle Spiele
- Kein „Zeigen!“-Schritt: nach der Schreibzeit kommt direkt die Lösung.
- Funktioniert ohne Ton; Musik nur über den Knopf (Standard aus).
- „Jeder für sich“ muss möglich sein; Teams heißen nach Plätzen (Tür, Fenster, Mitte …), 1 Punkt pro Team und Runde.
- Schrift Andika, Hintergrund #F1EFEB, Orange #D9690A, Grün #059E42, Rosa #F2A7C3; Vollbild-Knopf, Taste F.
- Artikelfarben: der #5B8DB8 · die #FA3A2F · das #269A31 · Plural #AF7F23 · Verben #D9690A · Adjektive #3A8C8C.
- Immer „Plural“/„Singular“ und „Infinitiv“; auf Spielen nur Punkte ●/●●/●●●, keine Niveauangaben.
- Öffentliches Repo: keine Namen, Fotos oder Daten von Schüler:innen.

## Daten, die nur auf dem Gerät liegen
- „Was sagen die meisten?“: Fragen und Antworten stehen im `localStorage` (`rie_meisten_v1`) des Geräts, nicht im Repo. Weitergabe über Export/Import im Spiel (JSON-Datei). Im Repo stehen nur 3 erfundene Beispielfragen.
- Fertiger Satz „Deutschland“ (Liste `FERTIG` in `meisten_tpl.html`): 9 Fragen mit echten Zahlen (Quelle steht an jeder Frage, Stand 12.11.2026) und 7 geschätzte Fragen (`art:"g"`, im Spiel als „geschätzt“ markiert). Neue Umfragen dort ergänzen, Quelle immer mit Jahr.

## Noch offen
- Wort-Comeback für die Leseheft-Wörter (Wortlisten kommen von Frau Rie).
- Ton bei der Lösung.
