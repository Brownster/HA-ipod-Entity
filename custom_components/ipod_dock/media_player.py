import logging
import httpx
from homeassistant.components.media_player import (
    MediaPlayerEntity,
    MediaPlayerEntityFeature,
    MediaPlayerState,
)

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass, config_entry, async_add_entities):
    """Set up the iPod Dock media player from a config entry."""
    host = config_entry.data["host"]
    api_key = config_entry.data.get("api_key")
    client = httpx.AsyncClient(base_url=f"http://{host}", timeout=10.0)
    if api_key:
        client.headers["Authorization"] = f"Bearer {api_key}"
    async_add_entities([IpodMediaPlayer(client, "iPod Dock")], True)


class IpodMediaPlayer(MediaPlayerEntity):
    """Representation of an iPod Dock."""

    def __init__(self, client, name):
        self._client = client
        self._name = name
        self._state = MediaPlayerState.IDLE
        self._media_title = None
        self._media_artist = None

    @property
    def name(self):
        return self._name

    @property
    def state(self):
        return self._state

    @property
    def media_title(self):
        return self._media_title

    @property
    def media_artist(self):
        return self._media_artist

    @property
    def supported_features(self):
        return (
            MediaPlayerEntityFeature.PLAY |
            MediaPlayerEntityFeature.PAUSE |
            MediaPlayerEntityFeature.NEXT_TRACK |
            MediaPlayerEntityFeature.PREVIOUS_TRACK |
            MediaPlayerEntityFeature.PLAY_MEDIA
        )

    async def async_update(self):
        try:
            response = await self._client.get("/player/status")
            response.raise_for_status()
            data = response.json()
            self._state = MediaPlayerState(data.get("state", "idle"))
            self._media_title = data.get("title")
            self._media_artist = data.get("artist")
        except Exception as err:
            _LOGGER.error("Failed to update iPod status: %s", err)
            self._state = MediaPlayerState.UNAVAILABLE

    async def async_media_play(self):
        await self._client.post("/player/play")

    async def async_media_pause(self):
        await self._client.post("/player/pause")

    async def async_media_next_track(self):
        await self._client.post("/player/next")

    async def async_media_previous_track(self):
        await self._client.post("/player/previous")

    async def async_play_media(self, media_type, media_id, **kwargs):
        payload = {"title": media_id}
        await self._client.post("/player/play_media", json=payload)
