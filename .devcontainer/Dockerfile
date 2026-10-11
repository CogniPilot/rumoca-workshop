FROM mcr.microsoft.com/devcontainers/python:1-3.12-bookworm
# This Python-only workshop does not use the base image's Yarn apt feed.
# Remove it so unrelated stale signing keys cannot break feature installation.
RUN rm -f /etc/apt/sources.list.d/yarn.list
COPY --from=ghcr.io/astral-sh/uv:0.11.21 /uv /uvx /usr/local/bin/
# Cache dependency downloads in the image build; postCreate installs into the
# participant's writable workspace. No Rust compiler, CUDA, or large libraries.
COPY pyproject.toml uv.lock /opt/workshop-deps/
RUN cd /opt/workshop-deps && UV_CACHE_DIR=/opt/uv-cache uv sync --frozen --no-dev \
    && chown -R vscode:vscode /opt/uv-cache
ENV UV_CACHE_DIR=/opt/uv-cache
