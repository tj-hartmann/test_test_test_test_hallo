"""Starter tests for the weather module.

These tests deliberately cover only ordinary examples. They show how pytest works,
but they are not a sufficient test suite for the specification in SPECIFICATION.md.
"""

from weather import (
    average_temperature,
    filter_by_temperature,
    hottest_measurement,
    parse_measurement,
    parse_time,
)
import pytest
# parse_time(time_text)
def test_parse_time_irregular_input():
    with pytest.raises(ValueError, match="Time must have HH:MM format."):
        parse_time('1245')
        parse_time('13:22:43')
        parse_time('7:')

def test_parse_time_not_a_digit():
    with pytest.raises(ValueError, match="Hour and minute must be numeric."):
        parse_time('HH:MM')
        parse_time('12:Uhr')
        parse_time('8:4.6')

def test_parse_hour_out_of_bound():
    with pytest.raises(ValueError, match="Hour must be between 0 and 23."):
        parse_time('35:33')
        parse_time('-2:02')

def test_parse_minutes_out_of_bound():
    with pytest.raises(ValueError, match="Minute must be between 0 and 59."):
        parse_time('12:65')
        parse_time('3:777')

def test_parse_time_regular_time():
    assert parse_time("14:21") == 861
    assert parse_time("23:59") == 1439
    assert parse_time("9:2") == 542
    assert parse_time("09:02") == 542
    assert parse_time("9:20") == 560

# parse_measurement(line)
def test_parse_measurement_irregular_input():
    with pytest.raises(ValueError, match="Measurement must be a string."):
        parse_measurement(True)
        parse_measurement(10101000010010)
        parse_measurement(["Horsthausen;20:31;6.6"])

def test_parse_measurement_irregular_format():
    with pytest.raises(ValueError, match="Expected exactly three fields."):
        parse_measurement("Ostpreussen;Kalinigrad;4:47;-10.4")
        parse_measurement("Prag;33.6")
        parse_measurement("Stockholm|20:31|6.6")
        parse_measurement("Trondheim 19:02 -4.0")

def test_parse_measurement_empty_city():
    with pytest.raises(ValueError, match="City must not be empty."):
        parse_measurement("   ; 7:44 ; 8.8")
        parse_measurement("       ;15:15;   -1.2  ")

def test_parse_measurement_temperature_to_float():
    with pytest.raises(ValueError, match="Temperature must be numeric."):
        parse_measurement("Helsinki;14:56; sehr kalt")
        parse_measurement("Oslo;21:11;True")

def test_parse_measurement_regular_line():
    assert parse_measurement("Köln;14:21;21.7") == ("Köln", 861, 21.7)
    assert parse_measurement("Bergen;2:30;-8.7") == ("Bergen", 150, -8.7)
    assert parse_measurement("Dublin;19:27;4.8") == ("Dublin", 1167, 4.8)

# filter_by_temperature(measurements, lower, upper)
def test_filter_by_temperature_irregular_boundries():
    with pytest.raises(ValueError, match="lower must not be greater than upper."):
        irish_measurements = [
            ("Londonderry", 640, 2.0),
            ("Cork", 1190, 16.5),
            ("Galway", 480, 8.3)
        ]

        filter_by_temperature(irish_measurements, 24, 0)
        filter_by_temperature(irish_measurements, 11, 11)
        
def test_filter_by_temperature_returns_list():
    scotish_measurements = [
        ("Edinburgh", 583, 12.0),
        ("Glasgow", 1297, 11.5),
        ("Aberdeen", 975, 9.1)
    ]

    assert isinstance(filter_by_temperature(scotish_measurements, 10, 15), list)

def test_filter_by_temperature_includes_boundries():
    english_measurements = [
        ("Newcastel", 777, 9.3),
        ("Manchester", 1397, 10.0),
        ("London", 435, 15.0)
    ]

    assert filter_by_temperature(english_measurements, 10, 15) == [
        ("Manchester", 1397, 10.0),
        ("London", 435, 15.0)
    ]
    
def test_filter_by_temperature_same_order():
    welsh_measurements = [
        ("Cardiff", 566, 8.4),
        ("Swansea", 933, 7.2),
        ("Newport", 570, 8.4)
    ]

    assert filter_by_temperature(welsh_measurements, 8.0, 12.5) == [
        ("Cardiff", 566, 8.4),
        ("Newport", 570, 8.4)    
    ]

