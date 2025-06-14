# HA-iPod Entity

This repository contains a Home Assistant custom integration that exposes an iPod connected to a Raspberry Pi as a `media_player` entity. The integration communicates with a FastAPI backend running on the Pi.

See `custom_components/ipod_dock/README.md` for setup instructions.

## Development

Run tests with:

```bash
pip install -e .[test]
pytest
```

When a tag starting with `v` is pushed, GitHub Actions builds the package and creates a release with the distribution archives.
