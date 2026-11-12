ART={'der':1,'die':1,'das':1}
# Wort-Blitz Blitzlesen – 10 Sets in Listen-Reihenfolge (Wort 1–200) + 3 Verwechslungs-Sets
import os, sys, json


L1 = [("der","a"),("die","a"),("das","a"),("mit",""),("für",""),("und",""),("auf",""),("in",""),("von",""),("zu",""),("ist","v"),("auch",""),("als",""),("ein",""),("nicht",""),("sich",""),("eine",""),("nach",""),("hat","v"),("vor",""),("hier",""),("über",""),("durch",""),("bei",""),("sind","v"),("wie",""),("sie",""),("aber",""),("er",""),("aus",""),("ihr",""),("wieder",""),("wenig",""),("muss","v"),("oder",""),("noch",""),("haben","v"),("viel",""),("werden","v"),("war","v"),("ihm",""),("müssen","v"),("dich",""),("ja",""),("klein",""),("sein","v"),("jetzt",""),("heute",""),("mich",""),("groß",""),("doch",""),("können","v"),("gar",""),("machen","v"),("nein",""),("mehr",""),("kann","v"),("diese",""),("wird","v"),("sehr",""),("links",""),("Junge",""),("was",""),("alle",""),("dein",""),("ihn",""),("kommen","v"),("wo",""),("wann",""),("Frau",""),("hatte","v"),("falsch",""),("immer",""),("mein",""),("spielen","v"),("gehen","v"),("nämlich",""),("welcher",""),("nichts",""),("einmal",""),("dieser",""),("kommt","v"),("richtig",""),("ich",""),("sagen","v"),("hinter",""),("Kind",""),("zwischen",""),("Mann",""),("zurück",""),("damit",""),("unter",""),("Mädchen",""),("halten","v"),("vorne",""),("dass",""),("alt",""),("oben",""),("neu",""),("Tag","")]
L2s = "fliegen dir warten mit |die Blume |das Eis |die Augen |der Ball fangen |das Bett |die Angst es beide hat allein bin |das Brot hier |das Fenster kurz |die Eltern fertig da |der Boden |das Bein ist fallen |der Arm |der Garten |das Ei blau fragen kann |das Geld langsam |die Leute helfen jung |der Bruder laut |die Katze sich richtig |das Mädchen |der Baum lassen holen gleich |der Herr |der Freund |der Kopf |der Junge |der Onkel nein |die Maus rennen mein |der Schuh lieb lachen |der Hund |die Klasse |die Woche sehr nun oben hören |die Schwester legen mir rufen mehr schlafen lesen sprechen unten |der Weg sind singen war sitzen will |die Sonne |der Opa stellen |der Stein suchen |der Tisch tragen |die Tür trinken voll |die Stunde |die Seite wo |der Vogel rot |der Wald soll |das Tier"
L2 = []
for chunk in L2s.split('|'):
    pass
toks = L2s.replace('|', ' | ').split()
i = 0
while i < len(toks):
    if toks[i] == '|': L2.append(toks[i+1] + ' ' + toks[i+2]); i += 3
    else: L2.append(toks[i]); i += 1
assert len(L2) == 100, len(L2)
V2 = set('fliegen warten fangen hat bin ist fallen fragen kann helfen lassen holen rennen lachen hören legen rufen schlafen lesen sprechen sind singen war sitzen will stellen suchen tragen trinken soll'.split())
L2 = [(w, 'v' if w in V2 else ('a' if w.split(' ')[0] in ART and ' ' in w else '')) for w in L2]
L1 = [(w, 'a' if t == 'a' else t) for w, t in L1]

STUFEN = [('●', 'Lies das Wort laut.'), ('●●', 'Sag einen Satz mit dem Wort.'),
          ('●●●', 'Nimm 2 Wörter von deiner Karte. Sag 1 Satz mit beiden Wörtern.')]
STUFEN_V = [('●', 'Lies das Wort laut. Schau genau: Jeder Buchstabe zählt!'), ('●●', 'Zeig ein Wort, das fast gleich aussieht. Lies beide.'),
            ('●●●', 'Sag einen Satz mit beiden Wörtern.')]

SETS = {}
def add(key, sub, words, stufen, schwarz=False):
    assert len(words) == 21 and len({w for w, _ in words}) == 21, key
    SETS[key] = dict(titel=sub, welt='ritual', items=[(w, None) for w, _ in words], typ={w: t for w, t in words},
                     stufen=stufen, schwarz=schwarz)
for li, L, off in ((1, L1, 0), (2, L2, 100)):
    for k in range(5):
        n = (li - 1) * 5 + k + 1
        if k < 4:
            ws = L[21*k:21*k+21]; sub = f'Blitzlesen {n} · Wort {off+21*k+1}–{off+21*k+21}'
        else:
            extra = (['das', 'hier', 'oder', 'über', 'hat'] if li == 1 else ['will', 'sitzen', 'der Opa', 'die Sonne', 'die Woche'])
            d = dict(L); ws = L[84:] + [(w, d[w]) for w in extra]; sub = f'Blitzlesen {n} · Wort {off+85}–{off+100} + 5'
        add(f'Blitzlesen-{n:02d}', sub, ws, STUFEN)
VA = 'das dass was war wo wie die dir dich mich mir mit mein dein nein ein eine ihr ihm ihn ich'.split()
VB = 'sie sich sind sein hat hier kann kommt viel voll vor von soll will auf aus auch und noch nach doch'.split()
VC = ['der Tag', 'das Tier', 'die Tür', 'der Tisch', 'der Mann', 'die Maus', 'das Bein', 'der Baum', 'der Ball', 'das Bett',
      'der Stein', 'die Seite', 'die Sonne', 'lesen', 'legen', 'lassen', 'lachen', 'sitzen', 'singen', 'suchen', 'sagen']
alle = {w for w, _ in L1} | {w for w, _ in L2}
for nm, sub, ws in (('Verwechslung-A', 'Verwechslung A · kleine Wörter', VA), ('Verwechslung-B', 'Verwechslung B · kleine Wörter', VB),
                    ('Verwechslung-C', 'Verwechslung C · Nomen + Verben', VC)):
    miss = [w for w in ws if w not in alle and w.split(' ')[-1] not in alle]; assert not miss, (nm, miss)
    add(nm, sub, [(w, '') for w in ws], STUFEN_V, schwarz=True)

