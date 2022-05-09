# Use intermediate stage to generate a requirements.txt file, so we don't need poetry in the final image
FROM python:3.8-slim as requirements-stage

# Install poetry with pip: this way we don't need an image with curl, and we are going to ditch this image anyway
# so it won't matter if it messes up our system packages
RUN pip install "poetry==1.1.12"
WORKDIR /packages
COPY poetry.lock pyproject.toml ./
RUN poetry export -f requirements.txt --without-hashes > requirements.txt

# Final image
FROM python:3.8-slim
WORKDIR /app
COPY --from=requirements-stage /packages/requirements.txt .
RUN pip install --no-input --no-cache-dir -r requirements.txt
COPY src/ /app

# TODO command
# install gunicorn?