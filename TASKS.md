# CATGPT – Aufgabenplan für Story, Mobile UI, Minispiele und Audio

Stand: 8. Oktober 2026
Planungsbasis: Repository `werislav1996/CATGPT`, Commit `7d85646`, Spielversion 0.5.0
Status: Version 0.6 umgesetzt, lokal und auf GitHub geprüft und veröffentlicht. Offene Checkboxen kennzeichnen verbleibende Prüfungen oder Detailarbeit, insbesondere echte Mobilgeräte und menschliche Hör-/Spieltests.

## 1. Zielbild

Ein schönes, leicht bedienbares Handyspiel mit Ted als völlig überzeugtem, vollkommen unfähigem Katzen-CEO. Die Fotos tragen die Geschichte. Kurze Dialoge, absurde Aufgaben, gute Reaktionen und passende Geräusche machen daraus einen lebendigen Durchlauf.

**Qualitätsmaßstab:** Das Büro im Kleiderschrank mit dem gelb-blauen Ball als IT-Abteilung. Foto, Behauptung und Aufgabe ergeben zusammen den Witz. Diese Passage erhalten und gezielt verbessern.

**Leitidee:** „Ted bringt seine Firma an die Börse. Du musst vorher kurz aufräumen.“ Ted hat die KI beauftragt, ihn reich zu machen, ohne seinen Tagesablauf zu verändern. Heute findet die große Unternehmensvorführung statt. Ein normaler Katzentag wird als immer absurderes Unternehmen verkauft.

### Verbindliche Anforderungen

- Mobile Bedienung ist die primäre Gestaltungsvorgabe; Desktop bleibt nutzbar.
- Mindestens 30 der 33 freigegebenen Fotos erscheinen in jedem vollständigen normalen Durchlauf direkt in der Handlung. Der geplante Hauptweg verwendet alle 33.
- Bilder dürfen weder korrekte Antworten noch einen Besuch der Galerie voraussetzen.
- Original-Nr. 14 (`1000601355.jpg`) bleibt ausgeschlossen.
- Die Story darf deutlich dümmer, frecher und absurder werden. Ted erklärt seinen Unsinn mit voller Überzeugung.
- Die drei Minispiele Ball, Futter und Katzenklo bleiben erhalten und werden spielerisch sowie visuell überarbeitet.
- Keine erzwungenen Scrollsprünge nach einer Antwort auf dem Handy.
- Musik und UI-Geräusche gehören zum fertigen Spiel; stumm muss es genauso verständlich sein.
- Kein Konto, API-Schlüssel, laufender KI-Dienst oder Backend zum Spielen erforderlich.
- Bestehendes Repository und GitHub Pages weiterverwenden. Arbeitsverzeichnis: `C:\Users\weris\Desktop\CATGPT`.

### Was Erfolg bedeutet

Der Spieler möchte das nächste Foto sehen, versteht jede Aufgabe ohne lange Anleitung und erlebt seine Entscheidungen später wieder. Die Geschichte steigert sich, statt denselben Witz über einen faulen Chef zu wiederholen. Zielspielzeit: ungefähr 15–20 Minuten; erst durch menschliches Probespielen bestätigen.

## 2. Ausgangslage und konkrete Probleme

Die folgenden Punkte wurden am aktuellen Quelltext, an den Fotos und durch das Wiedergeben vorhandener Spielstand-Fixtures geprüft:

| Befund | Folgerung für den Umbau |
|---|---|
| Die vier gespeicherten Endpfade enthalten bereits alle 33 Fotos. | Entscheidend ist die Inszenierung, nicht nur die Bildanzahl im Zustand. |
| Sieben Szenen enthalten jeweils zwei Fotos. | Jedes Motiv bekommt einen eigenen erkennbaren Moment; Paare nur bei einer gemeinsamen Pointe. |
| Die geprüften Endpfade enthalten je 36 Szenen, 32 Antworten, sieben Bestätigungsschritte und 44 Minispielaktionen. | Wiederholungen, unnötige Bestätigungen und monotone Aktionen reduzieren. |
| Auf dem geprüften Weg liegen neun Szenen vor dem ersten Minispiel. | Schneller zum Schrankbüro und zur ersten interaktiven Aufgabe kommen. |
| Anerkennung, Grenzen und Feierabend werden wiederholt verhandelt. | Diese Themen bündeln und Platz für konkrete, bildbezogene Absurdität schaffen. |
| `send()` scrollt bei neuen Verlaufseinträgen wieder automatisch. | Das mobile Verhalten ausdrücklich neu gestalten und durch einen passenden Regressionstest absichern. |
| README und Spiel nennen 0.5.0, `package.json` noch 0.4.0. | Versionsangaben und Dokumentation abgleichen. |
| `npm test` verweist auf ältere Testdateien; daneben existieren neue Core-Tests und alte Vorschau-Skripte. | Testbestand prüfen und einen verlässlichen aktuellen Prüfweg festlegen. |

Die gespeicherten Endpfade sind kein Nachweis dafür, dass jeder mögliche Weg gut funktioniert oder dass ein Foto tatsächlich gelesen wurde. Diese Eigenschaften werden separat geprüft.

## 3. Prioritäten und Arbeitsweise

| Priorität | Bedeutung |
|---|---|
| P0 | Grundlage oder Muss-Kriterium für die neue Version. |
| P1 | Inhalt und Ausarbeitung, die vor Veröffentlichung fertig sein müssen. |
| P2 | Optionale Verfeinerung nach einem vollständig funktionierenden Durchlauf. |

