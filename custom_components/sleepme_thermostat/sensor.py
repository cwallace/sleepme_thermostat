import logging
from homeassistant.components.sensor import SensorEntity, SensorDeviceClass
from homeassistant.helpers.entity import EntityCategory
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.const import UnitOfTemperature, PERCENTAGE
from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass, entry, async_add_entities):
    """Set up SleepMe sensors from a config entry."""
    device_id = entry.data.get("device_id")
    name = entry.data.get("name")
    device_type = entry.data.get("device_type", "sleep_pad")
    coordinator = hass.data[DOMAIN][f"{device_id}_update_manager"]

    _LOGGER.debug(f"[Device {device_id}] Setting up {device_type} sensor platform from config entry.")

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
        IPAddressSensor(coordinator, device_info, device_id, name, device_type),
        LANAddressSensor(coordinator, device_info, device_id, name, device_type),
    ]

    # Device-specific sensors
    if device_type == "sleep_pad":
        sensors.extend([
            # Sleep pad control sensors
            BrightnessLevelSensor(coordinator, device_info, device_id, name),
            DisplayTemperatureUnitSensor(coordinator, device_info, device_id, name),
            TimeZoneSensor(coordinator, device_info, device_id, name),
            SetTemperatureSensor(coordinator, device_info, device_id, name),
            
            # Sleep pad status sensors
            WaterLevelSensor(coordinator, device_info, device_id, name),
            WaterTemperatureSensor(coordinator, device_info, device_id, name),
        ])
    elif device_type == "sleep_tracker":
        sensors.extend([
            # Sleep tracker environment sensors
            EnvironmentTemperatureSensor(coordinator, device_info, device_id, name),
            EnvironmentHumiditySensor(coordinator, device_info, device_id, name),
            BedTemperatureSensor(coordinator, device_info, device_id, name),
        ])

    _LOGGER.debug(f"[Device {device_id}] Adding {len(sensors)} sensors for {device_type}")
    async_add_entities(sensors)

# Common sensors for both device types
class IPAddressSensor(CoordinatorEntity, SensorEntity):
    """Representation of a sensor that indicates the IP address."""

    def __init__(self, coordinator, device_info, device_id, name, device_type):
        super().__init__(coordinator)
        self._device_id = device_id
        self._device_type = device_type
        device_name = "ChiliPad Pro" if device_type == "sleep_pad" else "Sleep Tracker"
        self._attr_name = f"{device_name} {name} IP Address"
        self._attr_unique_id = f"{DOMAIN}_{device_id}_ip_address"
        self._attr_icon = "mdi:ip"
        self._attr_entity_category = EntityCategory.DIAGNOSTIC
        self._attr_device_info = device_info

    @property
    def state(self):
        """Return the IP address of the device."""
        return self.coordinator.data.get("about", {}).get("ip_address")

class LANAddressSensor(CoordinatorEntity, SensorEntity):
    """Representation of a sensor that indicates the LAN address."""

    def __init__(self, coordinator, device_info, device_id, name, device_type):
        super().__init__(coordinator)
        self._device_id = device_id
        self._device_type = device_type
        device_name = "ChiliPad Pro" if device_type == "sleep_pad" else "Sleep Tracker"
        self._attr_name = f"{device_name} {name} LAN Address"
        self._attr_unique_id = f"{DOMAIN}_{device_id}_lan_address"
        self._attr_icon = "mdi:lan"
        self._attr_entity_category = EntityCategory.DIAGNOSTIC
        self._attr_device_info = device_info

    @property
    def state(self):
        """Return the LAN address of the device."""
        return self.coordinator.data.get("about", {}).get("lan_address")

# Sleep pad specific sensors
class BrightnessLevelSensor(CoordinatorEntity, SensorEntity):
    """Representation of a sensor that indicates the brightness level."""

    def __init__(self, coordinator, device_info, device_id, name):
        super().__init__(coordinator)
        self._device_id = device_id
        self._attr_name = f"ChiliPad Pro {name} Brightness Level"
        self._attr_unique_id = f"{DOMAIN}_{device_id}_brightness_level"
        self._attr_icon = "mdi:brightness-6"
        self._attr_entity_category = EntityCategory.DIAGNOSTIC
        self._attr_native_unit_of_measurement = PERCENTAGE
        self._attr_device_info = device_info

    @property
    def state(self):
        """Return the brightness level of the device."""
        return self.coordinator.data.get("control", {}).get("brightness_level")

class DisplayTemperatureUnitSensor(CoordinatorEntity, SensorEntity):
    """Representation of a sensor that indicates the display temperature unit."""

    def __init__(self, coordinator, device_info, device_id, name):
        super().__init__(coordinator)
        self._device_id = device_id
        self._attr_name = f"ChiliPad Pro {name} Display Temperature Unit"
        self._attr_unique_id = f"{DOMAIN}_{device_id}_display_temperature_unit"
        self._attr_icon = "mdi:thermometer"
        self._attr_entity_category = EntityCategory.DIAGNOSTIC
        self._attr_device_info = device_info

    @property
    def state(self):
        """Return the display temperature unit of the device in uppercase."""
        temp_unit = self.coordinator.data.get("control", {}).get("display_temperature_unit")
        return temp_unit.upper() if temp_unit else None

