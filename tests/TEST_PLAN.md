# Test Planung
unterschiedliche Klassen von Tests
- gewoehnliche Beispiele
- Grenzwerte
- Spezialfaelle
- ungueltige Eingabe
- Seiteneffekte (z.B. Veraenderungen von Eingaben)

## Datenmodell
Tupel (city, time, temperature)
- city ist String
- time ist Anzahl Minuten seit Mitternacht
- temperature ist float // Temperatur in Grad Celsius
Rheinfolge von Messungen ist relevant

## parse_time(time_text)
Konvertiert Uhrzeit mit einem Doppelpunkt in Minuten seit Mitternacht
- Text muss zwei numerische Bestandteile getrennt durch einen Doppelpunkt
- fuehrende Nullen sind optional
- Stunde zwischen 0 und 23
- Minuten zwischen 0 und 59
- bei ungueltigem Format -> ValueError

## parse_measurement(line)
Liest genau eine Wetter-Messung
- line muss String sein -> sonst Value Error
- fuehrende/nachfolgende Leerzeichen werden entfernt
- Stadtname ist nicht leer
- Uhrzeit nach Regeln von parse_time (siehe oben)
- Temperatur in Fliesskommazahl --> wenn nicht moeglich Value Error

## filter_by_temperature(measurements, lower, upper)
Gibt alle Messungen zurueck der Temperaturen im gewuenschtem Bereich
- Grenzen sind inklusiv
- Rheinfolge der Messungen bleibt erhalten
- doppelte und identische Messungen bleiben erhalten
- uebergebene Liste nicht veraendern
- lower > upper -> ValueError
- Ergebnis ist eine Liste