Checkboxen erst nach Umsetzung und erfolgreicher Prüfung abhaken. Zu jedem abgeschlossenen Arbeitspaket kurz Ergebnis, relevante Dateien und Prüfnachweis ergänzen. Eine bestandene technische Prüfung ersetzt keine Beurteilung von Humor oder Spielgefühl.

### Meilensteine und Abhängigkeiten

| Meilenstein | Enthaltene Pakete | Abhängigkeit | Ergebnis |
|---|---|---|---|
| M0 – belastbare Grundlage | A | keine | Aktueller Stand, Tests und Speicherstrategie geklärt. |
| M1 – mobile Musterpassage | B, C, D, E, erste Teile von H | M0 | Schrankbüro bis Ball-Ergebnis mit neuer UI und hörbarem Feedback spielbar. |
| M2 – vollständiger Durchlauf | restliches D, F, G, I | M1 | Alle Kapitel, Bilder, Spiele und Enden zusammenhängend spielbar. |
| M3 – fertige Audiofassung | H vollständig | Audiovorlage geklärt; M1/M2 | Musik, Miau-Motive und Effekte vollständig eingebunden. |
| M4 – geprüfte Veröffentlichung | J, K | M2 und M3 | Neue Version auf GitHub Pages erfolgreich geprüft. |

## 4. A – Grundlage sichern und technische Altlasten prüfen · P0

- [x] **A01** Git-Status, aktuelle Branch und Remote prüfen; fremde lokale Änderungen erhalten.
- [x] **A02** Den Ausgangsstand eindeutig referenzieren und Änderungen in einer eigenen Arbeitsbranch entwickeln.
- [x] **A03** Aktuelle Tests den tatsächlichen Funktionen zuordnen. Alte Slideshow-Tests, Vorschau-Skripte und Scrolltests auf überholte Annahmen prüfen.
- [x] **A04** Einen gültigen Ausgangslauf der aktuellen Core- und Browserprüfungen dokumentieren; vorhandene Fehler getrennt von späteren Regressionen erfassen.
- [ ] **A05** Verwendete CSS-Schichten und UI-Funktionen erfassen. Veraltete Slideshow- und Layoutreste beim Umbau gezielt entfernen.
- [ ] **A06** Ladegröße, erste nutzbare Darstellung und Speicherbedarf auf einem mobilen Testprofil als Vergleichswerte erfassen.
- [x] **A07** Vor Storyänderungen die Spielstandstrategie entscheiden: Migration nur, wenn Ereignisse eindeutig übertragbar sind; sonst neue Speicherversion mit verständlicher Anzeige. Alte Daten nicht löschen oder still überschreiben.

**Abnahme:** Ausgangsversion und bekannte Probleme sind nachvollziehbar. Tests prüfen die aktuelle Spielarchitektur. Der Umbau gefährdet keine vorhandenen Spielstände durch stilles Überschreiben.

## 5. B – Mobile Oberfläche · P0

### Geplanter Bildschirmaufbau

1. Schmale Kopfzeile: Kapitel, Fortschritt, Ton und Menü.
2. Aktuelles Foto: groß genug, damit das für den Witz entscheidende Detail erkennbar ist.
3. Kurzer Dialog und direkte Reaktion.
4. Große Antwortflächen im unteren Bereich.

Galerie, Verlauf, Dokumente und Einstellungen liegen im Menü. Statistiken erscheinen bei relevanten Änderungen kurz und sind ansonsten dort einsehbar.

- [x] **B01** Einheitliche Farben, Abstände, Schriftgrößen, Radien und Buttonzustände definieren; warme dunkle Grundgestaltung beibehalten.
- [x] **B02** Eine mobile Szenenansicht erstellen, die das Foto und die aktuelle Unterhaltung klar priorisiert.
- [x] **B03** Dauerhafte Nebenspalten und Statistiken aus der mobilen Hauptansicht entfernen.
- [x] **B04** Zwei bis drei Antwortflächen als Standard gestalten; vier Abschlussoptionen bei Bedarf zugänglich anbieten.
- [ ] **B05** Bedienflächen mindestens 44 × 44 CSS-Pixel groß machen und ausreichend voneinander trennen.
- [x] **B06** Notch, untere Systemleiste, dynamische Browserleisten und kleine Bildschirmhöhen berücksichtigen.
- [x] **B07** Lange Inhalte innerhalb eines klaren Lesebereichs zugänglich halten. Keine verdeckten Antworten oder verschachtelten Scrollfallen.
- [x] **B08** Fotovergrößerung mit vollständigem Motiv und gut erreichbarem Schließen anbieten. Für Pointen relevante Details nicht wegschneiden.
- [x] **B09** Galerie, Verlauf und Dokumente ohne Verlust der aktuellen Szene öffnen und schließen lassen.
- [x] **B10** Desktop und Tablet aus derselben Struktur ableiten; lesbare Breiten und Bildgrößen begrenzen.
- [x] **B11** Sichtbare Fokuszustände, große Schrift und reduzierte Bewegung berücksichtigen.

**Abnahme:** Bei 320, 360, 390 und 430 Pixel Bildschirmbreite entsteht kein horizontales Scrollen. Foto, Lesetext und Antworten sind zugänglich. Große Schrift funktioniert ohne Überlagerung. Desktop bei 1440 × 960 bleibt sinnvoll bedienbar.

