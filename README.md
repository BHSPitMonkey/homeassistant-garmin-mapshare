# Garmin MapShare (Custom Integration for Home Assistant)

[![hacs_badge](https://img.shields.io/badge/HACS-Custom-41BDF5.svg?style=for-the-badge)](https://github.com/hacs/integration)

Integrate sensors in Home Assistant derived from one or more Garmin MapShare feeds

## Description

Given a user's MapShare link name and password, this custom component will periodically pull data from their KML feed 
and create a handful of entities in Home Assistant based on the state reported from an inReach satellite communicator.

**Please note:** This does not use the username and password that the Garmin owner uses to log in. Instead, it uses
the data from the user's MapShare profile on https://share.garmin.com/ assuming the owner has turned the MapShare
feature "on" and shared the link with you.

This allows you, as a friend or family member of one or more inReach owners, to track their status centrally without
having to use the MapShare web interface (or to create automations based on Zones, for example).

## Installation

Add this repository using [HACS](https://hacs.xyz/):

```
https://github.com/BHSPitMonkey/homeassistant-garmin-mapshare
```

After a successful installation and restart, you should now be able to add Garmin MapShare from the Integrations
page in Home Assistant (one or more times).

## Configuration

Each time you set up a new instance of this integration, the configuration flow will ask you for some basic information:

| Name              | Description                                                                                                     |
| ----------------- | --------------------------------------------------------------------------------------------------------------- |
| Map Link Name     | The unique name from the MapShare link URL, e.g. `MyName` if the URL is `https://share.garmin.com/share/MyName` |
| Map Link Password | The password used to protect the MapShare link (if password-protected)                                          |

## Platforms and Entities

Each MapShare feed you configure will be represented in Home Assistant as a "device" with a number of entities. These
are described below, organized by "platform":

### Device Tracker

The `device_tracker` entity represents the current GPS coordinates, and will appear on the Map.

### Binary Sensor

(Not yet implemented)

| Name          | Entity Name | Description         |
| ------------- | ----------- | ------------------- |
| In Emergency  | TBD         | *Needs description* |
| Valid GPS Fix | TBD         | *Needs description* |

### Sensor

| Name      | Entity name  | Description                               | Example state                |
| --------- | ------------ | ----------------------------------------- | ---------------------------- | 
| Elevation | `elevation`  | Elevation from GPS                        | 1628.12 m                    |
| Course    | `course`     | Course based on GPS movement              | "22.50 ° True"               |
| Velocity  | `velocity`   | Velocity based on GPS movement            | 6.0 km/h                     |
| Text      | `last_text`  | *Needs description*                       | ""                           |
| Event     | `last_event` | (Disabled by default) *Needs description* | "Tracking message received." |
| Latitude  | `latitude`   | (Disabled by default)                     | 37.728345 °                  |
| Longitude | `longitude`  | (Disabled by default)                     | -119.637130 °                |

Entities denoted as "disabled by default" are disabled because they are redundant or considered less useful, but they
can be enabled by the user from the device page if desired.

## Development Status

This integration in its starting state is the result of a random weekend work session.
It's my first Home Assistant integration, and it shows.
Pull requests are very welcome!