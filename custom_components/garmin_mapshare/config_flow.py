"""Config flow for Garmin MapShare integration."""
from __future__ import annotations

import logging
import re
from typing import Any

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.core import HomeAssistant
from homeassistant.data_entry_flow import AbortFlow, FlowResult
from homeassistant.exceptions import HomeAssistantError

from .const import DOMAIN, CONF_LINK_NAME, CONF_LINK_PASSWORD, PRODUCT_NAME
from .kml_fetch import KmlFetch, LinkInvalid, PasswordInvalid, PasswordRequired

_LOGGER = logging.getLogger(__name__)

STEP_USER_DATA_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_LINK_NAME): str,
        vol.Optional(CONF_LINK_PASSWORD): str,
    }
)


async def validate_input(
    hass: HomeAssistant, data: dict[str, str]
) -> tuple[dict[str, str], dict[str, str]]:
    """Validate the user input allows us to connect.

    Data has the keys from STEP_USER_DATA_SCHEMA with values provided by the user.
    """
    # If the user provided a URL, extract the last part of the URL path
    validated_data = data
    link_name_pattern = r"share/(\w+)"
    given_link_name = data[CONF_LINK_NAME]
    match = re.search(link_name_pattern, given_link_name)
    if match:
        validated_data[CONF_LINK_NAME] = match.group(1)
    else:
        validated_data[CONF_LINK_NAME] = given_link_name.strip()

    # If your PyPI package is not built with async, pass your methods
    # to the executor:
    # await hass.async_add_executor_job(
    #     your_validate_func, data["username"], data["password"]
    # )

    # Return info that you want to store in the config entry.
    return ({"title": PRODUCT_NAME}, validated_data)


async def test_connection(hass: HomeAssistant, data: dict[str, str]):
    # Test the credentials by attempting to fetch
    hub = KmlFetch(hass, data[CONF_LINK_NAME], data.get(CONF_LINK_PASSWORD, None))
    if not await hub.authenticate():
        raise CannotConnect


class ConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Garmin MapShare."""

    VERSION = 1

    async def async_step_user(
        self, user_input: dict[str, str] | None = None
    ) -> FlowResult:
        """Handle the initial step."""
        data_schema = STEP_USER_DATA_SCHEMA
        errors: dict[str, str] = {}
        if user_input is not None:
            try:
                (info, user_input) = await validate_input(self.hass, user_input)
                await self.async_set_unique_id(user_input[CONF_LINK_NAME].lower())
                self._abort_if_unique_id_configured()
                test_connection(self.hass, user_input)
            except AbortFlow as e:
                raise e
            except CannotConnect:
                errors["base"] = "cannot_connect"
            except LinkInvalid:
                errors[CONF_LINK_NAME] = "invalid_link"
            except PasswordInvalid:
                errors[CONF_LINK_PASSWORD] = "invalid_auth"
            except PasswordRequired:
                errors[CONF_LINK_PASSWORD] = "password_required"
            except Exception:  # pylint: disable=broad-except
                _LOGGER.exception("Unexpected exception")
                errors["base"] = "unknown"
            else:
                return self.async_create_entry(title=info["title"], data=user_input)
            data_schema = self.add_suggested_values_to_schema(data_schema, user_input)

        return self.async_show_form(
            step_id="user", data_schema=data_schema, errors=errors
        )


class CannotConnect(HomeAssistantError):
    """Error to indicate we cannot connect."""