## 6. C – Gesprächsablauf und Navigation · P0

- [x] **C01** Klare Zustände definieren: Szene lesen → antworten → Reaktion lesen → nächste Szene beziehungsweise Aufgabe.
- [x] **C02** Nach der Auswahl die gewählte Antwort und Teds unmittelbare Reaktion beim zugehörigen Foto zeigen.
- [x] **C03** Die nächste Szene nicht vor der Pointe einblenden oder unbemerkt aktivieren.
- [x] **C04** Einen bewussten Übergang anbieten, wenn ein neuer Bildmoment beginnt. Keine zusätzliche Bestätigung, wenn eine eindeutige Navigationsaktion bereits bestätigt wurde.
- [x] **C05** Automatische Scrollsprünge nach Antwortklicks auf Mobilgeräten entfernen; Scrollposition und Lesefokus nachvollziehbar erhalten.
- [x] **C06** Bei langen Reaktionen ein klares Lesesignal beziehungsweise eine explizite Navigation anbieten, statt den Spieler zwangsweise zu verschieben.
- [x] **C07** Fotos, Nachrichten und Reaktionen kurz animieren; keine erzwungene Tippanimation oder künstliche Wartezeit.
- [x] **C08** Doppelklicks, schnelle Mehrfachtipps und veraltete Antworten ohne doppelte Wirkung abfangen.
- [x] **C09** Nach Menüs, Galerie, Wiederaufnahme und Import zur richtigen Szene zurückkehren.
- [x] **C10** Verlauf als Lesefunktion vom bestätigungspflichtigen Kapitelneustart unterscheiden.
- [x] **C11** Tastaturbedienung und verständliche Ansagen für neue Reaktionen erhalten; sichtbare Bedienelemente und Fokus synchron halten.

**Abnahme:** Kein überraschender Wechsel von Bild, Kapitel oder Scrollposition. Jede Antwort hat eine erkennbare Reaktion. Es gibt keine bedeutungslosen doppelten Weiter-Klicks und keinen versteckten Zeitdruck.

## 7. D – Story, Bilder und Humor · P0/P1

### Regeln für das Schreiben

- Ausgangspunkt ist ein wirklich sichtbares Detail im Foto.
- Ted gibt diesem Detail eine völlig übertriebene Unternehmensfunktion.
- Der Mensch darf trocken widersprechen, mitspielen oder den Unsinn steigern.
- Ted bleibt seiner absurden Erklärung treu, auch wenn sie offensichtlich zusammenbricht.
- Eine gute Pointe wird nicht im nächsten Absatz erklärt.
- Kurze warme Momente bleiben möglich; sie führen nicht sofort zurück in eine Vertragsbelehrung.
- Eine Antwort verändert entweder Reaktion, Handlung, späteren Rückbezug oder Ende. Nicht jede lustige Antwort muss eine eigene lange Verzweigung erzeugen.

### Aufgaben

- [x] **D01** Hauptgeschichte und Eskalation der fünf Kapitel ausformulieren.
- [x] **D02** In den ersten zwei bis drei Entscheidungen den Auftrag verständlich machen und zur Firmenführung kommen.
- [x] **D03** Für alle Fotos Bilddetail, Bildunterschrift, Dialog, Antwortreaktionen und möglichen Rückbezug schreiben.
- [x] **D04** Relevante Fotos in den gemeinsamen Hauptweg legen. Verzweigungen verändern überwiegend die Interpretation und Folgen, nicht den Zugang zum Großteil der Bilder.
- [x] **D05** Doppelbilder auflösen, sofern sie keinen gemeinsamen Vorher-nachher-Witz ergeben.
- [x] **D06** Dialoge überwiegend auf zwei bis vier kurze Sätze pro Moment kürzen.
- [x] **D07** Wiederholte Gespräche über Anerkennung, Mitsprache und Feierabend zu wenigen wirksamen Entscheidungen zusammenführen.
- [x] **D08** Mindestens fünf wiederkehrende Witze mit späterer Steigerung ausarbeiten: Ball-IT, Lampe, eigener Stuhl, Chefedition, Teds Abnahme.
- [x] **D09** Antwortmöglichkeiten ebenso pointiert schreiben wie Teds Texte; reine Zustimmung nicht zum Standard machen.
- [x] **D10** Ergebnisdialoge für erfolgreiches Spielen, ungewöhnliche Lösungen und Abkürzungen getrennt schreiben.
- [x] **D11** Humor am Bild prüfen: Würde der Satz unverändert zu fast jedem Katzenfoto passen, braucht er eine konkretere Idee.
- [x] **D12** Einen vollständigen Lesedurchlauf auf Wiederholungen, unnötige Erklärungen und fehlende Übergänge prüfen.

### Foto- und Szenenmatrix

Die folgende Zuordnung ist der geplante gemeinsame Hauptweg. Jede Zeile ist ein eigener Bildmoment; nicht automatisch eine zusätzliche Entscheidungsseite. Die Pointen sind Arbeitsentwürfe.

