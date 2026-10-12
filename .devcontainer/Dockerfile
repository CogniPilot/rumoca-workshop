FROM mcr.microsoft.com/devcontainers/python:1-3.12-bookworm
# The workshop does not use the base image's Yarn apt feed.
# Remove it so unrelated stale signing keys cannot break feature installation.
RUN rm -f /etc/apt/sources.list.d/yarn.list
RUN apt-get update && apt-get install -y --no-install-recommends tmux bubblewrap build-essential \
    && rm -rf /var/lib/apt/lists/*
COPY scripts/install_agent_tools.py scripts/cache_editor_extensions.py scripts/agent_tools.json /opt/workshop-agent-tools/
RUN python /opt/workshop-agent-tools/install_agent_tools.py --prefix /usr/local
RUN python /opt/workshop-agent-tools/cache_editor_extensions.py
COPY scripts/install_rumoca_cli.py /opt/workshop-agent-tools/
RUN python /opt/workshop-agent-tools/install_rumoca_cli.py --prefix /usr/local
COPY --from=ghcr.io/astral-sh/uv:0.11.21 /uv /uvx /usr/local/bin/
# Cache downloads under the container user's home, which the devcontainer CLI
# adjusts when mapping that user's UID to the host. postCreate installs into
# the writable workspace. No Rust compiler or CUDA is needed.
COPY pyproject.toml uv.lock /opt/workshop-deps/
RUN chown -R vscode:vscode /opt/workshop-deps
USER vscode
RUN cd /opt/workshop-deps && uv sync --frozen --no-dev --group torch && rm -rf .venv
USER root
