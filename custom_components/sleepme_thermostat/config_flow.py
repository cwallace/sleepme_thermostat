import logging
import voluptuous as vol
from homeassistant import config_entries
from homeassistant.data_entry_flow import FlowResult
from .sleepme import SleepMeClient
from .const import DOMAIN, API_URL
from httpx import HTTPStatusError
from .device_utils import get_device_type, get_device_title

_LOGGER = logging.getLogger(__name__)

class SleepMeThermostatConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for SleepMe Thermostat."""

    VERSION = 3

    def __init__(self) -> None:
        """Initialize the config flow."""
        self.api_token = ""
        self.claimed_devices = []

    @staticmethod
    def _schema(api_token: str = "") -> vol.Schema:
        """Return the schema for the current step."""
        return vol.Schema({
            vol.Required("api_token", default=api_token): str,
        })

    async def async_step_user(self, user_input=None) -> FlowResult:
        """Handle the initial step."""
        errors = {}

        if user_input is not None:
            _LOGGER.debug(f"User input received: {user_input}")
            self.api_token = user_input.get("api_token")

            # Instantiate SleepMeClient to get the list of devices
            client = SleepMeClient(API_URL, self.api_token)

            try:
                # Get the list of claimed devices
                self.claimed_devices = await client.get_claimed_devices()
                _LOGGER.debug(f"Claimed devices: {self.claimed_devices}")

                if not self.claimed_devices:
                    errors["base"] = "no_devices_found"
                else:
                    # Proceed to select device step
                    return await self.async_step_select_device()

            except ValueError as err:
                # Check for specific error raised for invalid token
                if str(err) == "invalid_token":
                    _LOGGER.error(f"Invalid token error: {err}")
                    errors["base"] = "invalid_token"
                else:
                    _LOGGER.error(f"Unexpected ValueError: {err}")
                    errors["base"] = "cannot_connect"
            except HTTPStatusError as e:
                _LOGGER.error(f"HTTP error fetching claimed devices: {e}")
                errors["base"] = "cannot_connect"
            except Exception as e:
                _LOGGER.error(f"Unexpected error fetching claimed devices: {e}")
                errors["base"] = "cannot_connect"

        return self.async_show_form(
            step_id="user",
            data_schema=self._schema(self.api_token),
            errors=errors,
        )

    async def async_step_select_device(self, user_input=None) -> FlowResult:
        """Step 2: Select a device from the list of claimed devices."""
        errors = {}

        if user_input is not None:
            _LOGGER.debug(f"Device selected: {user_input}")

            # Retrieve the selected device name and ID
            device_id = user_input["device_id"]
            name = self.context["claimed_devices_dict"][device_id]

            # Set a unique ID for the device configuration
            await self.async_set_unique_id(device_id)
            self._abort_if_unique_id_configured()

            # Instantiate SleepMeClient to fetch device details
            client = SleepMeClient(API_URL, self.api_token, device_id)

            try:
                # Fetch the device status, which now includes "about" information
                device_status = await client.get_device_status()
                _LOGGER.debug(f"Device status: {device_status}")
                
                # Get the selected device info for type detection
                selected_device_info = next((dev for dev in self.claimed_devices if dev["id"] == device_id), {})
                
                # Determine device type
                device_type = get_device_type(selected_device_info, device_status)
                device_title = get_device_title(device_type, name)
                
                _LOGGER.info(f"Detected device type: {device_type} for device {device_id}")

                # Store device info in the entry data
                return self.async_create_entry(
                    title=device_title,
                    data={
                        "api_url": API_URL,
                        "api_token": self.api_token,
                        "device_id": device_id,
                        "name": name,
                        "device_type": device_type,
                        "firmware_version": device_status.get("about", {}).get("firmware_version"),
                        "mac_address": device_status.get("about", {}).get("mac_address"),
                        "model": device_status.get("about", {}).get("model"),
                        "serial_number": device_status.get("about", {}).get("serial_number"),
                    },
                )

            except Exception as e:
                _LOGGER.error(f"Error fetching device status: {e}")
                errors["base"] = "cannot_fetch_device_info"

        # Prepare the selection form
        if self.claimed_devices:
            claimed_devices_dict = {device["id"]: device["name"] for device in self.claimed_devices}
            self.context["claimed_devices_dict"] = claimed_devices_dict
        else:
            errors["base"] = "no_devices_found"

        data_schema = vol.Schema({
            vol.Required("device_id"): vol.In(self.context["claimed_devices_dict"])
        })

        return self.async_show_form(
            step_id="select_device",
            data_schema=data_schema,
            errors=errors
        )

    async def async_step_import(self, user_input=None) -> FlowResult:
        """Handle import from YAML."""
        return await self.async_step_user(user_input)
