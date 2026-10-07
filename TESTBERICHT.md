# CATGPT – Der CEO schläft: Testbericht

Stand: 7. Oktober 2026 · Version 0.3.0 · Geprüfte Datei: `catgpt.html`

## Ergebnis

| Prüfung | Ergebnis |
|---|---:|
| Node-Tests für Spielregeln, Dialoggraph und Speicherformat | **157 bestanden, 0 fehlgeschlagen** |
| Chromium-Prüfungen für Oberfläche und Bedienabläufe | **76 bestanden, 0 fehlgeschlagen** |
| Vollständige, deterministisch erzeugte alternative Spielwege | **600 erfolgreich abgeschlossen** |
| Im 600-Wege-Test besuchte Szenen | **57 von 57** |
| Im 600-Wege-Test erreichte unterschiedliche Enden | **4 von 4** |
| Fotos pro geprüftem vollständigem Weg | **22 von 22** |
| Laufzeit-JavaScriptfehler in den Browserprüfungen | **0** |
| Externe HTTP-/HTTPS-Anfragen während der Browserprüfungen | **0** |

Die 600 Spielwege sind **eine zusätzliche Prüfschleife innerhalb der 157 Node-Tests**, nicht 600 zusätzliche unabhängige Testfälle. Ebenso bedeutet „alle Szenen und Enden besucht“ nicht, dass jede mathematisch mögliche Kombination sämtlicher Entscheidungen vollständig aufgezählt wurde.

## Spielregeln und Dialogbaum

Geprüft wurden fünf Kapitel, 57 benannte Szenen, vier Enden und drei Minispiele. Alle Übergangsziele existieren. Der Graph ist zyklenfrei; jede Szene ist strukturell erreichbar. Reguläre Antwortmöglichkeiten, Bedingungen und spätere Rückbezüge wurden mit dem echten Zustandsmodell getestet.

Vier feste, vollständig gespielte Referenzwege erreichen je ein Ende. Zusätzlich durchlaufen 600 reproduzierbar erzeugte Wege mit Seed `63471` unterschiedliche Antworten, Minispielkombinationen und Überspringen. Alle beenden die Geschichte, behalten Werte innerhalb 0–5 und besuchen sämtliche 22 Fotomomente. Korrekte und späte Beweisaufnahme, Anerkennung, Ruhevereinbarung und die Wiederverwendung des selbst gebauten Pitchs sind eigens geprüft.

Die Stichprobe in `results/path-metrics.json` enthält 40–43 Szenen und 36–39 Storyentscheidungen pro Durchlauf. Die ausgegebenen Wortzahlen zählen den besuchten Gesprächsverlauf, nicht sämtliche ungewählten Antwortkarten und Minispieltexte.

**Die ungefähren 20 Minuten sind ein Designziel, keine gemessene oder garantierte Spielzeit.** Eine menschliche Proberunde mit gemessenem Lesetempo, Humorbewertung und Minispieldauer steht noch aus.

## Minispiele

- **Schrank-IT:** Alle sechs möglichen Reihenfolgen, richtige und falsche Lösung, Hinweise, Untersuchung einzelner Gegenstände, unterbrochene Spielstände und einmalige Bonusvergabe.
- **Pitch:** Alle 27 Kombinationen aus Produkt, Zielgruppe und Versprechen; Vorschau ohne vorzeitige Belohnung; Bestätigung nur einmal; tatsächlicher Pitch bleibt in Folgeszenen erhalten.
- **Firewall:** Alle 90 vollständigen Ressourcenfolgen mit je zweimal Stummschalten, KI und Eigenarbeit; Ausgabenlimit, Weckpegel, Feedbackschritt, Wiederaufnahme nach verbrauchter Ressource und optimaler Weg ohne Wecken.

Alle drei Minispiele lassen sich überspringen. Ein ungeschickter oder übersprungener Durchlauf erzeugt keine Sackgasse und erzwingt keinen vollständigen Neustart.

## Speicherung und Robustheit

Geprüft: optionales Speichern, Wiederherstellen durch Ereignis-Replay, Spielstand-Export und gültiger Import, Bestätigung vor Ersetzung, Kapitelneustarts mit vollständiger Rücknahme späterer Wirkungen sowie Fortbestand bereits erlebter Enden.

