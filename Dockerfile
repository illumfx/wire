FROM python:3.9

ARG TOKEN
ARG PREFIX
ARG OWNER_ID

RUN pip install poetry

WORKDIR /wire

COPY poetry.lock pyproject.toml /wire/

RUN poetry install --no-interaction --no-ansi

COPY . /wire/

CMD ["poetry", "run", "python", "-m", "src"]