def test_filter_by_temperature_regular_values():
    nrw_measurements = [
        ("Köln", 600, 10.0),
        ("Düsseldorf", 720, 18.5),
        ("Bonn", 900, 25.0),
    ]

    assert filter_by_temperature(nrw_measurements, 15.0, 20.0) == [
        ("Düsseldorf", 720, 18.5)
    ]

    nefrance_measurements = [
        ("Lille", 12, 8.3)
        ("Le Havre", 34, 9.7)
        ("Calais", 39, 7.3)
        ("Dunkirk", 57, 10.1)
        ("Paris", 63, 11.5)
        ("Caen", 88, 7.0)
        ("Rouen", 91, 6.8)
    ]

    assert filter_by_temperature(nefrance_measurements, 7.0, 10.0) == [
        ("Lille", 12, 8.3)
        ("Le Havre", 34, 9.7)
        ("Calais", 39, 7.3)
        ("Caen", 88, 7.0)
    ] 

def test_average_temperature_no_messurements():
    with pytest.raises(ValueError, match="No measurements found for city."):
        nwfrance_measurements = [
            ("Rennes", 456, 30.4)
            ("Rennes", 897, 28.5)
            ("Brest", 902, 26.8)
            ("Lorient", 1184, 21.9)
            ("Lorient", 754, 26.0)
        ]
        average_temperature(nwfrance_measurements, "Saint Malo")
        average_temperature(nwfrance_measurements, "Quimper")
        average_temperature(nwfrance_measurements, "rennes")
        average_temperature(nwfrance_measurements, "Breste")

def test_average_temperature_case_sensitive():
    efrance_measurements = [
        ("Nantes", 1230, 17.3)
        ("La Rochelle", 1198, 15.0)
        ("Les Sables-d'Olonne", 1054, 18.2)
        ("LaRochelle", 978, 18.5)
        ("Bordeaux", 822, 25.9)
        ("Les Sables dOlonne", 793, 19.9)
        ("bordeaux", 611, 22.2)
    ]
    assert average_temperature(efrance_measurements, "Bordeaux") == 25.9
    assert average_temperature(efrance_measurements, "La Rochelle") == 15.0
    assert average_temperature(efrance_measurements, "Les Sables-d'Olonne") == 18.2

def test_average_temperature_regular_values():
    measurements = [
        ("Köln", 600, 10.0),
        ("Köln", 720, 20.0),
    ]

    assert average_temperature(measurements, "Köln") == 15.0

    sefrance_measurements = [
        ("Toulouse", 792, 16.8)
        ("Toulouse", 845, 18.6)
        ("Carcassonne", 509, 23.2)
        ("Perpignan", 600, 25.3)
        ("Toulouse", 699, 16.2)
        ("Perpignan", 843, 28.7)
    ]

    assert average_temperature(sefrance_measurements, "Toulouse") == 17.2
    assert average_temperature(sefrance_measurements, "Carcassonne") == 23.2
    assert average_temperature(sefrance_measurements, "Perpignan") == 27.0

def test_hottest_measurement_with_empty_sequence():
    with pytest.raises(ValueError, match="No measurements available"):
        mars_measurements = []
        hottest_measurement(mars_measurements)

def test_hottest_measurement_with_unique_maximum():
    measurements = [
        ("Köln", 600, 10.0),
        ("Düsseldorf", 720, 25.0),
        ("Bonn", 900, 20.0),
    ]

    assert hottest_measurement(measurements) == ("Düsseldorf", 720, 25.0)

def test_hottest_measurement_with_multiple_maxima_unique_time():
    sfrance_measurements = [
        ("Montpellier", 693, 24.0)
        ("Marseille", 992, 27.4)
        ("Avignon", 1004, 26.2)
        ("Aix-en-Provence", 1423, 25.3)
        ("Cannes", 1294, 27.4)
    ]
    
    assert hottest_measurement(sfrance_measurements) == ("Marseille", 992, 27.4)

def test_hottest_measurement_with_multiple_maxima_same_time():
    efrance_measurements = [
        ("Grenoble", 15, 4.8)
        ("Lyon", 994, 18.2)
        ("Annecy", 734, 12.3)
        ("Dijon", 840, 18.5)
        ("Strasbourg", 126, 11.0)
        ("Metz", 840, 18.5)
        ("Reims", 1433, 9.4)
    ]

    assert hottest_measurement(efrance_measurements) == ("Dijon", 840, 18.5)