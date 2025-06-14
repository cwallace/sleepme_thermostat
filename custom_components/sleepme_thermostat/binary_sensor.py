import logging
from homeassistant.components.binary_sensor import BinarySensorEntity, BinarySensorDeviceClass
from homeassistant.helpers.entity import EntityCategory
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass, entry, async_add_entities):
    """Set up SleepMe binary sensors from a config entry."""
    device_id = entry.data.get("device_id")
    name = entry.data.get("name")
    device_type = entry.data.get("device_type", "sleep_pad")
    coordinator = hass.data[DOMAIN][f"{device_id}_update_manager"]

    _LOGGER.debug(f"[Device {device_id}] Setting up {device_type} binary sensor platform from config entry.")

    # Get device info for all sensors
    device_info = {
        "identifiers": {(DOMAIN, device_id)},
        "name": f"{'ChiliPad Pro' if device_type == 'sleep_pad' else 'Sleep Tracker'} {name}",
        "manufacturer": "SleepMe",
        "model": entry.data.get("model"),
        "sw_version": entry.data.get("firmware_version"),
        "connections": {("mac", entry.data.get("mac_address"))},
        "serial_number": entry.data.get("serial_number"),
    }

    # Common sensors for both device types
    sensors = [
        DeviceConnectedBinarySensor(coordinator, device_info, device_id, name, device_type),
    ]

    # Device-specific sensors
    if device_type == "sleep_pad":
        sensors.append(WaterLevelLowSensor(coordinator, device_info, device_id, name))
    elif device_type == "sleep_tracker":
        sensors.append(UserDetectedSensor(coordinator, device_info, device_id, name))

    _LOGGER.debug(f"[Device {device_id}] Adding {len(sensors)} binary sensors for {device_type}")
    async_add_entities(sensors)

# Common binary sensors
class DeviceConnectedBinarySensor(CoordinatorEntity, BinarySensorEntity):
    """Representation of a binary sensor that indicates if the device is connected."""

    def __init__(self, coordinator, device_info, device_id, name, device_type):
        super().__init__(coordinator)
        self._device_id = device_id
        self._device_type = device_type
        device_name = "ChiliPad Pro" if device_type == "sleep_pad" else "Sleep Tracker"
        self._attr_name = f"{device_name} {name} Connected"
        self._attr_device_class = BinarySensorDeviceClass.CONNECTIVITY
        self._attr_unique_id = f"{DOMAIN}_{device_id}_connected"
        self._attr_entity_category = EntityCategory.DIAGNOSTIC
        self._attr_device_info = device_info

    @property
    def is_on(self):
        """Return true if the device is connected."""
        return self.coordinator.data.get("status", {}).get("is_connected", False)

# Sleep pad specific binary sensors
class WaterLevelLowSensor(CoordinatorEntity, BinarySensorEntity):
    """Representation of a binary sensor that indicates if the water level is low."""

    def __init__(self, coordinator, device_info, device_id, name):
        super().__init__(coordinator)
        self._device_id = device_id
        self._attr_name = f"ChiliPad Pro {name} Water Level Low"
        self._attr_device_class = BinarySensorDeviceClass.PROBLEM
        self._attr_unique_id = f"{DOMAIN}_{device_id}_water_low"
        self._attr_device_info = device_info

    @property
    def is_on(self):
        """Return true if the water level is low."""
        return self.coordinator.data.get("status", {}).get("is_water_low", False)

# Sleep tracker specific binary sensors
class UserDetectedSensor(CoordinatorEntity, BinarySensorEntity):
    """Representation of a binary sensor that indicates if a user is detected."""

    def __init__(self, coordinator, device_info, device_id, name):
        super().__init__(coordinator)
        self._device_id = device_id
        self._attr_name = f"Sleep Tracker {name} User Detected"
        self._attr_device_class = BinarySensorDeviceClass.OCCUPANCY
        self._attr_unique_id = f"{DOMAIN}_{device_id}_user_detected"
        self._attr_device_info = device_info

    @property
    def is_on(self):
        """Return true if a user is detected."""
        return self.coordinator.data.get("status", {}).get("user_detected", False)
