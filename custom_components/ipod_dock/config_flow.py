import httpx
import voluptuous as vol
from homeassistant.config_entries import ConfigFlow
from .const import DOMAIN

class IpodDockConfigFlow(ConfigFlow, domain=DOMAIN):
    async def async_step_user(self, user_input=None):
        errors = {}
        if user_input is not None:
            try:
                host = user_input["host"]
                async with httpx.AsyncClient() as client:
                    response = await client.get(f"http://{host}/status")
                    response.raise_for_status()
                return self.async_create_entry(title="iPod Dock", data=user_input)
            except Exception:
                errors["base"] = "cannot_connect"
        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema({
                vol.Required("host"): str,
                vol.Optional("api_key"): str,
            }),
            errors=errors,
        )
