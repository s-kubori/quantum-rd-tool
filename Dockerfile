FROM python:3.12-slim

WORKDIR /app

# Install the CPU-only torch build first; the default PyPI wheel pulls ~5 GB of
# CUDA runtime that this container has no GPU to use.
RUN pip install --no-cache-dir torch --index-url https://download.pytorch.org/whl/cpu

# Install dependencies first so this layer is cached when only app code changes.
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .
COPY run.py .
COPY pages/ ./pages/
COPY utils/ ./utils/

# Match the host UID so bind-mounted files stay writable from WSL.
ARG UID=1000
ARG GID=1000
RUN groupadd -g ${GID} app && useradd -u ${UID} -g ${GID} -m app

# The app writes SQLite and Chroma data here.
RUN mkdir -p data && chown -R app:app /app

USER app

EXPOSE 8501 8000

CMD ["python", "run.py"]