Ungültiges JSON, unbekannte Ereignisse und Felder, falsche Revisionen, unzulässige Übergänge und beschädigte Daten werden abgelehnt. Importierter Freitext kann keine ausführbaren Antworten einschleusen. Ein abgelehntes Ereignis verändert den bisherigen Zustand nicht. Veraltete Revisionen und doppelte Ausführung vergeben keine doppelten Belohnungen.

Im Browser wurden erfolgreicher, verweigerter, voller, beschädigter und nicht zuverlässig schreibender Speicher nachgebildet. Das Spiel meldet Speicherprobleme statt einen nicht bestätigten Erfolg anzuzeigen. Der alte Chat-Speicherschlüssel wird nicht verändert. Ein tatsächlicher JSON-Dateidownload aus dem Browser wurde ausgelöst und sein Inhalt mit dem Spielstand abgeglichen.

## Oberfläche und Bilder

Ein kompletter Referenzdurchlauf bis zum Mitgründer-Ende wurde in Chromium über echte Bedienelemente einschließlich aller drei Minispiele ausgeführt. Die drei anderen Abschlussansichten wurden zusätzlich aus gültigen, mit dem Produktions-Zustandsmodell erzeugten Spielständen dargestellt. Der Unterschied zwischen diesen Prüfarten ist beabsichtigt: Nicht alle vier Enden wurden nochmals vollständig mit der Maus durchgeklickt.

Weitere Prüfungen: sofort sichtbare Antwortreaktion, Zweigwechsel, Dokumente, Tastenkürzel, Doppelklickschutz, Bestätigungsdialoge, erreichte Kapitel, Größenanpassung, Schriftvergrößerung, Bewegungseinstellung und mobile Profilansicht.

Alle 22 eingebetteten Fotos wurden dekodiert und sind einzeln in der Vergrößerung erreichbar. Suche nach Motiv, numerischem Dateinamen und Originalnummer, Kapitelfilter, Zurück/Vorwärts und Escape wurden geprüft. Original-Nr. 14 und die Datei `1000601355.jpg` fehlen im freigegebenen Bildbestand.

Startansicht bei Breiten **1440, 1280, 1024, 768, 700, 390, 360 und 320 Pixeln**; Storyansicht bei **1440, 768, 390, 360 und 320 Pixeln**. In diesen Prüfungen gab es keinen horizontalen Seitenüberlauf; die Antwortbedienelemente blieben im sichtbaren Bereich. Desktop-, Handy-, Galerie-, Pitch-, Firewall- und Abschluss-Screenshots wurden erzeugt; mehrere davon wurden zusätzlich visuell geprüft.

## Testumgebung und Grenzen

Node.js 22.16.0; Python 3.13.5; Playwright 1.57.0; Chromium 144.0.7559.96 unter Linux.

Die verwaltete Testumgebung blockiert Navigation auf lokale Datei- und HTTP-Adressen. Daher wurde **die unveränderte auszuliefernde HTML-Datei mit Playwright `set_content` geladen**, nicht über eine normale `file://`-Adresse oder eine veröffentlichte Webseite. Speicherfälle verwenden ausdrücklich definierte Speicheradapter. Es wurde kein Anwendungsquelltext für diese Browserprüfungen umgeschrieben.

Nicht separat geprüft: echte iPhones/Android-Geräte, Safari, Firefox, ein Live-Hosting, echte Browser-Speicherung über Neustarts an einer `file://`-Adresse, Screenreader-Kompatibilität sowie eine formale Barrierefreiheits- oder Sicherheitszertifizierung. Die responsive Chromium-Emulation ersetzt diese Prüfungen nicht.

Das Spiel benötigt keine KI-Anbindung. Es wurden keine Live-KI-Antworten geprüft oder simuliert. Kein GitHub-Push und keine Veröffentlichung wurden vorgenommen. Die Zustands- und Importprüfungen sind kein Manipulationsschutz gegen jemanden, der bewusst den lokalen Quelltext verändert.

## Reproduzierbarkeit

`tests/game.test.mjs` prüft die eingebettete Spielengine direkt aus `catgpt.html`; `tests/browser_checks.py` lädt dieselbe Datei. Zuerst die Node-Tests ausführen, damit `results/fixtures/` mit gültigen Referenz-Spielständen erzeugt wird. Browserergebnisse und Fehlerlisten stehen in `results/browser-results.json`; Node-Ergebnisse in `results/node-tests.tap`. Vollständige Ausgaben sind dem Paket beigelegt.
