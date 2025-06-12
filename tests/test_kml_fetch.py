"""Test the entity classes."""

from custom_components.garmin_mapshare.kml_fetch import parse_response


def test_kml_fetch():
    with open("tests/fixtures/sample-feed.kml", "r") as file:
        data = file.read()

    expected = {
        "100110011001100": {
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
    }
    parsed = parse_response(data)
    assert parsed == expected


def test_kml_fetch_multiple():
    with open("tests/fixtures/sample-feed-multiple.kml", "r") as file:
        data = file.read()

    expected = {
        "11011011011011011": {
            "Id": "633432229",
            "Time UTC": "7/2/2023 6:28:00 PM",
            "Time": "7/2/2023 12:28:00 PM",
            "Name": "George Mallory",
            "Map Display Name": "George Mallory",
            "Device Type": "inReach 2.5",
            "IMEI": "11011011011011011",
            "Incident Id": None,
            "Latitude": "42.462215",
            "Longitude": "-108.794286",
            "Elevation": "1879.00 m from MSL",
            "Velocity": "0.0 km/h",
            "Course": "0.00 ° True",
            "Valid GPS Fix": "True",
            "In Emergency": "False",
            "Text": "Checking in, all good.",
            "Event": "Quick Text to MapShare received",
            "Device Identifier": None,
            "SpatialRefSystem": "WGS84",
        },
        "1000100010001000": {
            "Id": "448062523",
            "Time UTC": "12/15/2020 1:38:00 PM",
            "Time": "12/15/2020 6:38:00 AM",
            "Name": "Fred Beckey",
            "Map Display Name": "Fred Beckey",
            "Device Type": "inReach 2.5",
            "IMEI": "1000100010001000",
            "Incident Id": None,
            "Latitude": "42.478511",
            "Longitude": "-108.769975",
            "Elevation": "1891.00 m from MSL",
            "Velocity": "25.8 km/h",
            "Course": "45.00 ° True",
            "Valid GPS Fix": "True",
            "In Emergency": "False",
            "Text": "Checking in, all good.",
            "Event": "Quick Text to MapShare received",
            "Device Identifier": None,
            "SpatialRefSystem": "WGS84",
        },
        "00111001110011100": {
            "Id": "464204294",
            "Time UTC": "1/13/2021 10:33:00 PM",
            "Time": "1/13/2021 3:33:00 PM",
            "Name": "Conrad Anker",
            "Map Display Name": "Conrad Anker",
            "Device Type": "inReach 2.5",
            "IMEI": "00111001110011100",
            "Incident Id": None,
            "Latitude": "42.221741",
            "Longitude": "-108.655370",
            "Elevation": "2351.00 m from MSL",
            "Velocity": "0.0 km/h",
            "Course": "0.00 ° True",
            "Valid GPS Fix": "True",
            "In Emergency": "False",
            "Text": "I have an emergency and need help immediately.",
            "Event": "Quick Text to MapShare received",
            "Device Identifier": None,
            "SpatialRefSystem": "WGS84",
        },
    }

    parsed = parse_response(data)
    assert parsed == expected
