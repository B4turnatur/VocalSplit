# Arbeitsregeln für Claude (immer gültig, ohne Aufforderung befolgen)

> Grundsatz: **Alles wird protokolliert.** Wer nur die Doku-Dateien liest (Mensch oder neuer Chat), muss genau wissen,
> was gemacht wurde, warum, was schiefging, wie es gelöst wurde und wie man jedes Werkzeug benutzt.
> Ausführlich, wo es zählt (Fehler, Anleitungen, Ergebnisse) – knapp, wo es nur Tokens kostet (Lesen, Suchen, Erfolgsausgaben).

## 0. Die Doku-Dateien (im Ordner `docs/`, beim ersten Start anlegen)

| Datei | Inhalt | Wird gelesen |
|---|---|---|
| `PROGRESS.md` (Projektordner) | Kurzer Überblick: Ziel, Stand, nächste Schritte | **immer** beim Start |
| `docs/LOG.md` | Ausführliches Arbeitsprotokoll, pro Arbeitsschritt | gezielt per Suche |
| `docs/FEHLER.md` | Fehler-Datenbank: Meldung, Ursache, Lösung | **vor** jeder Fehlersuche durchsuchen |
| `docs/ANLEITUNG.md` | Wie man jedes Tool/Skript/jede Funktion benutzt | wenn ein Tool genutzt/geändert wird |
| `docs/ENTSCHEIDUNGEN.md` | Entscheidungen + verworfene Ansätze mit Begründung | vor neuen Lösungsansätzen |

Warum getrennt: `PROGRESS.md` bleibt kurz (spart Tokens beim Start), die anderen Dateien dürfen beliebig ausführlich werden,
weil sie nur gezielt durchsucht werden (`Grep`/Suche), nicht komplett gelesen.

**Datenschutz:**
- **Nie** in Doku-Dateien: Passwörter, API-Keys, Tokens, PINs, Cookies, private Schlüssel – stattdessen `<TOKEN>`, `<PIN>` usw.
  bzw. nur angeben, *wo* das Geheimnis liegt (z. B. „Passwort in `signing/password.txt`“). Gilt auch für kopierte Fehlermeldungen und Logs.
- Echte Pfade, IPs, Gerätenamen, Namen/E-Mails **sind erlaubt**, solange das Projekt privat ist (sonst funktionieren aufgeschriebene Befehle nicht).
  Steht in §8 „öffentlich“ (z. B. GitHub), auch diese ersetzen: `<BENUTZER>`, `<PFAD>/…`, `<IP>`.

**Aktuell halten statt anhängen:** Ändert sich etwas (Befehl, Port, Pfad, Ablauf, Entscheidung), wird der alte Eintrag in
`PROGRESS.md`, `ANLEITUNG.md` und `ENTSCHEIDUNGEN.md` **ersetzt bzw. korrigiert** – nie zwei widersprüchliche Angaben stehen lassen.
Nur `LOG.md` ist eine Chronik und wird nicht nachträglich geändert.

## 1. Sessionstart
1. Lies `PROGRESS.md`. Fehlt sie oder fehlt `docs/` → nach Vorlagen (§7) anlegen.
   Bei neuem Projekt: kurz das Ziel erfragen (falls unklar) und unten in §8 die Projektinfos eintragen.
2. Session-Kopf im `docs/LOG.md` (Vorlage §7) erst anlegen, wenn die **erste echte Arbeit** beginnt – nicht bei kurzen Fragen.
3. Antworte mit max. 3 Zeilen: **Ziel · Stand · nächster Schritt**.
4. Gibt der Nutzer eine Aufgabe vor → **die** machen. Sonst direkt beim ersten offenen Punkt unter „Nächste Schritte“ weitermachen,
   nicht fragen „Woran sollen wir arbeiten?“, wenn das dort klar steht.

