"""Test the entity classes."""
from custom_components.garmin_mapshare.kml_fetch import parse_response


def test_kml_fetch():
    with open("tests/fixtures/sample-feed.kml", "r") as file:
        data = file.read()

    expected = {
        "Id": "123456789",
        "Time UTC": "8/26/2023 8:58:45 PM",
        "Time": "8/26/2023 1:58:45 PM",
        "Name": "John Muir",
        "Map Display Name": "John Muir",
        "Device Type": "inReach Mini",
        "IMEI": "100110011001100",
        "Incident Id": None,
        "Latitude": "48.468750",
        "Longitude": "-121.059358",
        "Elevation": "1628.12 m from MSL",
        "Velocity": "6.0 km/h",
        "Course": "22.50 ° True",
        "Valid GPS Fix": "True",
        "In Emergency": "False",
        "Text": None,
        "Event": "Tracking message received.",
        "Device Identifier": None,
        "SpatialRefSystem": "WGS84",
    }
    parsed = parse_response(data)
    assert parsed == expected
