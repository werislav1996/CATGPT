# CATGPT – Testbericht zur Foto-Story 0.4.0

**Prüfstand: 8. Oktober 2026.** Dieser Bericht bezieht sich auf die tatsächlich erzeugte und geprüfte `catgpt.html`, nicht auf einen veröffentlichten Webauftritt.

## Ausgelieferte Datei

- Größe: **8.388.023 Bytes**.
- SHA-256: `9f595643784734546095d707781bf64484120feb1a5ef7a3716ca626db36ecdc`.
- App-Version: `0.4.0`; Speicherformat: `2`; Schlüssel: `catgpt.game.v2`.
- Offline-Foto-Story mit einer Katzenfigur, 33 freigegebenen Fotos, 68 Szenen, fünf Kapiteln, drei Minispielen und vier Enden.
- Originalfoto Nr. 14 (`1000601355.jpg`) ist weiterhin nicht enthalten.

## Tatsächlich ausgeführte Prüfungen

| Prüfgruppe | Ergebnis | Protokoll |
|---|---:|---|
| Node-Logik- und Regressionstests | **180 bestanden, 0 fehlgeschlagen** | `results/node-tests.tap` |
| Chromium: bestehende Spielabläufe und Bedienung | **76 bestanden, 0 fehlgeschlagen** | `results/browser-results.json` |
| Chromium: neue Foto-Story, Rückblick und Bilddarstellung | **38 bestanden, 0 fehlgeschlagen** | `results/slideshow-browser-results.json` |
| Seed-basierte vollständige Spielwege | **600 abgeschlossen** | `results/path-metrics.json` |
| Eingebettete Bildvarianten | **58 dekodiert und geprüft** | `results/asset-audit.json` |

Die Browsergruppen ergeben zusammen **114 bestandene Prüfungen**. Die 600 Spielwege sind Teil der Logikprüfung und keine zusätzlichen 600 menschlichen Testdurchläufe. Die Tests wurden auf der vollständigen HTML-Datei mit dem oben angegebenen Hash ausgeführt. Nach den Tests wurden nur Dokumentation, Prüfsummen und Verpackung erstellt; die getestete HTML-Datei wurde nicht mehr verändert.

## Was die Logikprüfung abdeckt

Die 157 übernommenen beziehungsweise angepassten Regressionstests und 23 neuen Foto-Story-Tests prüfen unter anderem Szenenverbindungen, Antwortkennungen, Zustandsänderungen, Endbedingungen, Replay und Kapitel-Checkpoints. Veraltete Auswahlereignisse und unzulässige Aktionen werden abgewiesen. Wiederholte Minispielabschlüsse dürfen keine mehrfachen Belohnungen erzeugen.

Geprüft werden alle sechs Startreihenfolgen der Schrank-IT, alle 27 Pitch-Kombinationen und alle 90 zulässigen Ressourcenfolgen der sechsrundigen Nickerchen-Firewall. Alle vier Enden wurden erreicht. Auswertung und übersprungene Minispiele führen weiter statt in eine Sackgasse.

Die neuen Prüfungen umfassen die elf hinzugefügten Bildstationen und ihre Verknüpfung mit dem bestehenden Ablauf. Entscheidungen zu Mitarbeiterrechten der Spielzeuge, Remote-IT, Arbeitsplatz und Sitzplatz tauchen später wieder auf. Ein kosmetischer Pfotenstempel erstellt kein Anerkennungsdokument. Für jede Szene existiert eine freigegebene Bildkennung.

Die 600 reproduzierbaren Pfade mit Seed `63471` wurden vollständig bis zu einem Ende gespielt. Gemeinsam erreichten sie **alle 68 Szenen und alle vier Enden**, ohne festgestellte Sackgasse. Auf vollständigen Pfaden wurden alle 33 Storyfotos berücksichtigt. Das ist breite Stichprobenabdeckung, kein mathematischer Beweis über jede mögliche Kombination sämtlicher Spielentscheidungen.

## Was im Browser geprüft wurde

Die vollständige Benutzeroberfläche wurde mit echten DOM-Klicks, Tastatureingaben und ihren eingebauten Spielregeln geprüft. Darunter sind Start, ein vollständiger Hauptpfad, Minispiele, alle Abschlussansichten, Fotogalerie, Export/Import, Kapitelneustart, Fehlerfälle bei Speicherung und Dialogbedienung.

Die neue Ansicht zeigt eine Szene statt eines angesammelten Chatverlaufs. Die gewählte Antwort und Teds unmittelbare Reaktion erscheinen neben dem neuen Motiv. Zurückblättern, Vorwärtsblättern und Protokollnavigation verändern den Spielzustand nicht. Historische Antwortkarten und Minispiele werden nicht reaktiviert; auch die UI-Ereignisschnittstelle weist Entscheidungen während des Rückblicks zurück. Das Zurückkehren zur aktuellen Szene stellt die echte offene Auswahl wieder her.

Die Suche und der neue Filter enthalten die erwarteten Bilder. Alle 33 vollständigen Motive und 25 Bühnenausschnitte wurden im Browser dekodiert. Die Vergrößerung verwendet das vollständige Bild statt des Bühnenausschnitts. Galerieaufrufe vergeben keinen Storyfortschritt.

