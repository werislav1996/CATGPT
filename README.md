# CATGPT – Ein Kater. Dein Problem.

Version **0.6.1** · 8. Oktober 2026

**[Jetzt spielen](https://werislav1996.github.io/CATGPT/)**

Ted geht an die Börse. Du holst vorher kurz den Ball. Eine absurde Firmenführung mit 33 Katzenfotos, drei Minispielen, vier Enden und einer sehr weichen Geschäftsleitung.

## Was neu ist

- 0.6.1: 32 Bildvorstellungen, zahlreiche Szenen und Antwortreaktionen mit konkreterer Firmensatire überarbeitet. Das Schrankbüro bleibt erhalten; der plumpe E-Mail-Spruch ist entfernt. Spielstände aus 0.6.0 bleiben verwendbar.
- Mobile Szenenansicht: ein Foto im Mittelpunkt, kurze Texte und große Antwortflächen.
- Deine Antwort und Teds Reaktion bleiben am selben Bild. Du öffnest den nächsten Moment bewusst; kein automatisches Scrollen durch einen langen Chat.
- Bildpaare werden nacheinander gezeigt. Ein vollständiger Durchlauf zeigt alle 33 freigegebenen Motive; Original-Nr. 14 bleibt ausgeschlossen.
- Schnellstart ins Unternehmen: Die erste Antwort führt ohne lange Einstellungsrunde zur Firmenführung.
- Neu geschriebene Bildunterschriften und kürzere Dialoge mit absurdem Börsengang, Ball-IT, physischer Firewall und beförderter Lampe.
- Ballspiel: Ziel antippen, automatisch um Möbel laufen, Ball aufnehmen und zurückbringen.
- Futterspiel: Bestellung zusammenstellen und dasselbe Essen als Chefedition, Napf Royal oder Mousse de Miau verkaufen.
- Katzenklo: automatische Eimerentleerung bei Bedarf, Spuren gemeinsam wegfegen und Streu mit einem Schritt ergänzen.
- Synthetische Miau-Musik zur traditionellen Melodie **Bruder Jakob**, instrumentale Zwischenrunden und passende UI-/Spielgeräusche.

## Bedienung

**Ted anschreiben** startet das Spiel und gibt die Audiowiedergabe frei. Ton oben jederzeit ausschalten. Musik und Effekte sind unter dem Zahnrad getrennt regelbar; beim Wechsel in einen anderen Tab pausiert die Musik.

Fotos antippen, um das vollständige Originalmotiv zu sehen. Menü oben links: Gesprächsverlauf, Galerie, Dokumente, Spielwerte, Einstellungen und Kapitelneustart. Der Verlauf ist eine Lesefunktion. Ein Kapitelneustart verlangt eine Bestätigung und setzt spätere Entscheidungen zurück.

Antworten lassen sich auch mit **1–4** wählen. Tab und Enter bedienen Schaltflächen; Pfeiltasten steuern die Spielfigur im fokussierten Ball-Spielfeld. Escape schließt Dialoge. Große Schrift und reduzierte Bewegung sind einstellbar.

Alle Minispiele haben Hinweise und eine bestätigte Abkürzung. Kein Zeitlimit, kein Konto, kein API-Schlüssel, kein Backend. Die Dialoge sind geschrieben; das Spiel verwendet keinen laufenden KI-Dienst.

## Spielstände

**0.6 beginnt eine neue Schicht.** Der verkürzte Einstieg und neue Spielaktionen verwenden Format **4** und `catgpt.game.v4`. Ältere Daten wie `catgpt.game.v3` werden nicht gelöscht oder überschrieben. Alte Exporte sind mit der passenden alten Spielversion verwendbar; sie werden hier verständlich abgelehnt.

Lokales Speichern bleibt freiwillig. Ohne Aktivierung bleibt der Stand im offenen Tab. Export und Import stehen in den Einstellungen bereit. Auch die noch ungelesene Antwortreaktion und die Position innerhalb eines Bildpaars werden mitgesichert. Tonpräferenzen werden unabhängig vom Spielfortschritt unter `catgpt.audio.v1` gespeichert, sofern der Browser das erlaubt.

Bei blockiertem oder vollem Speicher läuft das Spiel weiter; ein Export ist die unabhängige Sicherung.

## Lokal spielen und entwickeln

`catgpt.html` im Browser öffnen. Bilder, Musik und Effekte sind eingebettet beziehungsweise werden lokal synthetisiert. `index.html` ist der relative Einstieg für GitHub Pages. Es gibt keine Laufzeit-Abhängigkeiten oder externen Audiodateien.

Die bestehenden Spielregeln und das Grundgerüst stehen in `catgpt.html`. Die neue Ausgabe hat zusätzliche gepflegte Quellen:

| Datei | Aufgabe |
|---|---|
| `src/mobile.css` | Neue responsive Oberfläche und Minispielgestaltung |
| `src/story.js` | Bildpointen, kürzere Handlung, Antwortvarianten und Endtexte |
| `src/scene-ui.js` | Aktuelle Szene, Reaktionsansicht, Bildfolge, Wegfindung und Audio-Bedienung |
| `src/audio.js` | Bruder-Jakob-Arrangement, synthetische Miau-Stimme und Effekte |
| `scripts/build.mjs` | Bettet diese vier Quellen in die auslieferbare HTML-Datei ein |
| `TASKS.md` | Aufgabenplan mit Umsetzungsstand und offenen Geräte-/Hörtests |

Nach Änderungen unter `src/`:

```sh
npm run build
npm test
```

Unter PowerShell mit gesperrten npm-Skripten gegebenenfalls `npm.cmd` verwenden.

Browserprüfung mit Python und Playwright:

```sh
python tests/mobile_v06.py
```

`CHROMIUM_PATH` kann auf eine installierte Chromium-/Chrome-Datei zeigen. Die Prüfung startet selbst einen lokalen HTTP-Server. Optional eine URL als Argument übergeben, um dieselben Abläufe auf einer veröffentlichten Seite zu prüfen.

## Veröffentlichung und Prüfungen

Änderungen auf `main` werden über GitHub Actions geprüft und als GitHub Pages veröffentlicht. Der Workflow prüft außerdem, dass die eingebetteten Quellen zum Build passen. Ausgeliefert werden nur `index.html`, `catgpt.html` und `.nojekyll`.

Aktuelle Prüfungen und Grenzen stehen in [TESTBERICHT.md](TESTBERICHT.md), Audioherkunft in [AUDIO.md](AUDIO.md). Frühere Tests unter `tests/archive/` und ältere Ergebnisdateien dokumentieren vergangene Versionen; sie sind keine aktuellen Qualitätsnachweise.

Ungefähr 15–20 Minuten sind weiterhin ein Designziel. Ein menschlicher Zeit- und Humortest sowie Hörtests auf realen Handylautsprechern stehen noch aus.
