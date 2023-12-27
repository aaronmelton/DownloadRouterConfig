ARG PYTHON_VER=3.11
ARG REPO_NAME=download_router_config

##################
### BASE IMAGE ###
##################

FROM python:${PYTHON_VER} AS base

ARG REPO_NAME
LABEL name=${REPO_NAME} prune=true

WORKDIR /app

RUN pip install poetry
RUN poetry config virtualenvs.create false

COPY pyproject.toml .

RUN poetry install --no-dev

##################
### TEST IMAGE ###
##################

FROM base AS test

ARG REPO_NAME
LABEL name=${REPO_NAME} prune=true

WORKDIR /app

COPY pyproject.toml .
COPY tests/ tests/
COPY download_router_config/ download_router_config/

RUN poetry install

RUN echo '-->Running Flake8p' && \
    flake8p --config pyproject.toml . && \
    echo '-->Running Black' && \
    black --config pyproject.toml --check --diff . && \
    echo '-->Running isort' && \
    find . -name '*.py' | xargs isort && \
    echo '-->Running Pylint' && \
    find . -name '*.py' | xargs pylint --rcfile=pyproject.toml && \
    echo '-->Running pydocstyle' && \
    pydocstyle . --config=pyproject.toml && \
    echo '-->Running Bandit' && \
    bandit --recursive ./ --configfile pyproject.toml && \
    echo '-->Running pytest' && \
    coverage run -m pytest --color=yes -vvv && \
    echo '-->Running coverage' && \
    coverage report

###################
### FINAL IMAGE ###
###################

FROM python:${PYTHON_VER}-slim AS cli

ARG PYTHON_VER

WORKDIR /app

RUN addgroup docker && adduser --system --shell /bin/false --disabled-password --no-create-home docker --ingroup docker

RUN mkdir -p /app/log/

COPY --from=base /usr/local/lib/python${PYTHON_VER}/site-packages /usr/local/lib/python${PYTHON_VER}/site-packages
COPY --from=base /usr/local/bin /usr/local/bin

# .dockerignore required to prevent copying unwanted files into image
COPY ./download_router_config .

RUN chown -R docker:docker /app

USER docker

ENTRYPOINT ["python", "download_router_config.py"]