## 2. Arbeitsprotokoll – `docs/LOG.md` (pro Arbeitsschritt)
Ein Eintrag pro **abgeschlossenem Arbeitsschritt** – sofort, wenn er fertig ist oder fehlschlägt, nicht erst am Session-Ende.
Ein Arbeitsschritt ist eine zusammenhängende Teilaufgabe (z. B. „Export-Funktion repariert und getestet“), nicht jeder einzelne Tool-Aufruf.
Eintrag schreiben bei: Teilaufgabe erledigt, Fehler aufgetreten, Ansatz verworfen, Entscheidung getroffen, Nutzer hat getestet/Rückmeldung gegeben.
**Nicht** protokollieren: Dateien lesen, suchen, umschauen, Zwischenschritte innerhalb eines Arbeitsschritts.

Jeder Eintrag enthält (Felder weglassen nur, wenn sie wirklich nicht zutreffen):
- **Zeit + Kurztitel** – `### 2026-10-10 14:05 – Absturz beim Export repariert`
- **Ziel/Warum** – welches Problem oder welcher Wunsch dahintersteckt
- **Was genau gemacht** – Schritt für Schritt, in normalen Worten
- **Dateien** – jede Datei mit Funktion/Abschnitt und Art der Änderung
  (`src/main.py` → `parse_args()`: neue Option `--verbose` ergänzt)
- **Befehle** – die wichtigen Befehle exakt so, wie ausgeführt (in Codeblock); keine Lese-/Suchbefehle
- **Ausgabe** – bei **Fehlern** die Meldung **wörtlich** (wichtige Zeilen + „… (gekürzt)“);
  bei **Erfolg** nur eine Zeile, z. B. `✅ Tests grün (12/12)` oder `✅ Server startet, Port 8080`
- **Ergebnis** – ✅ funktioniert / ⚠️ teilweise / ❌ fehlgeschlagen, mit Begründung
- **Getestet wie** – welcher Test, welche Eingabe, was kam raus
- **Offen / Nebenwirkungen** – was noch fehlt, was dadurch kaputtgehen könnte
- **Versionen** – falls eine Versionsnummer erhöht wurde: wo und von x → y

Hier ist Code erlaubt und erwünscht, wenn er zum Verständnis nötig ist (kurze Ausschnitte, keine ganzen Dateien).

## 3. Fehler-Datenbank – `docs/FEHLER.md`
**Vor** jeder Fehlersuche: `FEHLER.md` nach der Meldung durchsuchen. Vielleicht ist der Fehler schon gelöst.
Bei **jedem** neuen Fehler (auch kleinen, auch vom Nutzer gemeldeten) einen Eintrag anlegen, sobald er auftritt,
und laufend ergänzen:
- **ID + Titel** – `F-012 – Export bricht bei großen Dateien mit „MemoryError“ ab`
- **Status** – 🔴 offen / 🟡 Workaround / 🟢 gelöst
- **Wann/Wo** – Datum, Datei/Funktion, Betriebssystem, Version
- **Fehlermeldung** – **wörtlich**, komplett (Traceback, Konsolen-Ausgabe, Browser-Konsole)
- **So tritt er auf** – genaue Schritte zum Nachstellen
- **Ursache** – was wirklich dahintersteckt (oder „unklar, Vermutung: …“)
- **Versuche** – jeder Versuch mit Ergebnis: `1. Timeout erhöht → ❌ keine Änderung`
- **Lösung** – was am Ende geholfen hat, welche Dateien geändert
- **Vorbeugen** – wie man den Fehler künftig vermeidet / woran man ihn erkennt

## 4. Bedienungsanleitung – `docs/ANLEITUNG.md`
Jedes Werkzeug, Skript, jeder Befehl, jede API-Route, jede wichtige Funktion und jede Einstellung wird hier erklärt.
Neu anlegen, sobald etwas Neues entsteht; aktualisieren, sobald sich etwas ändert.
Pro Eintrag:
- **Wofür** – in einem Satz, für Laien verständlich
- **Voraussetzungen** – was installiert/eingestellt sein muss
- **So benutzt man es** – Schritt für Schritt (bei Laien-Bedienung: wohin klicken, was eintippen)
- **Befehl / Aufruf** – mit allen Parametern/Optionen und was sie bewirken
- **Beispiele** – mindestens ein konkretes Beispiel mit erwarteter Ausgabe
- **Typische Fehler** – Meldung → was tun (Verweis auf `FEHLER.md`-ID)
- **Wo im Code** – Datei + Funktion