| Fertig | Kapitel | Nr. / Kennung | Bildmoment und mögliche Pointe |
|---|---|---|---|
| [x] | 1 – Du hast den Job bereits | 2 `judge` | Vorstellungsgespräch: „Du hast die Seite geöffnet. Die Personalabteilung wertet das als Verzweiflung. Du bist eingestellt.“ |
| [x] | 1 | 21 `director` | Vorstand: vier Ämter, eine Katze; jede Pfote verweist auf eine andere Zuständigkeit. |
| [x] | 1 | 12 `alert` | Ted steht beziehungsweise sitzt aufrecht: „Bitte protokollieren. Meine Bewegung für dieses Quartal.“ |
| [x] | 1 | 18 `tilt` | Deine Gehaltsfrage zwingt Ted zu einer neuen Kopfhaltung: „Ich suche den Winkel, aus dem das kostenlos klingt.“ |
| [x] | 2 – Die IT ist weggerollt | 4 `closet` | Schrankbüro, textile Schalldämmung und gelb-blaue IT. Referenzszene erhalten. |
| [x] | 2 | 27 `portfolio` | Spielzeugteam: „Niemand hat einen Abschluss. Drei haben eine Glocke.“ |
| [x] | 2 | 29 `remoteit` | Ball im Außendienst. Möbel werden zur Firewall; daraus entsteht die Rückholaufgabe. |
| [x] | 2 | 17 `mat` | Außenstelle: Ted zeigt dem Stammsitz den Rücken und beantragt Reisekosten. |
| [x] | 2 | 3 `think` | Lampe: „Unsere hellste Mitarbeiterin. Ich habe ihr gekündigt. Sie hat mich schlecht aussehen lassen.“ |
| [x] | 2 | 33 `desk` | Freigabestelle: „Jede Freigabe muss erst unter mir durch.“ Zeitung durch Tastatur ersetzt und dafür einen Digitalisierungspreis beantragt. |
| [x] | 2 | 13 `work` | In Gerätenähe liegen als Leistungsnachweis: Ted beantragt die Urheberschaft am laufenden Rechner. |
| [x] | 2 | 28 `security` | Zugangskontrolle per Katzenblick. Ein Passwort gilt erst, wenn Ted es nicht hören wollte. |
| [x] | 3 – Unbegrenztes Wachstum | 1 `floor` | Zusammenbruch wegen angeblicher Unterversorgung: letzte Mahlzeit vor dramatisch kurzer Zeit. |
| [x] | 3 | 22 `stretch` | Expansion wird in belegter Liegefläche gemessen, nicht in Umsatz. |
| [x] | 3 | 30 `solar` | Solarbetrieb: „Sobald eine Wolke kommt, musst du mich mit einer Taschenlampe motivieren.“ |
| [x] | 3 | 7 `bed` | Strategische Vorbereitung aufs Essen. Ted spart sämtliche Energie für die Beschwerde. |
| [x] | 3 | 20 `duvet` | Blumenmuster wird zur angeblich exklusiven Restaurantausstattung. |
| [x] | 3 | 25 `wellness` | Nach dem Essen tragen die Kissen das Unternehmen; Ted übernimmt die Anerkennung. |
| [x] | 3 | 26 `upsidedown` | „Die Zahlen waren schlecht. Ich habe den Geschäftsführer gedreht. Jetzt geht alles nach oben.“ |
| [x] | 4 – Das Unternehmen hat etwas produziert | 6 `sofa` | Verdauung als einzige laufende Produktionsanlage. |
| [x] | 4 | 10 `nap` | Stand-by der Geschäftsführung; Anfragen bitte an eine wache Körperstelle richten. |
| [x] | 4 | 16 `lounge` | Krisensitzung: Ted beansprucht den gesamten Sitzplatz für die Verantwortung, die er abgibt. |
| [x] | 4 | 11 `chaos` | Reaktion auf den Kostenvoranschlag: Der eigene Output soll plötzlich einen anderen Verursacher haben. |
| [x] | 4 | 34 `approval` | „Ich prüfe mit geschlossenen Augen. So beeinflusst mich das Ergebnis nicht.“ |
| [x] | 4 | 5 `sun` | Pfote am Stoff als Versuch, Besitz und Personal körperlich festzuhalten. |
| [x] | 4 | 31 `marketshare` | Sofabesetzung als feindliche Übernahme; dein Sitzplatz ist die letzte unerschlossene Region. |
| [x] | 4 | 24 `edge` | „Wir stehen kurz vor dem Durchbruch. Das Kissen hat schon nachgegeben.“ |
| [x] | 5 – Die große Vorführung | 15 `boss` | Führungsebene am Kratzbaum: mehr Höhe soll fehlende Kompetenz ersetzen. |
| [x] | 5 | 19 `closeup` | Nahaufnahme als letzter Versuch, sachliche Fragen mit Gesicht zu beantworten. |
| [x] | 5 | 32 `walkover` | „Die Übernahme ist abgeschlossen. Bitte bewege das Unternehmen nicht, ich liege darauf.“ |
| [x] | 5 | 8 `cozy` | Ein kurzer ehrlicher Nähe-Moment, den Ted sofort als unabsichtliches Firmengeheimnis bezeichnet. |
| [x] | 5 | 9 `belly` | Vollständige Offenlegung der Unternehmenssubstanz: ein Bauch. Entscheidung über die Zukunft. |
| [x] | 5 | 23 `paws` | Feierabendpfoten mit individueller Schlusspointe und Rückbezug auf deinen Durchlauf. |

