# CATGPT 0.6 – Prüfbericht

Stand: 8. Oktober 2026. Geprüft wurde die neue mobile Ausgabe vor Veröffentlichung.

## Automatisierte Spielregeln

`npm test`: **64 Tests bestanden**, einschließlich 300 variierter vollständiger Wege. Alle 43 Szenen und vier Enden erreichbar; alle 33 freigegebenen Fotos in den untersuchten vollständigen Wegen vorhanden. Minispiel-Abkürzungen bleiben abschließbar.

Zusätzlich geprüft: verkürzte Einführung, gültige Futtermarken und deren genaue Reaktion, Replay/Export, neue Speichergrenze zu Format 3, eingebettete Quellen und JavaScript-Syntax.

## Browser

`python tests/mobile_v06.py`: **18 Prüfgruppen bestanden**. Normale HTTP-Navigation gegen einen lokalen Server, Desktop-Chromium mit mobilen Viewports.

- Layout und Antwortreaktion bei 320×640, 360×740, 390×844, 430×932, 768×1024 und 1440×960.
- Antwort bleibt am bisherigen Foto; expliziter Wechsel zum nächsten Bild; kein erzwungener Scrollsprung beim getesteten Antwortklick.
- Tatsächlich erzeugtes Audiosignal nach Spielstart, Stummschaltung, getrennte Pegel, Pause/Wiederaufnahme bei simuliertem Sichtbarkeitswechsel.
- Optionales Speichern stellt eine ungelesene Reaktion wieder her; Tonpräferenz bleibt separat erhalten.
- Alter lokaler Spielstand bleibt unangetastet; Import von Format 3 wird ohne Ersetzen des laufenden Spiels abgelehnt.
- Vollständiger Durchlauf über tatsächliche UI-Eingaben: Ball per Zielklick zurückgebracht, Futter als Mousse de Miau präsentiert, Klo gereinigt, Mitgründer-Ende erreicht.
- **Alle 33 unterschiedlichen Fotos wurden dabei im aktuellen Szenenbereich tatsächlich gerendert**, nicht nur im Spielzustand gezählt.
- Andere drei Enden per gültigem Fixture geladen und deren Abschlussdarstellung geprüft.
- Verlauf mit Fotos und konkreter Futtermarke, große Schrift, reduzierte Bewegung und blockierter Speicher.
- Keine JavaScript-Laufzeitfehler in diesen Szenarien.

Maschinenlesbarer Bericht: `results/mobile-v06-results.json`. Aktuelle Screenshots entstehen lokal als `results/v06-*.png` und sind nicht Teil der Website.

## Größe und Grenzen

Die HTML-Datei liegt bei etwa 8,42 MB gegenüber 8,36 MB in 0.5. Audio erzeugt keine zusätzlichen Downloads; Bilder dominieren die Dateigröße.

Nicht durchgeführt: echte iPhone-/Android-Gerätetests, menschlicher Zeit-/Humortest, Hörtest auf Handylautsprechern oder Kopfhörern, vollständige Screenreader-Prüfung und belastbarer Leistungsvergleich unter langsamer Mobilverbindung. Ein messbares Audiosignal beweist keinen angenehmen Klang.

Die allgemeinen Bedienflächen sind groß. Einzelne Zellen des 7×5-Ballspielfelds bleiben auf sehr schmalen Displays kleiner als 44 Pixel. Eine Auswahl bewegt die Figur automatisch zum Ziel; wiederholte präzise Schritt-Eingaben sind nicht mehr nötig. Gleichwertige große Lauftasten erlauben die komplette Bedienung ohne Treffen kleiner Zellen.

Historische Dateien unter `tests/archive/`, ältere Browserberichte und ältere Vorschauen gehören zu früheren Versionen und sind kein Nachweis für 0.6.
