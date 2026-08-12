FROM python:3.12-slim

WORKDIR /app

# Install the CPU-only torch build first; the default PyPI wheel pulls ~5 GB of
# CUDA runtime that this container has no GPU to use.
RUN pip install --no-cache-dir torch --index-url https://download.pytorch.org/whl/cpu

# Install dependencies first so this layer is cached when only app code changes.
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .
COPY pages/ ./pages/
COPY utils/ ./utils/

# The app writes SQLite and Chroma data here.
RUN mkdir -p data

EXPOSE 8501

CMD ["streamlit", "run", "app.py", "--server.address=0.0.0.0", "--server.port=8501"]
