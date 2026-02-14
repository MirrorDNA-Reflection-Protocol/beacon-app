# Truth-First Beacon — Core Dockerfile
FROM alpine:latest AS hugo-builder
RUN apk add --no-cache hugo
COPY . /site
WORKDIR /site
RUN hugo --minify

FROM python:3.11-slim
RUN apt-get update && apt-get install -y --no-install-recommends \
    git gpg ipfs \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY --from=hugo-builder /site/public /app/public
COPY engine/ /app/engine/
COPY scripts/ /app/scripts/
COPY README.md hugo.toml /app/

RUN pip install --no-cache-dir -r engine/requirements.txt

# Environment variables for Ollama/IPFS/Groq
ENV OLLAMA_HOST=host.docker.internal:11434
ENV IPFS_PATH=/root/.ipfs

EXPOSE 1313
CMD ["bash"]
