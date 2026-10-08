# CATGPT 0.6 – Audio

## Musik

Vom Nutzer gewählte Vorlage: **Bruder Jakob**, traditionelle Melodie.

Die Begleitung und die synthetische Miau-Stimme werden in `src/audio.js` mit Web Audio erzeugt. Es wird keine fremde Tonaufnahme, kein Sample-Paket und kein Streamingdienst verwendet. Die Melodiefolge liegt als Notenwerte im Quelltext; Bassbegleitung, Klanggestaltung und Ablauf wurden für diese Ausgabe erstellt.

Eine Miau-Runde wechselt sich mit einer instrumentalen Runde ab. In Minispielen läuft die Begleitung etwas schneller. Die Miau-Stimme ist eine elektronische Annäherung mit Tonhöhenverlauf und Resonanzfilter, keine Aufnahme einer Katze oder einer menschlichen Stimme.

## Effekte

Auswahl, Nachricht, Ball, Napf, Wasser, Reinigung und Erfolg werden ebenfalls synthetisiert. Ein kurzer Erfolgsjingle begleitet Aufgabenabschlüsse und die Schlussentscheidung. Schnelle Mehrfachtipps werden akustisch begrenzt.

## Bedienung und Speicher

- Audio wird erst durch eine Nutzeraktion freigegeben.
- Ton oben jederzeit ein-/ausschalten.
- Musik und Effekte in den Einstellungen getrennt regeln.
- Versteckter Tab pausiert die Audiowiedergabe.
- Einstellungen werden unter `catgpt.audio.v1` gespeichert, sofern verfügbar; keine Kopplung an die Zustimmung zum Speichern des Spielstands.
- Das Spiel bleibt ohne Audio vollständig verständlich.

## Prüfung und Grenzen

Die Browserprüfung kontrolliert einen tatsächlich erzeugten Audiosignalpegel, Start per Nutzeraktion, Stumm, getrennte Pegel sowie Pause und Wiederaufnahme bei einem simulierten Sichtbarkeitswechsel.

Eine Beurteilung des Klangs durch menschliches Anhören auf Kopfhörern, iPhone- und Android-Lautsprechern steht noch aus. Ein nicht-null Signal ist kein Nachweis für angenehmen Klang. Es sind keine realen Geräteprüfungen vorgetäuscht.
