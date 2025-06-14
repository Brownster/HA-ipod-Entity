import sys
import types
import pytest

# Create stub homeassistant modules
hass = types.ModuleType("homeassistant")
components = types.ModuleType("homeassistant.components")
media_player = types.ModuleType("homeassistant.components.media_player")
core = types.ModuleType("homeassistant.core")
config_entries = types.ModuleType("homeassistant.config_entries")

class MediaPlayerEntity:
    pass

class MediaPlayerEntityFeature:
    PLAY = 1
    PAUSE = 2
    NEXT_TRACK = 4
    PREVIOUS_TRACK = 8
    PLAY_MEDIA = 16

class MediaPlayerState(str):
    IDLE = "idle"
    UNAVAILABLE = "unavailable"

media_player.MediaPlayerEntity = MediaPlayerEntity
media_player.MediaPlayerEntityFeature = MediaPlayerEntityFeature
media_player.MediaPlayerState = MediaPlayerState
core.HomeAssistant = type("HomeAssistant", (), {})
config_entries.ConfigEntry = type("ConfigEntry", (), {})

sys.modules["homeassistant"] = hass
sys.modules["homeassistant.components"] = components
sys.modules["homeassistant.components.media_player"] = media_player
sys.modules["homeassistant.core"] = core
sys.modules["homeassistant.config_entries"] = config_entries

from ipod_dock.media_player import IpodMediaPlayer

class DummyResponse:
    def __init__(self, json_data=None, status_code=200):
        self._json = json_data or {}
        self.status_code = status_code

    def raise_for_status(self):
        if self.status_code >= 400:
            raise Exception("HTTP error")

    def json(self):
        return self._json

class DummyClient:
    def __init__(self):
        self.posts = []
        self.gets = []

    async def get(self, url):
        self.gets.append(url)
        return DummyResponse({"state": "playing", "title": "Song", "artist": "Artist"})

    async def post(self, url, json=None):
        self.posts.append((url, json))
        return DummyResponse()

@pytest.mark.asyncio
async def test_play_media_posts_request():
    client = DummyClient()
    player = IpodMediaPlayer(client, "Test Player")
    await player.async_play_media("music", "Song")
    assert ("/player/play_media", {"title": "Song"}) in client.posts
