import logging

import httpx

from homeassistant.components.sensor import SensorEntity
from homeassistant.helpers.update_coordinator import (
    DataUpdateCoordinator,
    CoordinatorEntity,
)

from homeassistant.core import HomeAssistant

from .const import DOMAIN


_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    entry,
    async_add_entities
):

    server_url = entry.data["server_url"].rstrip("/")


    async def update_status():

        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{server_url}/health"
                )

            data = response.json()

            return data["status"]

        except Exception as err:
            _LOGGER.error(
                "Mia status failed: %s",
                err
            )

            return "offline"


    coordinator = DataUpdateCoordinator(
        hass,
        _LOGGER,
        name="Mia status",
        update_method=update_status,
        update_interval=30,
    )


    await coordinator.async_config_entry_first_refresh()


    async_add_entities([
        MiaStatusSensor(coordinator)
    ])



class MiaStatusSensor(CoordinatorEntity, SensorEntity):

    def __init__(self, coordinator):
        super().__init__(coordinator)

        self._attr_name = "Mia Status"
        self._attr_unique_id = "mia_status"


    @property
    def native_value(self):
        return self.coordinator.data
