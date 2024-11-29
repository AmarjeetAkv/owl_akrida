# #FROM ghcr.io/hyperledger/aries-cloudagent-python:py3.9-indy-1.16.0-0.8.2
# #bcgovimages/von-image:py36-1.16-1
# FROM bcgovimages/aries-cloudagent:py3.12_1.0.0

# USER root
# ENV POETRY_HOME=/opt/poetry \
#     VENV=/usr/src/app/.venv
# ENV PATH="$POETRY_HOME/bin:$VENV/bin:$PATH"

# #RUN curl -sSL https://install.python-poetry.org | python3 -
# # Fixes installation failure
# RUN pip3 install --no-cache-dir poetry
# USER aries
# RUN poetry config virtualenvs.create true; poetry config virtualenvs.in-project true

# #RUN mkdir acapy_cache_redis && touch acapy_cache_redis/__init__.py
# COPY --chown=aries:aries pyproject.toml poetry.lock ./

# RUN poetry install 

# # Make site packages location more accessible (for use with volumes)
# #RUN ln -s $(poetry env info -p)/lib/python3.6/site-packages site-packages

# #COPY --chown=indy:indy docker/default.yml .
# COPY --chown=aries:aries afj_load_testing/ afj_load_testing/

# #ENTRYPOINT ["/bin/bash", "-c", "aca-py \"$@\"", "--"]
# ENTRYPOINT ["/bin/bash", "-c", "poetry run aca-py \"$@\"", "--"]
# CMD ["start", "--arg-file", "default.yml"]

FROM bcgovimages/aries-cloudagent:py3.12_1.0.0

USER root

# Set up Poetry environment variables
ENV POETRY_HOME=/opt/poetry \
    VENV=/usr/src/app/.venv
ENV PATH="$POETRY_HOME/bin:$VENV/bin:$PATH"

# Install Poetry
RUN pip3 install --no-cache-dir poetry
USER aries

RUN poetry config virtualenvs.create true; poetry config virtualenvs.in-project true

# Copy project dependencies configuration file
COPY --chown=aries:aries pyproject.toml poetry.lock ./

# Generate a new lock file and install dependencies
RUN poetry lock --no-update \
    && poetry install  # Correct command without --no-cache-dir
RUN poetry run pip install setuptools

# Copy application code
COPY --chown=aries:aries afj_load_testing/ afj_load_testing/
COPY --chown=aries:aries configs/ configs/

# Set the entrypoint and command for the container
ENTRYPOINT ["/bin/bash", "-c", "poetry run aca-py \"$@\"", "--"]
CMD ["start", "--arg-file", "default.yml"]