**Abnahme:** Mindestens 30 eindeutige Fotos pro vollständigem Weg, auch bei Abkürzungen. Der Hauptweg nutzt alle 33. Jedes Foto hat einen verständlichen eigenen Auftritt. Ein im Zustand registriertes, aber nie sichtbar präsentiertes Foto zählt nicht als erfülltes Gestaltungsziel.

## 8. E – Ballspiel und vollständige Musterpassage · P0

Die erste vollständig ausgearbeitete Passage umfasst Schrankbüro → Spielzeugteam → verschwundene IT → Ballspiel → Teds Ergebnisreaktion. Sie enthält bereits die neue UI, Übergänge und erste Audioeffekte.

- [x] **E01** Den Raum mit klar unterscheidbarem Menschen, Ted, Möbeln, Ball und Übergabeort gestalten.
- [x] **E02** Freie erreichbare Ziele antippbar machen und den Menschen auf einem gültigen Weg dorthin bewegen lassen; keine Eingabe für jeden einzelnen Schritt verlangen.
- [x] **E03** Hindernisse klar zeigen und unerreichbare Ziele verständlich beantworten.
- [x] **E04** Ballaufnahme und Übergabe kontextabhängig anbieten; nicht ständig mehrere unbenutzbare Buttons zeigen.
- [x] **E05** Kurze Lauf-, Aufnahme- und Rollanimationen mit passenden Geräuschen ergänzen.
- [x] **E06** Ted bei besonderen Ereignissen kommentieren lassen; nicht nach jedem Schritt denselben Spruch abspielen.
- [x] **E07** Karton, Ablage und genau eine freiwillige Extrarunde als unterschiedliche Abschlüsse erhalten.
- [x] **E08** Tastatursteuerung, reduzierte Bewegung und Speichern während der Aufgabe berücksichtigen.
- [x] **E09** Ergebnis und spätere Rückbezüge tatsächlich von deiner Lösung abhängig machen.
- [x] **E10** Die ganze Musterpassage auf kleinem Handyformat mit Ton und stumm durchspielen.

**Abnahme:** Ohne lange Erklärung spielbar. Keine Bewegung durch Möbel, keine doppelte Belohnung und keine Endlosschleife. Die neue Bedienung reduziert monotone Eingaben gegenüber dem Ausgangsstand. Bild, Text, Interaktion und Ton funktionieren zusammen.

## 9. F – Futterspiel: Chefedition · P1

- [x] **F01** Bestellung und aktuelle Zubereitung kompakt gleichzeitig sichtbar machen.
- [x] **F02** Große Karten für Menü und Schale gestalten; Auswahl direkt am Napf zeigen.
- [x] **F03** Befüllen und Wasser mit kurzen Animationen und dezenten Klängen bestätigen.
- [x] **F04** Wiederholte triviale Klicks reduzieren. Spielreiz auf Teds Ansprüche und deine absurde Präsentation verlagern.
- [x] **F05** Nach der Zubereitung eine kleine Auswahl aus übertriebenem Namen, Präsentation oder ehrlicher Servierweise anbieten.
- [x] **F06** Auf die Kombination passend reagieren: Dasselbe Futter wird beispielsweise allein durch das Etikett zur Chefedition.
- [x] **F07** Fehler konkret und lustig kommentieren; bereits getroffene Auswahl erhalten.
- [x] **F08** Abschlussentscheidung und tatsächliches Ergebnis später in der Vorführung aufgreifen.
- [x] **F09** Reine Spielmengen nicht als allgemeine Fütterungsempfehlung darstellen; Bedienoberfläche dabei knapp halten.

**Abnahme:** Die Aufgabe fühlt sich wie eine kleine komische Inszenierung an. Der Napf reagiert sichtbar auf Eingaben. Jede angebotene Präsentationslösung erhält eine passende Reaktion und führt ohne Sackgasse weiter.

## 10. G – Katzenklo: Altlastensanierung · P1

- [x] **G01** Klo, Klumpen und Spuren klar erkennbar und stilisiert darstellen.
- [x] **G02** Werkzeuge mit großen Symbolen und erkennbarem aktiven Zustand gestalten.
- [x] **G03** Wenige unterschiedliche Handlungen statt vieler gleichartiger Einzeltipps vorsehen.
- [x] **G04** Entfernen, Fegen und Auffüllen unmittelbar visuell und akustisch bestätigen.
- [x] **G05** Kapazitätsanzeigen verständlich machen oder unnötige Eimerverwaltung vereinfachen.
- [x] **G06** Falsches Werkzeug humorvoll beantworten, ohne bereits erledigte Arbeit zu löschen.
- [x] **G07** Ted bei der Abnahme zu einer absurden Handlung ansetzen lassen, auf die du reagieren kannst.
- [x] **G08** Dokumentierte Abnahme und „Erst Pfoten abstreifen“ mit eigenen Pointen und Rückbezügen ausarbeiten.
- [x] **G09** Abkürzung anbieten und später ehrlich als vereinfachte Lösung behandeln.

**Abnahme:** Ziele sind auch auf kleinen Bildschirmen treffsicher. Jede Aktion hat eine erkennbare Wirkung. Keine mühselige Wiederholung und keine komplette Zwangswiederholung nach Teds Schlussgag.

## 11. H – Musik, Miau-Motive und UI-Geräusche · P0/P1

### Musikalische Richtung

