"""Utilities for SleepMe device type detection and management."""
import logging

_LOGGER = logging.getLogger(__name__)

def get_device_type(device_info: dict, device_status: dict = None) -> str:
    """
    Determine device type from device info or status.
    
    Args:
        device_info: Device info from claimed devices list
        device_status: Optional device status from API
    
    Returns:
        'sleep_pad' for ChiliPad Pro devices, 'sleep_tracker' for sleep trackers
    """
    # Check attachments field first (from device list)
    attachments = device_info.get("attachments", [])
    if "CHILIPAD_PRO" in attachments:
        return "sleep_pad"
    
    # Check model field (from device status or stored info)
    model = None
    if device_status:
        model = device_status.get("about", {}).get("model")
    else:
        model = device_info.get("model")
    
    if model:
        if model.startswith("DP"):  # DP999NA = Dock Pro/ChiliPad
            return "sleep_pad"
        elif model.startswith("ST"):  # ST501NA = Sleep Tracker
            return "sleep_tracker"
    
    # Default to sleep_pad for backward compatibility
    _LOGGER.warning(f"Could not determine device type for device {device_info.get('id', 'unknown')}, defaulting to sleep_pad")
    return "sleep_pad"

def get_device_title(device_type: str, name: str) -> str:
    """Get appropriate title for device based on type."""
    if device_type == "sleep_pad":
        return f"ChiliPad Pro {name}"
    elif device_type == "sleep_tracker":
        return f"Sleep Tracker {name}"
    else:
        return f"SleepMe {name}"

def should_create_climate_entity(device_type: str) -> bool:
    """Determine if climate entity should be created for device type."""
    return device_type == "sleep_pad"

def should_create_tracker_sensors(device_type: str) -> bool:
    """Determine if sleep tracker sensors should be created for device type."""
    return device_type == "sleep_tracker" 