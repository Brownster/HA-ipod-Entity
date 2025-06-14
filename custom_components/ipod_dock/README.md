# iPod Dock Home Assistant Integration

This custom integration creates a `media_player` entity to control an iPod connected to a Raspberry Pi. The integration communicates with the Pi via HTTP endpoints provided by the `ipod-dock` API.

## Installation

1. Copy the `ipod_dock` folder into your Home Assistant `custom_components` directory.
2. Restart Home Assistant.
3. In Home Assistant, go to **Settings > Devices & Services** and add the **iPod Dock** integration.
4. Enter the host (IP address) of your Raspberry Pi and optional API key.

## Voice Commands

Once added, you can control playback using Assist, for example:

- "Play the iPod" – starts playback
- "Pause the iPod" – pauses playback
- "Play *Free Bird* on the iPod" – plays a specific track
