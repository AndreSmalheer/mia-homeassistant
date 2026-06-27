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

    async def send_message_service(call: ServiceCall):
        """Send message to Mia AI."""

        message = call.data["message"]

        url = f"{server_url}/message"

        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    url,
                    json={
                        "message": message
                    }
                )

            _LOGGER.info(
                "Mia response: %s",
                response.text
            )

        except Exception as err:
            _LOGGER.error(
                "Failed to send message: %s",
                err
            )

    hass.services.async_register(
        DOMAIN,
        "send_message",
        send_message_service,
    )

    await hass.config_entries.async_forward_entry_setups(
        entry,
        ["sensor"]
    )

    _LOGGER.info(
        "Mia connected to backend: %s",
        server_url
    )

    return True