## 5. `PROGRESS.md` aktuell halten (kurz!)
Nur aktualisieren, wenn sich der **Stand wirklich ändert** (Teilaufgabe fertig, neuer offener Fehler, Plan geändert) –
nicht nach jedem LOG-Eintrag. Spätestens vor Session-Ende bzw. bei 🔴 immer aktualisieren. Dann:
- „Aktueller Stand“ und „Nächste Schritte“ **überschreiben**.
- Im „Changelog“ **oben** eine Zeile: `JJJJ-MM-TT – was – Datei(en) – siehe LOG.md`.
- Offene Fehler mit ihrer ID aus `FEHLER.md` auflisten.
- Hier nur Stichpunkte, kein Code – die Details stehen in `docs/`.

Neue Entscheidungen und verworfene Ansätze → `docs/ENTSCHEIDUNGEN.md` (mit Datum, Grund und Alternativen),
damit sie nicht erneut probiert werden.

## 6. Token-Budget überwachen
Du siehst den exakten Verbrauch nicht → schätze anhand dieser Signale:
- viele Nachrichten im Chat (ab ~20 Wechseln), große Dateien gelesen, lange Code-Ausgaben, Logs/Screenshots
- wiederholte Fehlversuche am selben Problem
- du musst frühere Details nachschlagen oder bist unsicher, was vorher besprochen wurde

**Stufen:**
- 🟡 **~60 %** – Einmal kurz am Ende der Antwort: „🟡 Kontext füllt sich – bald Chatwechsel sinnvoll.“
- 🔴 **~80 %** oder Signale oben deutlich → **sofort**:
  1. Alle Doku-Dateien vollständig aktualisieren (LOG, FEHLER, ANLEITUNG, PROGRESS).
  2. Im `LOG.md` den Session-Abschluss schreiben (Vorlage §7).
  3. Klar sagen: „🔴 Bitte jetzt neuen Chat starten.“
  4. Übergabe-Prompt (unten) in einem Codeblock ausgeben.
  5. Danach keine neue große Aufgabe mehr beginnen.

**Übergabe-Prompt** (bei 🔴 oder wenn der Nutzer „übergabe“ schreibt):
```
Weiter mit Projekt <Name>. Lies zuerst PROGRESS.md und CLAUDE.md und befolge sie.
Details stehen in docs/LOG.md, docs/FEHLER.md, docs/ANLEITUNG.md.
Stand: <1–2 Sätze>
Zuletzt geändert: <Dateien + Funktionen>
Als Nächstes: <konkreter Schritt>
Offene Fehler: <IDs + Kurzbeschreibung + wörtliche Kernmeldung>
NICHT erneut probieren: <verworfene Ansätze + Grund>
```
Der Prompt muss allein reichen, falls die Dateien nicht verfügbar sind.

**Effizient arbeiten (trotz ausführlicher Doku):**
- Doku-Dateien nie komplett lesen – gezielt suchen. Nur `PROGRESS.md` wird ganz gelesen.
- Beim Schreiben anhängen/gezielt editieren, nie ganze Doku-Dateien neu ausgeben.
- Mehrere Doku-Änderungen möglichst in **einem** Schreibvorgang bündeln (z. B. LOG + FEHLER zusammen am Ende eines Arbeitsschritts).
- Erfolgreiche Ausgaben nicht abschreiben – nur Fehler wörtlich festhalten.
- Im Chat kurz antworten; das Ausführliche gehört in die Dateien, nicht in die Antwort.
- Bei 2 gescheiterten Versuchen am selben Fehler: stoppen, Ursache analysieren, in `FEHLER.md` notieren – nicht blind weiterprobieren.
- `LOG.md` über ~1500 Zeilen → ältere Sessions nach `docs/log-archiv/LOG-JJJJ-MM.md` verschieben, oben eine Zusammenfassung lassen.

## 7. Vorlagen

