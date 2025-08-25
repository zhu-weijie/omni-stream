FROM python:3.12-slim

WORKDIR /app

RUN pip install pipx
RUN pipx ensurepath
RUN pipx install uv

COPY pyproject.toml .

RUN /root/.local/bin/uv pip install --system -r pyproject.toml

COPY . .