Gewünscht ist eine alberne Katzen-Miau-Parodie eines bekannteren Liedes mit einer angenehmen instrumentalen Begleitung. Die Miau-Stimme setzt kurze Akzente und lässt beim Lesen Platz. Gewählte Vorlage: **Bruder Jakob – freche Katzenrunde**, vom Nutzer am 8. Oktober 2026 festgelegt. Umsetzung als synthetische Miau-Stimme mit instrumentalen Zwischenrunden.

| Ebene | Verwendung | Charakter |
|---|---|---|
| Ruhige Hintergrundfassung | Lesen und Antworten | Leicht, warm, zurückhaltend; sparsame Miau-Motive. |
| Minispiel-Fassung | Ball, Futter und Katzenklo | Etwas lebhafter, derselbe musikalische Grundcharakter. |
| Erfolgsjingle | Abschluss einer Aufgabe | Kurz und übertrieben feierlich. |
| Schlussmotiv | Bilanz und Ende | Kurzer Abschluss mit passender Miau-Pointe. |
| UI-Effekte | Tippen, Nachricht, Menü, Belohnung | Klar, weich, nicht schrill. |
| Spielgeräusche | Ball, Napf, Schaufel, Besen | Direkt zur sichtbaren Handlung passend. |

- [x] **H01** Konkrete Liedvorlage und Stil für die Miau-Parodie mit dem Nutzer festlegen; Audio-Infrastruktur und UI-Effekte können vorher entstehen.
- [x] **H02** Für die öffentliche Veröffentlichung eine verwendbare Melodie, Bearbeitung und Aufnahme wählen; Herkunft und Nutzungsgrundlage dokumentieren. Keine unklare Originalaufnahme als Platzhalter veröffentlichen.
- [ ] **H03** Einen kurzen Hörentwurf erstellen und als Schleife beurteilen, bevor alle Varianten produziert werden.
- [x] **H04** Ruhige Fassung, Minispiel-Fassung sowie Erfolgs- und Schlussmotive ausarbeiten.
- [x] **H05** Saubere Schleifen ohne Knacken, abrupte Schnitte oder große Lautstärkeunterschiede erstellen.
- [x] **H06** Eine zentrale Audiosteuerung mit getrennten Lautstärken für Musik und Effekte implementieren.
- [x] **H07** Audio über eine bewusste Nutzeraktion starten und abgewiesene Wiedergabe ohne Fehlermeldungskaskade behandeln.
- [x] **H08** Gut sichtbaren Stummschalter und leicht erreichbare Lautstärkeregler anbieten. Tonpräferenzen getrennt vom Spielfortschritt speichern, sofern Browserspeicher verfügbar ist.
- [x] **H09** Musik bei verstecktem Tab pausieren; bei Rückkehr die Stummschaltung respektieren und keine doppelte Wiedergabe starten.
- [x] **H10** Zwischen Lesen, Minispiel und Ende weich wechseln. Gleichzeitige Effekte begrenzen und Mehrfachtipps nicht zu Geräuschlawinen werden lassen.
- [x] **H11** Auswahl-, Nachrichten-, Menü-, Dokument- und Erfolgstöne ergänzen. Dezente UI-Töne können lokal synthetisiert werden.
- [x] **H12** Ballrollen, Aufheben, Napf, Wasser, Schaufel und Fegen an die tatsächlichen Aktionen koppeln.
- [x] **H13** Kurze Ted-Miauer gezielt einsetzen; keine Vollvertonung und kein dauerndes Miauen nach jeder Nachricht.
- [x] **H14** Audio komprimieren und Laden beziehungsweise Decodieren so einbauen, dass der Spielstart bedienbar bleibt.
- [x] **H15** Offline-Nutzung und die Auslieferung über GitHub Pages erhalten. Einbettung in die HTML-Datei bevorzugen, sofern Größe und Ladezeit vertretbar bleiben; bei separaten lokalen Assets die komplette Paketierung und relative Pfade anpassen.
- [x] **H16** Audiodateien, Herkunft, Lautstärkeabstimmung und endgültige Paketgröße dokumentieren.

**Abnahme:** Ton startet nach einer Nutzeraktion, lässt sich sofort abschalten und bleibt nach Szene, Menü oder Wiederaufnahme korrekt eingestellt. Keine überlagerten Musikschleifen. Das ganze Spiel bleibt ohne Ton verständlich. Auf Android Chrome und iOS Safari prüfen; fehlende reale Geräteprüfung ausdrücklich als offen markieren.

## 12. I – Entscheidungen, Enden und Speichern · P1

- [x] **I01** Frühere Entscheidungen gezielt im Finale verwenden: Ballvertrag, Lampe, Arbeitsplatz, Chefedition und Abnahme.
- [x] **I02** Vier vorhandene Endrichtungen erhalten und passend zur neuen Geschichte umschreiben: Mitgründer, Chief Human Officer, gemeinsamer Feierabend, eigener Ausstieg.
- [x] **I03** Enden nicht bloß durch einen unsichtbaren Punktestand bestimmen. Voraussetzungen und angebotene Entscheidung verständlich machen.
- [x] **I04** Schlussbilanz aus tatsächlich ausgeführten Handlungen bilden, einschließlich Abkürzungen.
- [x] **I05** Keine identische Schlussrede mit lediglich ausgetauschtem Endtitel verwenden.
- [x] **I06** Export, Import, Wiederaufnahme und Kapitelneustart an neue Zustände und Aktionen anpassen.
- [x] **I07** Szenenfortschritt, noch ungelesene Reaktion und laufende Minispielaktion nach Wiederaufnahme sinnvoll herstellen.
- [x] **I08** Speicherfehler sichtbar, aber ohne Spielabbruch behandeln. Export als unabhängige Sicherung erhalten.

