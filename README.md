# CATGPT – Der CEO schläft
## Du machst die Arbeit. Ted macht den Eindruck.

Version 0.3.0 · Offline-Story-Spiel · Deutsch

Ted, ein fauler Britisch-Kurzhaar-Kater, ist CEO von CATGPT. Die KI hat Firma, Website, Präsentation und Arbeitsvertrag erstellt. Jetzt fehlt nur noch jemand, der die Arbeit macht: du.

## Spielen

**[Jetzt im Browser spielen](https://werislav1996.github.io/CATGPT/)**

`catgpt.html` im normalen Browser öffnen und **„Schicht beginnen“** wählen. Kein Konto, keine Installation, kein API-Schlüssel und kein Server sind für das Spiel erforderlich. Die Datei enthält Oberfläche, Dialoge, Spielregeln und alle 22 freigegebenen Fotos. Eine reine Dateivorschau führt JavaScript möglicherweise nicht aus; dann die Datei außerhalb der Vorschau im Browser öffnen.

`index.html` ist ein relativer Einstieg zu derselben `catgpt.html`. Der eigentliche Quelltext bleibt in **einer Datei mit gleichbleibendem Namen**. Das Spiel wird aus diesem Repository über GitHub Pages veröffentlicht.

## Veröffentlichung

Änderungen auf `main` werden automatisch mit den 157 Spieltests geprüft und anschließend über GitHub Pages veröffentlicht. Nur `index.html`, `catgpt.html` und `.nojekyll` werden als Website ausgeliefert. Der Workflow kann unter **Actions → Publish game to GitHub Pages** auch manuell gestartet werden.

## Was enthalten ist

Fünf Kapitel, 57 geschriebene Szenen insgesamt und vier mögliche Abschlüsse. In den untersuchten Durchläufen werden etwa 40–43 Szenen und 36–39 Storyentscheidungen durchlaufen, zusätzlich zu den Minispielen. Die Kapitel heißen **Die Einstellung**, **Das Hauptquartier**, **Die Produktidee**, **Die Krise** und **Der Demo Day**.

Antwortkarten ersetzen das alte freie Texteingabefeld. Die Auswahl führt zu festen, vorbereiteten Handlungszweigen. Frühere Forderungen, gesicherte Beweise und Vereinbarungen werden später aufgegriffen. Es ist ein Autorenspiel, kein frei antwortender KI-Chat. Teds Behauptung, alles von KI erledigen zu lassen, gehört zur erfundenen Unternehmensgeschichte.

Die angestrebte Länge beträgt ungefähr **20 Minuten**, abhängig von Lesetempo, Entscheidungen, Galerie und Minispielen. Eine zeitlich gemessene menschliche Proberunde wurde noch nicht durchgeführt. Es gibt keine künstlichen Wartezeiten, keinen verbindlichen Countdown und keinen Zeitdruck beim Lesen.

## Bedienung

- **Antworten:** Eine der zwei bis vier Karten anklicken oder, außerhalb eines Dialogfensters, die entsprechende Ziffer **1–4** drücken. Einzelne Übergänge haben nur eine Weiter-Antwort.
- **Kapitel:** Erreichte Kapitel sind links beziehungsweise im Handy-Menü erreichbar. Ein bestätigter Kapitelneustart stellt den damaligen Anfang wieder her und entfernt spätere Entscheidungen und Belohnungen. Bisher erreichte Enden bleiben in der Übersicht erhalten.
- **Fotoarchiv:** „Beweisfotos“ oder das Bildsymbol öffnen. Alle 22 Fotos sind von Beginn an zugänglich, auch ohne Freischaltung. Nach Motiv, Dateiname oder Originalnummer suchen, nach Kapitel filtern und ein Foto vergrößern. In der Vergrößerung funktionieren Vor/Zurück, die Pfeiltasten und auf geeigneten Touchgeräten Wischgesten. Escape schließt das Fenster.
- **Dokumente:** Gesicherte Beweise und bestätigte Vereinbarungen sind in „Deine Dokumente“ nachlesbar. Das Öffnen allein verleiht keine Vorteile.
- **Darstellung:** Unter „Spiel & Einstellungen“ lassen sich größere Schrift und reduzierte Bewegung einstellen. Auf kleinen Bildschirmen öffnet das Katzensymbol Teds Profil und Werte.

**Teds Wohlwollen**, **Substanz** und **Show** reichen jeweils von 0 bis 5. Sie beeinflussen Verhandlungen und Vorführung. Nicht jede höfliche Antwort ist die beste und nicht jede freche Antwort ist schlecht. Wiederholtes Öffnen von Menüs verändert keine Werte.

## Die drei Minispiele – ohne Lösungsspoiler

**Wo ist hier der Server?** Im Schrankbüro Gegenstände untersuchen und aus den Hinweisen drei Neustart-Schritte zusammensetzen. Die Untersuchungsstellen gibt es als Bildbereiche und beschriftete Schaltflächen. Fehler sind korrigierbar.

**Der Pitch-Baukasten.** Produkt, Zielgruppe und Versprechen aus je drei Karten auswählen. Der vollständige Satz ist vor dem Bestätigen sichtbar. Alle 27 Kombinationen werden ausgewertet. Änderungen vor dem Bestätigen vergeben keine Punkte; der fertige Pitch wird später tatsächlich benutzt.

**Die Nickerchen-Firewall.** Sechs Störungen bearbeiten. Stummschalten, an die KI delegieren und selbst erledigen stehen jeweils nur zweimal zur Verfügung. Der Weckpegel ist ein Spielelement, kein Timer. Eine schlechte Entscheidung führt zu einer anderen Reaktion, nicht zum Neustart der Geschichte.

Jedes Minispiel bietet Hinweise und eine bestätigungspflichtige Möglichkeit zum Überspringen. Überspringen führt zu einer improvisierten Lösung ohne vollständigen Erfolgsbonus; die Schicht bleibt abschließbar.

## Spielstand sichern

Dauerhaftes Speichern ist zunächst **ausgeschaltet**. Ohne Aktivierung bleibt der Fortschritt im geöffneten Tab. Die Option **„Spielstand auf diesem Gerät speichern“** verwendet den eigenen Browserspeicher-Schlüssel `catgpt.game.v1`. Der frühere Chat-Speicher `catgpt.v1.local` wird nicht geändert oder entfernt.

Unter „Spiel & Einstellungen“ stehen **Spielstand exportieren** und **Spielstand importieren** zur Verfügung. Der JSON-Export enthält Entscheidungen, Minispielaktionen und die Liste bereits erlebter Enden, nicht die eingebetteten Fotos. Ein Import wird auf gültige Spielereignisse geprüft und erst nach Bestätigung übernommen. Die JSON-Datei nicht manuell bearbeiten. Die Text-Bilanz am Schluss ist eine separate Lesefassung, kein importierbarer Spielstand.

Bei direkt geöffneten Dateien oder eingeschränktem Browserspeicher kann dauerhaftes Speichern nicht verfügbar sein. Das Spiel zeigt dann eine Warnung, läuft im Tab aber weiter. **Vor einem Browserwechsel, Umbenennen/Verschieben der HTML-Datei oder Ersetzen durch eine neue Version den Spielstand exportieren.** Das ist auch die unabhängige Sicherung, wenn der Browser seine Daten löscht.

## Fotos und Geschichte

22 freigegebene Fotos sind eingebettet. Die alten Originalnummern bleiben erhalten; **Nr. 14 (`1000601355.jpg`) bleibt ausgeschlossen**. Alle 22 Motive besitzen einen festen Storymoment; die geprüften vollständigen Wege besuchten alle 22. Das Archiv ist unabhängig davon vollständig erreichbar. Die Motive stammen aus den bereitgestellten Fotos, die Datei verwendet bereits optimierte Bildkopien.

Ted ist die einzige Figur mit Katzenidentität. Unternehmensgeschichte, Titel, gespielte Stimmung und Bildunterschriften sind Satire und keine Tatsachenbehauptungen über sein wirkliches Verhalten.

## Quelltext ändern – Suchanker in catgpt.html

| Suchanker | Inhalt |
|---|---|
| `CATGPT_DESIGN` | Farben, Layout, mobile Darstellung und Lesbarkeit |
| `CATGPT_FOTOS` | Eingebettete Bilddaten und Originalnummern |
| `CATGPT_CONFIG` | Version, Speichergrenzen und Grundkonfiguration |
| `CATGPT_GAME_STORY` | Geschriebene Szenen, Auswahlmöglichkeiten und Rückbezüge |
| `CATGPT_GAME_STATE` | Zustandsänderungen, gültige Ereignisse, Replay und Checkpoints |
| `CATGPT_GAME_MINIGAMES` | Regeln und Auswertung der drei Spiele |
| `CATGPT_GAME_ENDINGS` | Endeauswahl und Abschlussdaten; enthält Spoiler |
| `CATGPT_RENDERING` | Nachrichten, Antwortkarten, Spieloberflächen und Status |
| `CATGPT_CHAT_FLOW` | Wechsel zwischen Szenen und Schutz vor doppelten Klicks |
| `CATGPT_GALLERY` | Archiv, Suche, Filter und Vergrößerung |
| `CATGPT_LOCAL_STORAGE` | Laden, Speichern, JSON-Import und Export |
| `CATGPT_EVENTS_ACCESSIBILITY` | Tastatur, Fokus, Dialoge und Bedienereignisse |

Es gibt keine Laufzeit-Abhängigkeiten. Das alte optionale KI-Backend gehört **nicht** zu diesem Spielpaket. Die Spielseite nimmt keine API-Verbindungen auf und fordert keinen Schlüssel an.

## Tests erneut ausführen

Zum Spielen werden diese Werkzeuge nicht benötigt. Die Tests wurden mit Node.js **22.16.0**, Python **3.13.5**, Playwright **1.57.0** und Chromium **144.0.7559.96** durchgeführt.

Aus diesem Verzeichnis:

```sh
node --test tests/game.test.mjs
```

Das erzeugt auch die gültigen Spielstand-Fixtures für die Browserprüfungen. Für diese benötigt Python das Paket `playwright` und eine lokale Chromium-Installation. `CHROMIUM_PATH` kann auf die ausführbare Browserdatei gesetzt werden:

```sh
python tests/browser_checks.py
```

Die Browserprüfungen laden die unveränderte HTML-Datei als Testdokument mit `set_content` und ersetzen für Speicherfälle die Storage-Schnittstelle durch ausdrücklich definierte Testadapter. Sie sind kein Test einer veröffentlichten Seite. `TESTBERICHT.md` dokumentiert Umfang und Grenzen; `results/` enthält die ausgeführten Prüfungen. **Tests und Spielstand-Fixtures enthalten Handlungsspoiler.**
