from homeassistant.core import HomeAssistant
from .const import DOMAIN


async def async_setup(hass: HomeAssistant, config: dict):
    """Set up Mia integration."""
    return True


async def async_setup_entry(hass: HomeAssistant, entry):
    """Set up from config flow."""
    return True