Die neuen Stationen wurden auch mit schmalen Ansichten bis 320 Pixeln geprüft. „Ted lesen“ scrollt auf dem Handy zur Szene, ohne eine Entscheidung auszulösen. Die geprüften Oberflächen hatten keinen ungewollten horizontalen Seitenüberlauf. In den aufgezeichneten Prüfungen gab es keine JavaScript-Laufzeitfehler und keine externen HTTP-/HTTPS-Anfragen der Anwendung.

## Bildprüfung und manuelle Sichtkontrolle

Das Bildaudit prüft **33 optimierte vollständige WebP-Bilder und 25 zusätzliche Bühnenausschnitte** mit Python/Pillow; Chromium hat dieselben Varianten erfolgreich dekodiert. Das Audit enthält Maße und Hashes. EXIF-Metadaten sind in den geprüften Varianten nicht vorhanden. Der feste Avatar ist zusätzlich eingebettet und wird in den 58 Varianten nicht mitgezählt.

Die Bühnenausschnitte dienen nur der Platzierung. Vollständige Motive sind weiterhin erreichbar. Es wurden keine neuen Katzen, Requisiten oder Bildinhalte generiert. Die ursprünglichen Uploads bleiben unverändert. Der Schreibtisch und der Ball im Schrank bleiben als handlungsrelevante Requisiten sichtbar.

Desktop-Start, Schreibtischszene, Spielzeug-Team, Schrank-IT und mobile Szenen wurden als Screenshots visuell kontrolliert. Die Vorschauen im Ergebnisordner wurden aus derselben HTML-Datei erzeugt. Die Verwendung von Test-Checkpoints dient nur dem gezielten Erreichen der Szenen.

## Speicherung und Versionswechsel

Speicherformat 2 verwendet einen anderen Schlüssel als die bisherige Ausgabe 0.3. Ein alter Wert unter `catgpt.game.v1` blieb in der Browserprüfung unverändert. Ein Export mit altem Format wird mit einer verständlichen Meldung abgelehnt. Neue Exporte lassen sich durch Replay wiederherstellen; beschädigte oder unzulässige Ereignisse werden abgewiesen.

Mit Testadaptern wurden erfolgreiche Speicherung, verweigerter Zugriff, Schreibfehler, stillschweigend fehlgeschlagene Schreibversuche und beschädigte Werte geprüft. Diese kontrollierten Adapter sind kein Ersatz für jeden echten Browser-Speicherfall.

## Spielzeit: noch nicht menschlich gemessen

Die 20 im Pfadprotokoll ausgewiesenen Stichproben umfassten **51–55 Szenen, 47–51 Auswahlentscheidungen und 2.914–3.157 gezählte Wörter**, zuzüglich Minispielbedienung und optionaler Fotoerkundung. Diese Bereiche beschreiben die protokollierte Stichprobe, nicht garantiert jeden möglichen Pfad. Sie erlauben kein exaktes Zeitversprechen.

Die Zielgröße bleibt ungefähr 20 Minuten. Ein zeitlich gemessener menschlicher Lesedurchlauf steht noch aus. Es gibt kein Auto-Weiter und keine künstlichen Pausen, um diese Zeit zu erzwingen.

## Wichtige Prüfgrenzen

Die verwaltete Browserumgebung verweigerte das direkte Navigieren zur lokalen Datei mit `net::ERR_BLOCKED_BY_ADMINISTRATOR`. Deshalb wurde die **unveränderte, vollständige HTML-Datei mit Playwright `set_content` als Testdokument geladen**. Es wurde kein vereinfachtes Spielmodell eingesetzt. Die Speicherfälle wurden durch explizite Adapter erzeugt.

Daraus folgen diese Grenzen: Kein Nachweis über die reale `file://`-Speicherung in jedem Browser, kein Test einer veröffentlichten Adresse, kein echter Safari-/iPhone-/Android-Gerätetest und keine Zusage identischer Schrift-/Layoutdarstellung auf allen Geräten. Schmale Chromium-Ansichten sind eine Layoutprüfung, keine Hardware-Zertifizierung. Die mitgelieferte relative `index.html` wurde auf ihren Pfad geprüft; eine öffentliche Weiterleitung wurde nicht bereitgestellt.

Es gab keinen Git-Push, keine Veröffentlichung und keinen KI-Aufruf. Die Anwendung selbst benötigt für ihre geschriebene Handlung keine KI-Verbindung. Eine menschliche Bewertung von Humor und Lesetempo bleibt separat von den bestandenen technischen Tests.

## Nachvollziehen

```sh
node --test tests/game.test.mjs tests/slideshow.test.mjs
python tests/browser_checks.py
python tests/slideshow_browser.py
```

Die Node-Tests liefen unter Node.js 22.16.0; die Browserprüfungen mit installiertem Python-Playwright und dem verwalteten Chromium. Quelltests, Fixtures und Ergebnisprotokolle sind im Paket enthalten. `SHA256SUMS.txt` dokumentiert die ausgelieferten Quelldateien und Prüfartefakte.