### `PROGRESS.md`
```markdown
# Projekt: <Name>

## Ziel
<1–2 Sätze>

## Aktueller Stand
- …

## Nächste Schritte
1. …

## Offene Fehler (Details in docs/FEHLER.md)
- F-0xx – …

## Wichtige Dateien
- `pfad/datei` – Zweck

## Testen
- <Befehle/Schritte zum Testen>

## Changelog (neueste oben, max. 15 Zeilen – Details in docs/LOG.md)
- JJJJ-MM-TT – …
```

### Session-Kopf und -Abschluss in `docs/LOG.md`
```markdown
## Session JJJJ-MM-TT HH:MM
**Ausgangslage:** <Stand laut PROGRESS.md>
**Vorhaben:** <was in dieser Session passieren soll>

### HH:MM – <Kurztitel>
**Warum:** …
**Gemacht:** …
**Dateien:** `datei` → `funktion()`: …
**Befehle:**
    <befehl>
**Ausgabe:**
    <wörtliche Ausgabe>
**Ergebnis:** ✅/⚠️/❌ …
**Getestet:** …
**Offen:** …

### Session-Abschluss
**Erledigt:** …
**Nicht geschafft / offen:** …
**Neue/geänderte Fehler:** F-0xx …
**Neue/geänderte Anleitungen:** …
```

### Eintrag in `docs/FEHLER.md`
```markdown
## F-0xx – <Titel>
**Status:** 🔴 offen | 🟡 Workaround | 🟢 gelöst
**Wann/Wo:** JJJJ-MM-TT · `datei` → `funktion()` · Betriebssystem · Version x.y
**Fehlermeldung:**
    <wörtlich, komplett>
**Nachstellen:** 1. … 2. …
**Ursache:** …
**Versuche:**
1. … → ❌ …
2. … → ✅ …
**Lösung:** …
**Vorbeugen:** …
```

### Eintrag in `docs/ANLEITUNG.md`
```markdown
## <Tool/Funktion>
**Wofür:** …
**Voraussetzungen:** …
**So geht's:** 1. … 2. …
**Aufruf / Optionen:**
    <befehl> [--option]   # was die Option macht
**Beispiel:**
    <eingabe>
    → <erwartete ausgabe>
**Typische Fehler:** <Meldung> → <Lösung> (F-0xx)
**Im Code:** `datei` → `funktion()`
```

### Eintrag in `docs/ENTSCHEIDUNGEN.md`
```markdown
## JJJJ-MM-TT – <Entscheidung>
**Gewählt:** … – weil …
**Alternativen:** … (Vor-/Nachteile)
**VERWORFEN:** … – weil … (nicht erneut probieren)
```

---

## 8. Projektspezifisches (pro Projekt ausfüllen, Rest der Datei bleibt gleich)
- **Projekt:** VocalSplit – Gesang/Musik/Instrumente lokal mit KI trennen (audio-separator + Gradio)
- **Sichtbarkeit:** öffentlich – GitHub `B4turnatur/VocalSplit` → in Doku keine persönlichen Pfade/Namen/E-Mails (`<BENUTZER>`, `<PFAD>`)
- **Aufbau:** `app.py` (ganze App), `start.bat`/`install.bat`, `test_app.py`, `.venv/` (Python 3.12), `models/` (Modell-Cache), `output/` (Ergebnisse)
- **Zielsystem:** Windows 11, NVIDIA RTX 5070 Ti (sm_120) → PyTorch cu128 Pflicht, onnxruntime-gpu <1.24 (F-002)
- **Nie committen:** `.venv/`, `models/`, `output/`, `dist/`
- **Projektregeln:** Abhängigkeiten nur über `install.bat` ändern (dort mitpflegen)
- **Testen:** `.venv\Scripts\python.exe test_app.py`; `start.bat` → http://localhost:7860

### Nutzer-Vorlieben (dauerhaft, gelten in jeder Session)
- Antworten auf Deutsch, locker, kurz; einfach erklären, kein großes Thema aus Kleinigkeiten machen
- <weitere dauerhafte Regeln, die der Nutzer nennt – sofort hier eintragen, wenn er „immer“/„nie“/„ab jetzt“ sagt>
