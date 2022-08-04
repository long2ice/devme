FROM python:3.9 as builder
RUN mkdir -p /devme
WORKDIR /devme
COPY pyproject.toml poetry.lock /devme/
ENV POETRY_VIRTUALENVS_CREATE false
RUN pip3 install poetry && poetry install --no-root --no-dev

FROM python:3.9-slim
WORKDIR /devme
COPY --from=builder /usr/local/lib/python3.9/site-packages /usr/local/lib/python3.9/site-packages
COPY --from=builder /usr/local/bin/ /usr/local/bin/
COPY . /devme
CMD ['uvicorn' ,'devme.app:app', '--host', '0.0.0.0']
