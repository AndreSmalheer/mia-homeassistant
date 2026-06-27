import logging

import httpx

from homeassistant.core import HomeAssistant, ServiceCall

from .const import DOMAIN


_LOGGER = logging.getLogger(__name__)


async def async_setup(hass: HomeAssistant, config: dict):
    """Set up Mia integration."""
    return True


async def async_setup_entry(hass: HomeAssistant, entry):
    """Set up Mia from a config entry."""

    server_url = entry.data["server_url"].rstrip("/")

    async def ping_service(call: ServiceCall):
        """Ping Mia backend."""

        url = f"{server_url}/health"

        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(url)

            _LOGGER.info(
                "Mia backend responded: %s",
                response.text
            )

        except Exception as err:
            _LOGGER.error(
                "Failed to ping Mia backend: %s",
                err
            )

    hass.services.async_register(
        DOMAIN,
        "ping",
        ping_service,
    )

    _LOGGER.info(
        "Mia connected to backend: %s",
        server_url
    )

    return True
