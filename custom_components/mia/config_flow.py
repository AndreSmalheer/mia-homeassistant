import voluptuous as vol
import httpx

from homeassistant import config_entries

from .const import DOMAIN


class MiaConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Config flow for Mia AI."""

    VERSION = 1

    async def async_step_user(self, user_input=None):
        errors = {}

        if user_input is not None:
            server_url = user_input["server_url"].rstrip("/")

            try:
                async with httpx.AsyncClient(timeout=5) as client:
                    response = await client.get(
                        f"{server_url}/health"
                    )

                if response.status_code != 200:
                    errors["base"] = "cannot_connect"

                else:
                    return self.async_create_entry(
                        title="Mia AI",
                        data={
                            "server_url": server_url
                        },
                    )

            except Exception:
                errors["base"] = "cannot_connect"


        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema({
                vol.Required("server_url"): str,
            }),
            errors=errors,
        )