**Abnahme:** Alle vier Enden sind erreichbar. Rückbezüge behaupten nichts, was im jeweiligen Durchlauf nicht passiert ist. Spielstände werden geprüft; inkompatible ältere Stände verständlich abgelehnt oder nachweislich korrekt migriert.

## 13. J – Qualitätssicherung und Probespiel · P0/P1

### Automatisierbare Prüfungen

- [x] **J01** Storygraph, gültige Übergänge, Enden und Verhalten bei schnellen Mehrfachtipps prüfen.
- [x] **J02** Bildabdeckung für systematisch unterschiedliche Wege einschließlich Minispiel-Abkürzungen prüfen: mindestens 30 eindeutige Fotos, kein ausgeschlossenes Bild.
- [x] **J03** Sichtbare Bilddarstellung getrennt vom Zustand prüfen: geladene Bilder, sinnvolle Abmessungen, zugängliche Vergrößerung.
- [x] **J04** Antwort → Reaktion → Fortsetzung durch echte UI-Eingaben prüfen, ohne den Zustandsautomaten zu umgehen.
- [x] **J05** Mobile Scrollposition, Fokus und Layout nach Antworten, Menüwechseln und Aufgabenabschlüssen absichern.
- [x] **J06** Regeln der drei Minispiele, Fehlerkorrektur und jeweils unterschiedliche Abschlüsse prüfen.
- [x] **J07** Speichern, Import, Export, Wiederaufnahme und inkompatible Stände prüfen.
- [x] **J08** Audiozustände prüfen: Start, Stumm, Lautstärke, Tabwechsel, Szenenwechsel, Wiederaufnahme und fehlgeschlagene Audiofreigabe.
- [x] **J09** JavaScript-Fehler, kaputte Ressourcen und unbeabsichtigte externe Verbindungen ausschließen.
- [x] **J10** Relevante Prüfungen in den tatsächlich ausgeführten `npm test`- beziehungsweise Browser-Testweg aufnehmen.

### Menschliche und gerätebezogene Prüfungen

- [ ] **J11** Einen normalen vollständigen Durchlauf mit frischem Spielstand auf einem Handy spielen.
- [ ] **J12** Zusätzlich eine freche beziehungsweise maximal absurde Antwortfolge und einen Weg mit Abkürzungen prüfen.
- [ ] **J13** Kleine und große Handyformate, Tablet und Desktop ansehen; mindestens ein iPhone und ein Android-Gerät prüfen, soweit verfügbar.
- [ ] **J14** Große Schrift, reduzierte Bewegung, Tastaturbedienung und stummes Spielen prüfen.
- [ ] **J15** Audio über Handylautsprecher und Kopfhörer beurteilen: Verständlichkeit, Lautstärke, Wiederholungen und Ermüdung.
- [ ] **J16** Spielzeit, unnötige Klicks, unklare Aufgaben und übersprungene Bilder protokollieren.
- [ ] **J17** Pointen am sichtbaren Foto beurteilen. Schwache oder austauschbare Sprüche gezielt ersetzen.
- [ ] **J18** Ladezeit und Paketgröße mit dem Ausgangsstand vergleichen und auffällige Verschlechterungen beheben.

**Abnahme:** Keine blockierenden Fehler, verdeckten Pflichtaktionen oder verlorenen Spielstände. Der normale Durchlauf ist ohne Hilfestellung verständlich. Humor, Tempo und Audio wurden tatsächlich beurteilt; nicht verfügbare Geräteprüfungen werden nicht als bestanden ausgegeben.

## 14. K – Dokumentation und Veröffentlichung · P1

- [x] **K01** Spielversion, `package.json`, README und Änderungsprotokoll auf denselben Stand bringen.
- [x] **K02** README auf die bestehende Live-Seite, aktuelle Bedienung, Audiooptionen und Speicherkompatibilität aktualisieren.
- [x] **K03** Fotoverzeichnis und Testbericht aktualisieren; historische Nachweise nicht als aktuelle Prüfung ausgeben.
- [x] **K04** Prüfsummen für die tatsächlich ausgelieferten Dateien aktualisieren.
- [x] **K05** GitHub-Pages-Workflow auf aktuelle Tests und gegebenenfalls zusätzliche Audio-Assets abstimmen.
- [x] **K06** Vollständigen finalen Diff prüfen und Änderungen nachvollziehbar committen.
- [x] **K07** Fertige Version im bestehenden Repository veröffentlichen und erfolgreiches Pages-Deployment abwarten.
- [x] **K08** Auf der öffentlichen URL Spielstart, mobile Antworten, mindestens einen Aufgabenabschluss und Audiosteuerung prüfen.
- [x] **K09** Live-Link, Versionsstand, abgeschlossene Prüfungen und verbleibende Einschränkungen knapp festhalten.

**Abnahme:** `https://werislav1996.github.io/CATGPT/` liefert die geprüfte neue Version. Alle benötigten Dateien sind vorhanden. Lokaler Stand, Dokumentation und veröffentlichte Version passen zusammen.

## 15. Offene Entscheidungen