class TimeZoneSensor(CoordinatorEntity, SensorEntity):
    """Representation of a sensor that indicates the time zone."""

    def __init__(self, coordinator, device_info, device_id, name):
        super().__init__(coordinator)
        self._device_id = device_id
        self._attr_name = f"ChiliPad Pro {name} Time Zone"
        self._attr_unique_id = f"{DOMAIN}_{device_id}_time_zone"
        self._attr_icon = "mdi:earth"
        self._attr_entity_category = EntityCategory.DIAGNOSTIC
        self._attr_device_info = device_info

    @property
    def state(self):
        """Return the time zone of the device."""
        return self.coordinator.data.get("control", {}).get("time_zone")

class SetTemperatureSensor(CoordinatorEntity, SensorEntity):
    """Representation of a sensor that indicates the set (target) temperature."""

    def __init__(self, coordinator, device_info, device_id, name):
        super().__init__(coordinator)
        self._device_id = device_id
        self._attr_name = f"ChiliPad Pro {name} Set Temperature"
        self._attr_unique_id = f"{DOMAIN}_{device_id}_set_temperature"
        self._attr_icon = "mdi:thermometer-plus"
        self._attr_device_class = SensorDeviceClass.TEMPERATURE
        self._attr_native_unit_of_measurement = UnitOfTemperature.FAHRENHEIT
        self._attr_device_info = device_info

    @property
    def state(self):
        """Return the set temperature of the device in Fahrenheit."""
        return self.coordinator.data.get("control", {}).get("set_temperature_f")

class WaterLevelSensor(CoordinatorEntity, SensorEntity):
    """Representation of a sensor that indicates the water level."""

    def __init__(self, coordinator, device_info, device_id, name):
        super().__init__(coordinator)
        self._device_id = device_id
        self._attr_name = f"ChiliPad Pro {name} Water Level"
        self._attr_unique_id = f"{DOMAIN}_{device_id}_water_level"
        self._attr_icon = "mdi:water-percent"
        self._attr_native_unit_of_measurement = PERCENTAGE
        self._attr_device_info = device_info

    @property
    def state(self):
        """Return the water level of the device."""
        return self.coordinator.data.get("status", {}).get("water_level")

class WaterTemperatureSensor(CoordinatorEntity, SensorEntity):
    """Representation of a sensor that indicates the current water temperature."""

    def __init__(self, coordinator, device_info, device_id, name):
        super().__init__(coordinator)
        self._device_id = device_id
        self._attr_name = f"ChiliPad Pro {name} Water Temperature"
        self._attr_unique_id = f"{DOMAIN}_{device_id}_water_temperature"
        self._attr_icon = "mdi:thermometer-water"
        self._attr_device_class = SensorDeviceClass.TEMPERATURE
        self._attr_native_unit_of_measurement = UnitOfTemperature.FAHRENHEIT
        self._attr_device_info = device_info

    @property
    def state(self):
        """Return the current water temperature of the device in Fahrenheit."""
        return self.coordinator.data.get("status", {}).get("water_temperature_f")

# Sleep tracker specific sensors
class EnvironmentTemperatureSensor(CoordinatorEntity, SensorEntity):
    """Representation of a sensor that indicates the environment temperature."""

    def __init__(self, coordinator, device_info, device_id, name):
        super().__init__(coordinator)
        self._device_id = device_id
        self._attr_name = f"Sleep Tracker {name} Environment Temperature"
        self._attr_unique_id = f"{DOMAIN}_{device_id}_environment_temperature"
        self._attr_icon = "mdi:thermometer"
        self._attr_device_class = SensorDeviceClass.TEMPERATURE
        self._attr_native_unit_of_measurement = UnitOfTemperature.FAHRENHEIT
        self._attr_device_info = device_info

    @property
    def state(self):
        """Return the environment temperature in Fahrenheit."""
        return self.coordinator.data.get("status", {}).get("environment_temperature_f")

class EnvironmentHumiditySensor(CoordinatorEntity, SensorEntity):
    """Representation of a sensor that indicates the environment humidity."""

    def __init__(self, coordinator, device_info, device_id, name):
        super().__init__(coordinator)
        self._device_id = device_id
        self._attr_name = f"Sleep Tracker {name} Environment Humidity"
        self._attr_unique_id = f"{DOMAIN}_{device_id}_environment_humidity"
        self._attr_icon = "mdi:water-percent"
        self._attr_device_class = SensorDeviceClass.HUMIDITY
        self._attr_native_unit_of_measurement = PERCENTAGE
        self._attr_device_info = device_info

    @property
    def state(self):
        """Return the environment humidity percentage."""
        return self.coordinator.data.get("status", {}).get("environment_humidity")

class BedTemperatureSensor(CoordinatorEntity, SensorEntity):
    """Representation of a sensor that indicates the bed temperature."""

    def __init__(self, coordinator, device_info, device_id, name):
        super().__init__(coordinator)
        self._device_id = device_id
        self._attr_name = f"Sleep Tracker {name} Bed Temperature"
        self._attr_unique_id = f"{DOMAIN}_{device_id}_bed_temperature"
        self._attr_icon = "mdi:bed"
        self._attr_device_class = SensorDeviceClass.TEMPERATURE
        self._attr_native_unit_of_measurement = UnitOfTemperature.FAHRENHEIT
        self._attr_device_info = device_info

    @property
    def state(self):
        """Return the bed temperature in Fahrenheit."""
        return self.coordinator.data.get("status", {}).get("bed_temperature_f")