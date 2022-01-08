# Container image that runs the code.
# Setup for running github actions with python was inspired by:
#   https://github.com/jacobtomlinson/python-container-action

FROM python:3-slim AS builder
ADD . /app
WORKDIR /app

# Install dependencies directly into app source dir
# Setuptools appears necessary to succesfully install requirements-parser
RUN pip install --upgrade --target=/app setuptools requirements-parser

# A distroless container image with Python and some basics like SSL certificates
# https://github.com/GoogleContainerTools/distroless
FROM gcr.io/distroless/python3-debian10
COPY --from=builder /app /app
WORKDIR /app
ENV PYTHONPATH /app
CMD ["/app/main.py"]