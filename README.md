# SleepMe Dock Pro Integration

[![Home Assistant](https://img.shields.io/badge/Home%20Assistant-Custom%20Component-%2341BDF5.svg?style=for-the-badge)](https://www.home-assistant.io/)
[![hacs][hacsbadge]](https://github.com/hacs/default)

[hacsbadge]: https://img.shields.io/badge/HACS-Custom_Repository-41BDF5.svg?style=for-the-badge

## Overview

The **SleepMe Dock Pro Integration** is a custom component for Home Assistant, designed to provide seamless control and automation for the Chilipad Dock Pro Bed Cooling System. This integration allows you to manage your sleep environment with precise temperature controls and real-time monitoring of your device's water level, ensuring optimal performance and comfort throughout the night.

**This is a fork of [rsampayo's original project](https://github.com/rsampayo/sleepme_thermostat) with added support for sleep tracking devices and enhanced functionality.**

## Features

- **Temperature Control**: Precise temperature management for your Chilipad Dock Pro
- **Water Level Monitoring**: Real-time water level sensor integration
- **Sleep Tracking Device Support**: Enhanced integration with sleep tracking devices for automated temperature adjustments
- **Home Assistant Integration**: Native support for automations, scripts, and dashboards

## About the Chilipad Dock Pro Bed Cooling System

The [Chilipad Dock Pro](https://sleep.me/) is a cutting-edge bed cooling system that regulates your bed's temperature between 55°F and 115°F, ensuring you stay comfortable all night long, regardless of room temperature or your body's heat load. The system uses water circulation to maintain your desired temperature, making it an effective solution for hot sleepers or those who want a cooler sleep environment.

## Installation

### HACS Installation (Custom Repository)

1. Add the repository to HACS:
   - Go to HACS in Home Assistant.
   - Click the three dots in the top right corner and select "Custom repositories."
   - Enter the repository URL: `https://github.com/cwallace/sleepme_thermostat` and select "Integration."
   - Click "Add."
2. Install the integration from the HACS store.
3. Restart Home Assistant.
4. Add the integration via the Home Assistant UI.

### Manual Installation

1. Download the repository contents.
2. Copy the `sleepme_thermostat` folder to your Home Assistant's `custom_components` directory.
3. Restart Home Assistant.
4. Add the integration via the Home Assistant UI.

## Configuration

1. Before configuring the integration, you need to obtain an authentication token from [Sleep.me](https://sleep.me/):
   - Log in to your account on the Sleep.me website.
   - Navigate to your account details.
   - Go to the "Developer API" section.
   - Create a new token.

2. After obtaining the token, navigate to the integrations page in Home Assistant.
3. Click on "Add Integration" and search for "SleepMe Thermostat."
4. Follow the on-screen instructions to complete the setup, where you'll need to enter the token you generated.

## Usage

Once configured, you can use the SleepMe thermostat entity in your Home Assistant automations, scripts, and dashboards. The binary sensor provides real-time information on the water level in your Dock Pro, allowing you to automate alerts or actions when the water is low. Additionally, you can use this integration to adjust the temperature settings, either via the Home Assistant UI or through automation, to ensure your bed remains at the optimal temperature throughout the night.

### Sleep Tracking Integration

This enhanced version includes support for sleep tracking devices, allowing for:
- Automated temperature adjustments based on sleep phases
- Integration with sleep sensors for optimal comfort timing
- Advanced scheduling based on sleep patterns

## License

This project is licensed under the [MIT License](LICENSE).

## Contributing

Contributions are welcome! Please open an issue or submit a pull request.

## Support

If you encounter any issues or have questions, feel free to open an issue in the [GitHub repository](https://github.com/cwallace/sleepme_thermostat).

## Acknowledgments

- Thanks to [@rsampayo](https://github.com/rsampayo) for the original [sleepme_thermostat integration](https://github.com/rsampayo/sleepme_thermostat) that this project is forked from
- Thanks to the Home Assistant community for their support and resources.
