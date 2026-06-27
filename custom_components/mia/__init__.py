from homeassistant.core import HomeAssistant
from .const import DOMAIN


async def async_setup(hass: HomeAssistant, config: dict):
    """Set up Mia integration."""
    return True


async def async_setup_entry(hass: HomeAssistant, entry):
    """Set up from config flow."""
    return True

import logging

import httpx

DOMAIN = "mia"

_LOGGER = logging.getLogger(__name__)


async def async_setup(hass: HomeAssistant, config: dict):

    async def ping_service(call):
        url = "http://100.98.38.73:8000/health"

        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(url)

            _LOGGER.info("Backend responded: %s", response.text)

        except Exception as err:
            _LOGGER.error("Ping failed: %s", err)

    hass.services.async_register(
        DOMAIN,
        "ping",
        ping_service,
    )

    return True
