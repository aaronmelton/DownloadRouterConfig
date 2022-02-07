####################
# BUILD BASE IMAGE
####################

ARG PYTHON_VER=3.10
ARG APP_NAME=download_router_config

FROM python:${PYTHON_VER} AS base

WORKDIR /usr/src/app

RUN pip install poetry
RUN poetry config virtualenvs.create false

COPY pyproject.toml .
RUN poetry install --no-dev

####################
# BUILD TEST IMAGE
####################

FROM base AS test

RUN poetry install

COPY . .

#######################
# PERFORM CODE CHECKS
#######################

RUN echo '-->Running Flake8' && \
    flake8 . && \
    echo '-->Running Black' && \
    black --check --diff . && \
    echo '-->Running isort' && \
    find . -name '*.py' | xargs isort && \
    echo '-->Running Pylint' && \
    find . -name '*.py' | xargs pylint --rcfile=pyproject.toml && \
    echo '-->Running pydocstyle' && \
    pydocstyle . --config=pyproject.toml && \
    echo '-->Running Bandit' && \
    bandit --recursive ./ --configfile pyproject.toml

ENTRYPOINT ["pytest"]

CMD ["--color=yes", "-vvv"]

#####################
# BUILD FINAL IMAGE
#####################

FROM python:${PYTHON_VER}-slim

ARG PYTHON_VER
ARG APP_NAME

WORKDIR /usr/src/app

COPY $APP_NAME /usr/src/app
#COPY --from=base /usr/src/app /usr/src/app
COPY --from=base /usr/local/lib/python${PYTHON_VER}/site-packages /usr/local/lib/python${PYTHON_VER}/site-packages
#COPY --from=base /usr/local/bin /usr/local/bin

ENTRYPOINT ["python", "download_router_config.py"]