# 🗺️  Garmin MapShare (Custom Integration for Home Assistant)

[![hacs_badge](https://img.shields.io/badge/HACS-Default-orange.svg?style=for-the-badge)](https://github.com/hacs/integration)
![Version](https://img.shields.io/github/v/release/BHSPitMonkey/homeassistant-garmin-mapshare?style=for-the-badge)

Integrate sensors in Home Assistant derived from one or more Garmin MapShare feeds

## Description

Given a user's MapShare link name and (if required) password, this custom component will periodically pull data from
their KML feed and create a handful of entities in Home Assistant based on the state reported from an inReach
satellite communicator (or multiple communicators).

**Please note:** This does not use the username and password that the Garmin owner uses to log in. Instead, it uses
the data from the user's MapShare profile on https://share.garmin.com/ assuming the owner has turned the MapShare
feature "on" and shared the link with you.

This allows you, as a friend or family member of one or more inReach owners, to track their status centrally without
having to use the MapShare web interface (or to create automations based on Zones, for example—See the "Tips and Tricks" section below for details).

## Installation

Find this integration in [HACS](https://hacs.xyz/), or use the button below:

[![Open your Home Assistant instance and open a repository inside the Home Assistant Community Store.](https://my.home-assistant.io/badges/hacs_repository.svg)](https://my.home-assistant.io/redirect/hacs_repository/?owner=BHSPitMonkey&repository=homeassistant-garmin-mapshare)

After a successful installation and restart, you should now be able to add Garmin MapShare from the Integrations
page in Home Assistant (once per every MapShare link you wish to track).

## Configuration

Each time you set up a new instance of this integration, the configuration flow will ask you for some basic information:

| Name              | Description                                                                                                     |
| ----------------- | --------------------------------------------------------------------------------------------------------------- |
| Map Link Name     | The unique name from the MapShare link URL, e.g. `MyName` if the URL is `https://share.garmin.com/share/MyName` |
| Map Link Password | The password used to protect the MapShare link (if password-protected)                                          |

## Platforms and Entities

Each device included in each MapShare feed you configure will be represented in Home Assistant as a "device" with a number of entities. These
are described below, organized by "platform":

### Device Tracker

The `device_tracker` entity represents the current GPS coordinates, and will appear on the Map.

### Binary Sensor

| Name          | Entity Name     | Description         |
| ------------- | --------------- | ------------------- |
| In Emergency  | `in_emergency`  | True if the device is in SOS state. Messages sent while a device is in SOS mode are omitted from KML feeds except for emergency response agencies under special arrangement. |
| Valid GPS Fix | `valid_gps_fix` | True of the device has a GPS fix. This not a measure of the quality of GPS fix. It is unlikely that any point will be provided without a valid GPS fix. |

### Sensor

| Name       | Entity name  | Description                                                    | Example state                |
| ---------- | ------------ | -------------------------------------------------------------- | ---------------------------- |
| Elevation  | `elevation`  | Elevation (in meters from Mean Sea Level)                      | 1628.12 m                    |
| Course     | `course`     | Approximate direction of travel of the device, in true degrees | 22.50 °                      |
| Velocity   | `velocity`   | Ground speed of the device                                     | 6.0 km/h                     |
| Last Text  | `last_text`  | Last message sent from device (except while in SOS state)      | "I am doing good!"                           |
| Last Event | `last_event` | (Disabled by default) The last [event type](https://github.com/BHSPitMonkey/homeassistant-garmin-mapshare/wiki/inReach-KML-Feed-Documentation#event-log-types) received from the device | "Tracking message received." |
| Latitude   | `latitude`   | (Disabled by default) Latitude, as its own sensor              | 37.728345 °                  |
| Longitude  | `longitude`  | (Disabled by default) Longitude, as its own sensor             | -119.637130 °                |

Entities denoted as "disabled by default" are disabled because they are redundant or considered less useful, but they
can be enabled by the user from the device page if desired.

## Tips and Tricks

### Maps, Zones, and Automations

By default, Home Assistant will show every device tracker entity on the default Map dashboard.

The default Map dashboard only show's the most recent location for each device, but you can also see a history of
the entity's earlier locations by adding it to a Map card in any custom dashboard.

In the default Map dashboard, you can create Zones representing different places of interest. Zones become especially
useful in Automations; For example, you can create a Zone at major milestones along a backpacking route (summits,
camps, trailheads, etc.) and use an Automation to notify you whenever the tracked device enters or exits any of these
Zones.

### Map Icon Customization

The device will appear on maps as the initials of the device's Name (which you can edit within Home Assistant). You can
replace the initials with a custom image by placing an image file in your Home Assistant configuration directory's `www`
sub-directory and adding a Customize section to your `configuration.yaml` like the one shown below:

```yaml
homeassistant:
  customize:
    device_tracker.inreach_mini: # Replace with your actual entity name
      entity_picture: /local/inreach-mini-icon.png # /local/ refers to the www directory in your configuration directory
```

Learn more about customizing entities: https://www.home-assistant.io/docs/configuration/customizing-devices/

## Development Status

This integration is fairly feature-complete at this point. More translations and proper unit tests are most of what's
missing. It's my first Home Assistant integration, and it shows. Pull requests are very welcome!
