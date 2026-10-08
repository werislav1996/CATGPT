# CATGPT 0.5.0 – Testbericht

Stand: 8. Oktober 2026. Geprüfte Datei: `catgpt.html`.

SHA-256: `9547d680a5875b418efd3979012b3e5325253c140bb6f2aed3d1f8e0383020b0`

## Tatsächlich ausgeführte Prüfungen

| Bereich | Ergebnis | Methode |
|---|---:|---|
| Kernlogik | **56 / 56 bestanden** | Native Node-Tests gegen das unveränderte `gameCore`-Skript aus der fertigen HTML-Datei. |
| Browser | **70 / 70 bestanden** | Chromium, vollständige HTML-Datei via `set_content`; tatsächliche Klicks, Tasten, Import und Export. |
| Pfadprüfung | **300 vollständige Wege** | Deterministische variierte Entscheidungen, unterschiedliche Spielausgänge und Abkürzungen. |
| Abdeckung dieser Testwege | **44 Szenen, 4 Enden** | Alle geschriebenen Szenen und alle Enden in der Gesamtheit der Wege erreicht. |
| Fotos | **33 / 33** | Archivbilder im Browser decodiert; eingebettete Bilddaten mit 0.4 verglichen. |
| Ausschluss | **Nr. 14 nicht vorhanden** | Nummer, Dateiname, Fotoliste und Suchergebnis kontrolliert. |

Die 300 Wege sind Teil der Logikprüfung, keine 300 menschlichen Spieltests. Auf diesen Wegen kamen jeweils alle 33 freigegebenen Fotos vor. 28–32 Storyentscheidungen pro Weg; 2487–2800 Wörter im erzeugten Gesprächsprotokoll, ohne vollständige Zählung aller Auswahl- und Spieltexte. Daraus wird keine gemessene Dauer abgeleitet.

## Gesprächsfluss

Geprüft wurden die spezifische Reaktion auf die Auswahl, die erhaltene eigene Nachricht, das Sichtbarbleiben der direkten Antwort auf Desktop und Handy, echte Introverzweigungen, später aufgegriffene Abmachungen und Dokumente. Ein Kapitelende wartet auf Bestätigung; selbst nach Wartezeit wird der neue Auftrag nicht automatisch geladen. Nach Spielabschluss steht zunächst das Ergebnis, ebenfalls ohne unmittelbaren Sprung. Alte oder doppelte Klicks können nicht den nächsten Dialog auswählen oder Belohnungen doppelt vergeben.

## Minispiele

Ball: Kollisionen, erreichbare Route, korrektes Aufnehmen und Zurückbringen, freiwillige einzelne Extrarunde, Kartonlösung, Ergebniskommentar.

Futter: falsche Bestellung mit konkreter Rückmeldung, Grenzen der Portionsauswahl, Wasser, richtige Bestellung, danach verschiedene Reaktionen auf selbstständiges Gehen bzw. Chefedition.

Katzenklo: passende Werkzeuge, leere Felder, Eimerkapazität, fünf Klumpen und vier Spuren, Streu ergänzen, Abschlussbedingungen und eigene Abnahmeentscheidung. Zusätzliche Regressionstests verhindern, dass eine übersprungene Aufgabe im Folgedialog als eine tatsächlich ausgeführte Handlung beschrieben wird.

Alle drei Spiele lassen sich nach Rückfrage vereinfacht abschließen; dieser Status wird in Ergebnis und Endbilanz beibehalten. Kein notwendiger Neustart nach einem Fehler.

## Speicherung und Bedienung

Einwilligung, Wiederladen per Aktionswiedergabe, Exportdatei, bestätigter Import, Ablehnung älterer Formate, beschädigte Daten, verweigerter Speicher und fehlgeschlagener Schreibversuch wurden geprüft. Der vorherige Schlüssel bleibt unberührt. Kapitelneustarts verwerfen spätere Konsequenzen und produzieren keine doppelten Zustandsboni.

Layouts: 320×740, 360×780, 390×844, 768×1024, 1024×768, 1440×940 und 844×390 CSS-Pixel, jeweils zusätzlich große Schrift. Keine festgestellte horizontale Seitenüberbreite. Schaltflächen bleiben per Scrollen erreichbar. Tastaturantworten, fokussierte Raum-Pfeilsteuerung, Galerie-Navigation und Dialogschließen wurden ausgeführt.

Keine ungefangenen JavaScript-Fehler und keine HTTP-Anfragen in den geprüften Abläufen. Separate Bildprüfung: Die gesamten eingebetteten Assets sind unverändert gegenüber der vorherigen Ausgabe; die Originaluploads wurden nicht neu bearbeitet.

## Sichtprüfung

Desktop-Chat mit Auswahl und unmittelbarer Ted-Reaktion, Schrankbüro mit Fotoanhang, Desktop-Ballspiel sowie mobile Chat-, Futter- und Katzenklo-Ansichten wurden als Screenshots kontrolliert. Screenshots sind echte gerenderte Ansichten, keine Design-Mockups. Nicht jede der möglichen Dialogkombinationen wurde einzeln visuell gelesen.

## Grenzen

Direkte `file://`-Navigation wurde in dieser verwalteten Testumgebung mit `ERR_BLOCKED_BY_ADMINISTRATOR` blockiert. Daher liefen die Browserprüfungen mit dem vollständigen, unveränderten HTML-Inhalt als Testdokument. Speicherzugriffe wurden durch ausdrücklich eingerichtete, funktionierende bzw. verweigernde Adapter nachgebildet. Das prüft Anwendungslogik, aber garantiert nicht das Verhalten jeder lokalen Dateiablage oder Browserrichtlinie.

Keine Prüfung einer veröffentlichten Website, kein GitHub-Push, keine echten Mobilgeräte und keine Safari-/Firefox-Prüfung. Chromium-Mobilansichten sind Viewportprüfungen, kein Ersatz für Tests auf realen Telefonen.

Keine laufende KI, deshalb keine Live-KI-Prüfung erforderlich. Ein menschlich gemessener vollständiger Durchlauf und ein Nutzertest zur Humorwirkung stehen aus. Ungefähr 20 Minuten sind weiterhin ein Designziel. Dass jede Person über jede Pointe lacht, ist keine testbare Zusage.

## Reproduzierbare Nachweise

`results/node-tests.tap`, `results/browser-results.json`, `results/browser-tests.log`, `results/path-metrics.json`, `results/asset-audit.json`, die Spielstand-Fixtures und die beiden Testdateien liegen im Paket. Die Testdaten enthalten ausschließlich fiktive Spielentscheidungen.

Getestete Umgebung: Node.js 22.16.0; Python-Playwright 1.57.0; Chromium 144.0.7559.96 auf Debian GNU/Linux 13.
