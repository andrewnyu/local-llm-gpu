# LLM API Server

This repository contains a FastAPI server that serves a Hugging Face LLaMA model for text generation.

## Prerequisites

- Docker installed on your system
- A Hugging Face account and API token with access to the LLaMA models

## Quick Start with Docker

### 1. Clone the repository

```bash
git clone https://github.com/andrewnyu/local-llm-gpu
cd local-llm-gpu
```

### 2. Set up your Hugging Face token

Create a `.env` file in the root directory with your Hugging Face token:

```bash
echo "HUGGINGFACE_TOKEN=your_huggingface_token" > .env
```

Replace `your_huggingface_token` with your actual Hugging Face token.

### 3. Build the Docker image

```bash
docker build -t llm-api-server .
```

### 4. Run the Docker container

```bash
docker run -p 8000:8000 --env-file .env llm-api-server
```

The API server will be available at `http://localhost:8000`.

## Querying the API

The API exposes a single endpoint for text generation:

### GET /query

Send a GET request with a `text` parameter:

```bash
curl "http://localhost:8000/query?text=Tell%20me%20a%20short%20story%20about%20a%20robot"
```

Example using Python requests:

```python
import requests

response = requests.get(
    "http://localhost:8000/query",
    params={"text": "Tell me a short story about a robot"}
)

print(response.json())
```

The response will be in JSON format:

```json
{
  "response": "Tell me a short story about a robot. Once upon a time, there was a small robot named Bleep who worked in a factory..."
}
```

## Cloud Deployment

When deploying to cloud platforms, you'll need to securely provide your Hugging Face token. Here are some approaches:

### Option 1: Environment Variables (Recommended)

Most cloud platforms provide a way to set environment variables securely:

1. **AWS ECS/Fargate**: Use Secrets Manager or Parameter Store to store your token, then reference it in your task definition.
2. **Google Cloud Run**: Set environment variables in the Cloud Run service configuration.
3. **Azure Container Instances**: Use environment variables in the container configuration.

### Option 2: Manual Entry During Deployment

If you need to manually enter your Hugging Face token during deployment:

1. SSH into your cloud instance or connect to your container
2. Create or edit the `.env` file:
   ```bash
   echo "HUGGINGFACE_TOKEN=your_huggingface_token" > .env
   ```
3. Restart your application to load the new environment variable

### Option 3: Using Docker Secrets (for Docker Swarm)

If you're using Docker Swarm:

```bash
echo "your_huggingface_token" | docker secret create huggingface_token -
```

Then reference it in your docker-compose.yml:

```yaml
services:
  llm-api:
    image: llm-api-server
    secrets:
      - huggingface_token
    environment:
      - HUGGINGFACE_TOKEN_FILE=/run/secrets/huggingface_token
```

## Model Configuration

The server is configured to use `meta-llama/Llama-3.2-3B` as the default model. You can change the model in two ways:

### Option 1: Using Environment Variables (Recommended)

Add the `MODEL_NAME` variable to your `.env` file:

```bash
# .env file
HUGGINGFACE_TOKEN=your_huggingface_token
MODEL_NAME=meta-llama/Llama-3.2-1B  # Use a different model
```

### Option 2: Modifying the Default in server.py

You can also change the default model by modifying the `DEFAULT_MODEL` variable in `server.py`:

```python
# Default model for production
DEFAULT_MODEL = "meta-llama/Llama-3.2-3B"
```

Available models include:
- `meta-llama/Llama-3.2-1B` (fastest, smallest)
- `meta-llama/Llama-3.2-3B` (better quality, still reasonable speed)
- `meta-llama/Llama-3.2-8B` (higher quality, requires more resources)
- `meta-llama/Llama-3.2-70B` (highest quality, requires significant resources)

## Hardware Requirements

The server automatically detects if a GPU is available and uses it. If not, it falls back to CPU:

- With GPU: Uses CUDA with float16 precision
- Without GPU: Uses CPU with float32 precision

For production use, a GPU is strongly recommended for reasonable performance. 