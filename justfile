install:
    uv cache clean codework
    uv tool install --from . codework --force
