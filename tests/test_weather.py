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
    with pytest.raises(ValueError, mark="Time must have HH:MM format."):
        parse_time('1245')
        parse_time('13:22:43')
        parse_time('7:')

def test_parse_time_not_a_digit():
    with pytest.raises(ValueError, mark="Hour and minute must be numeric."):
        parse_time('HH:MM')
        parse_time('12:Uhr')
        parse_time('8:4.6')

def test_parse_hour_out_of_bound():
    with pytest.raises(ValueError, mark="Hour must be between 0 and 23."):
        parse_time('35:33')
        parse_time('-2:02')

def test_parse_minutes_out_of_bound():
    with pytest.raises(ValueError, mark="Minute must be between 0 and 59."):
        parse_time('12:65')
        parse_time('3:777')

def test_parse_time_regular_time():
    assert parse_time("14:21") == 861
    assert parse_time("23:59") == 1439
    assert parse_time("9:2") == 542
    assert parse_time("09:02") == 542
    assert parse_time("9:20") == 560


def test_parse_measurement_regular_line():
    assert parse_measurement("Köln;14:21;21.7") == ("Köln", 861, 21.7)


def test_filter_by_temperature_regular_values():
    measurements = [
        ("Köln", 600, 10.0),
        ("Düsseldorf", 720, 18.5),
        ("Bonn", 900, 25.0),
    ]

    assert filter_by_temperature(measurements, 15.0, 20.0) == [
        ("Düsseldorf", 720, 18.5)
    ]


def test_average_temperature_regular_values():
    measurements = [
        ("Köln", 600, 10.0),
        ("Köln", 720, 20.0),
    ]

    assert average_temperature(measurements, "Köln") == 15.0


def test_hottest_measurement_with_unique_maximum():
    measurements = [
        ("Köln", 600, 10.0),
        ("Düsseldorf", 720, 25.0),
        ("Bonn", 900, 20.0),
    ]

    assert hottest_measurement(measurements) == ("Düsseldorf", 720, 25.0)
