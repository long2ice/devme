FROM python:3.9 as builder
RUN mkdir -p /devme
WORKDIR /devme
COPY pyproject.toml poetry.lock /devme/
ENV POETRY_VIRTUALENVS_CREATE false
RUN pip3 install poetry && poetry install --no-root --no-dev

FROM node as web-builder
ENV REACT_APP_API_URL=/api
RUN mkdir -p /src
WORKDIR /src
RUN git clone https://github.com/long2ice/devme-web.git
RUN cd devme-web && npm i && npm run build

FROM python:3.9-slim
WORKDIR /devme
COPY --from=builder /usr/local/lib/python3.9/site-packages /usr/local/lib/python3.9/site-packages
COPY --from=builder /usr/local/bin/ /usr/local/bin/
COPY . /devme
COPY --from=web-builder /src/devme-web/build /devme/static
CMD ["uvicorn" ,"devme.app:app", "--host", "0.0.0.0"]