| Entscheidung | Vorschlag / aktueller Stand | Wann klären? |
|---|---|---|
| Liedvorlage für die Miau-Parodie | **Entschieden: Bruder Jakob**, synthetische Miau-Runde. | Umgesetzt; menschlicher Hörtest offen. |
| Musikalischer Stil | Leichte, alberne Begleitung mit ruhiger Lesefassung und lebhafter Spielvariante. | Zusammen mit dem Hörentwurf. |
| Audiopaketierung | Offline und möglichst weiterhin eine HTML-Datei; Größen- und Ladeprüfung entscheidet über separate lokale Dateien. | Bei H14/H15, vor Anpassung des Deployments. |
| Spielstandwechsel | **Entschieden: Format 4 / catgpt.game.v4.** Ältere Daten bleiben erhalten; Import alter Formate wird erklärt abgelehnt. | A07, vor Änderungen am Ereignismodell. |
| Finale Dialoglänge | Zwei bis vier kurze Sätze als Ausgangspunkt, nach Probespiel anpassen. | Musterpassage und J16/J17. |

## 16. Optionale Verfeinerungen · P2

- [ ] Kleine visuelle Rückbezüge: beförderte Lampe, gesicherter Ball oder Chefetikett im Finale wiederzeigen.
- [ ] Zusätzliche seltene Ted-Kommentare für freiwillige Fehlversuche oder die Extrarunde.
- [ ] Unterschiedliche Schlussjingles pro Ende, sofern die Grundfassung bereits angenehm und performant ist.
- [ ] Dezente dekorative Bewegungen, sofern sie weder Lesbarkeit noch reduzierte Bewegung beeinträchtigen.

Diese Extras ersetzen keine offenen Muss-Kriterien und sollen den Durchlauf nicht künstlich verlängern.

## 17. Fertigstellung der gesamten Version

- [x] Mobile Oberfläche ist einfach, konsistent und schön; Antworten sind mit einem Daumen erreichbar.
- [x] Keine erzwungenen Scrollsprünge nach Antworten.
- [x] Mindestens 30 Fotos pro vollständigem Weg; der gemeinsame Hauptweg zeigt alle 33 mit eigenen Pointen.
- [x] Story steigert sich und greift Entscheidungen wieder auf.
- [x] Alle drei Minispiele sind kurz, verständlich, sichtbar reaktiv und fehlerverzeihend.
- [x] Musik, Miau-Motive und UI-Effekte sind vollständig integriert und abschaltbar.
- [x] Alle vier Enden, Speicherfunktionen und Abkürzungen funktionieren.
- [ ] Technische Prüfungen und ein menschlicher mobiler Probedurchlauf sind dokumentiert.
- [x] GitHub Pages liefert die abschließend geprüfte Version.

## 18. Umsetzungsprotokoll

Hier nur tatsächlich abgeschlossene Arbeiten eintragen.

| Datum | Aufgaben-IDs | Ergebnis / Dateien | Prüfnachweis | Noch offen |
|---|---|---|---|---|
| 08.10.2026 | A–J, K01–K05 | Version 0.6: Szenenansicht, einzeln präsentierte Fotos, kürzere Story, überarbeitete Minispiele, Bruder-Jakob-Musik und Effekte. | 64 Node-Tests einschließlich 300 Pfaden; 18 Browser-Prüfgruppen, vollständiger UI-Durchlauf mit 33 sichtbaren Fotos. | Echte Mobilgeräte und menschliches Probespielen/Hören. |

### Grenzen des aktuellen Nachweises

Nachbesserung 0.6.1: 32 Bildvorstellungen, zahlreiche Szenen und Antwortreaktionen mit stärkerer bildbezogener Firmensatire überarbeitet. Schrankbüro beibehalten, beanstandeten E-Mail-Spruch entfernt. Erneut 64 Spieltests und 18 Browser-Prüfgruppen bestanden; acht Spielstand-Fixtures aus 0.6.0 weiterhin ladbar.

- E10 wurde mit mobiler Chromium-Emulation geprüft, nicht durch Spielen auf einem realen Telefon.
- D11/D12 wurden am Text und den dargestellten Fotos redaktionell geprüft. Ein unabhängiger menschlicher Humor-/Zeittest ist offen.
- H05 ist technisch mit Hüllkurven und Pegelbegrenzung umgesetzt. Ein subjektiver Hörtest bleibt H03/J15.
- B05 bleibt für kleine Spielfeldzellen offen: die allgemeinen Buttons sind groß, das 7×5-Feld hat auf sehr schmalen Displays kleinere Zellen. Zielklicks und automatische Wege reduzieren die erforderliche Präzision. Gleichwertige große Lauftasten erlauben die Bedienung ohne Treffen kleiner Zellen.
- A05/A06 und J18 bleiben offen für eine weitergehende Bereinigung alter CSS-Schichten und echte mobile Leistungsprofile.

### Veröffentlichung

Version 0.6 ist unter https://werislav1996.github.io/CATGPT/ veröffentlicht. Code-Commit: `6cbfd76`. GitHub-Run `37772629041`: Build, 64 Node-Tests, 18 Browser-Prüfgruppen und Pages-Deployment erfolgreich.

Direkt auf der öffentlichen URL zusätzlich geprüft: Version 0.6.0, Einstieg, Audio starten/stummschalten/wiederaufnehmen, Bild- und Antwortwechsel sowie komplette Ballaufgabe über die großen Lauftasten bei 390×844. Keine JavaScript-Fehler.
